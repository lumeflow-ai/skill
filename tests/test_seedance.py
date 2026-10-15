import copy
import logging
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
with patch('logging.FileHandler', return_value=logging.NullHandler()):
    import generate


class SeedanceRequests(unittest.TestCase):
    def body(self, model=73, **changes):
        body = dict(generate_type=0, model_type=model, prompt='Full prompt\nSecond line',
                    duration=5, resolution='720P', ratio='auto', outputs=1,
                    is_switch_audio=1)
        body.update(changes)
        return body

    def validate(self, body):
        return generate.validate_video_resolution(generate.validate_video_duration(body))

    def test_all_duration_boundaries_and_modes(self):
        for model in (73, 71, 86, 87, 150):
            for duration in (4, 7, 15):
                for mode in ('text', 'frame', 'omni'):
                    with self.subTest(model=model, duration=duration, mode=mode):
                        body = self.body(model, duration=duration)
                        if mode == 'frame':
                            body.update(generate_type=1, function_mode=0, image='https://example.com/image.png')
                        if mode == 'omni':
                            body.update(generate_type=1, function_mode=1, videos=['https://example.com/video.mp4'])
                        result = self.validate(body)
                        self.assertEqual(result['duration'], duration)
                        self.assertEqual(result['prompt'], 'Full prompt\nSecond line')
                        self.assertEqual(result['is_switch_audio'], 1)
            for duration in (3, 16, 4.5):
                with self.subTest(model=model, invalid_duration=duration), self.assertRaises(ValueError):
                    self.validate(self.body(model, duration=duration))

    def test_resolution_and_audio_by_model(self):
        for model in (73, 71, 86, 87, 150):
            with self.subTest(model=model):
                result = self.validate(self.body(model, is_switch_audio=0, resolution='480p'))
                self.assertEqual(result['resolution'], '480P')
                self.assertEqual(result['is_switch_audio'], 0 if model in (86, 87) else 1)
                if model in (73, 86):
                    self.validate(self.body(model, resolution='1080P'))
                else:
                    with self.assertRaises(ValueError):
                        self.validate(self.body(model, resolution='1080P'))

    def test_reference_compatibility_and_counts(self):
        for model in (73, 71, 86, 87, 150):
            for field, count in [('images', 10), ('videos', 2 if model in (73, 71) else 4),
                                 ('audios', 1 if model in (73, 71) else 4)]:
                with self.subTest(model=model, field=field), self.assertRaises(ValueError):
                    self.validate(self.body(model, generate_type=1, function_mode=1,
                                            **{field: ['https://example.com/material'] * count}))
            if model in (86, 87, 150):
                result = self.validate(self.body(model, generate_type=1, function_mode=1,
                                                audios=['https://example.com/audio.mp3']))
                self.assertEqual(len(result['audios']), 1)
        for changes in (dict(generate_type=1, function_mode=1),
                        dict(generate_type=1, function_mode=0),
                        dict(generate_type=0, function_mode=1, images=['url']),
                        dict(generate_type=1, function_mode=1, images='url'),
                        dict(generate_type=1, function_mode=1, images=[''])):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.validate(self.body(**changes))

    def test_other_models_keep_existing_constraints(self):
        self.validate(self.body(88, duration=2, resolution='720P', ratio='1:1'))
        with self.assertRaises(ValueError):
            self.validate(self.body(3, duration=10, resolution='1080P'))
        self.validate(self.body(3, duration=10, resolution='768P'))

    def test_price_and_generation_send_identical_normalized_body(self):
        for alias, model in [(76, 71), (70, 71), (74, 71), (160, 71), (161, 73),
                             (152, 150), (153, 150), (86, 86), (87, 87)]:
            with self.subTest(alias=alias), patch.object(generate, 'http_request', return_value={}) as http:
                original = self.body(alias, generate_type=1, function_mode=1,
                                     images=['https://example.com/image.png'], motion_mode='2',
                                     image='stale', image_tail='stale', ratio='Auto')
                saved = copy.deepcopy(original)
                generate.action_price('/api/lumeflow/video-generate', original)
                priced = http.call_args.kwargs['body'].copy()
                priced.pop('route')
                generate.action_generate('video-generate', original)
                submitted = http.call_args.kwargs['body']
                self.assertEqual(priced, submitted)
                self.assertEqual(submitted['model_type'], model)
                self.assertEqual(submitted['ratio'], 'auto')
                self.assertNotIn('motion_mode', submitted)
                self.assertNotIn('image', submitted)
                self.assertNotIn('image_tail', submitted)
                self.assertEqual(original, saved)

    def test_invalid_requests_never_reach_network(self):
        for changes in (dict(outputs=5), dict(prompt=''), dict(prompt='x' * 5001),
                        dict(ratio='21:9'), dict(is_switch_audio=2), dict(duration=16)):
            with self.subTest(changes=changes), patch.object(generate, 'http_request') as http:
                for operation in (lambda: generate.action_price('/api/lumeflow/video-generate', self.body(**changes)),
                                  lambda: generate.action_generate('video-generate', self.body(**changes))):
                    with self.assertRaises(ValueError):
                        operation()
                http.assert_not_called()

    def test_invalid_watch_and_balance_wrapper_do_not_query_balance(self):
        with patch.object(generate, 'action_balance') as balance:
            with self.assertRaises(ValueError):
                generate.action_generate_with_balance('video-generate', self.body(71, resolution='1080P'))
            with self.assertRaises(ValueError):
                generate.action_watch('video', self.body(150, duration=3))
            balance.assert_not_called()


if __name__ == '__main__':
    unittest.main()
