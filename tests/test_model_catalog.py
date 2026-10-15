import contextlib
import copy
import io
import json
import logging
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
with patch('logging.FileHandler', return_value=logging.NullHandler()):
    import generate
from model_catalog import MODEL_IDS, MODEL_PROFILES, normalize_video_request, resolve_model_type


class WebsiteModelCompatibility(unittest.TestCase):
    def test_removed_models_fail_before_network_or_balance(self):
        removed = [(7, 'kling2.0', 'Kling 2.0'), (15, 'venus', 'Venus AI 1.0'), (91, 'kling2.6', 'Kling 2.6'), (92, 'klingo1', 'Kling O1')]
        with patch.object(generate, 'http_request') as http, patch.object(generate, 'action_balance') as balance:
            for model, key, name in removed:
                for value in (model, str(model), float(model), key, name, key.upper()):
                    for mode in (0, 1):
                        body = dict(model_type=value, generate_type=mode, prompt='Prompt')
                        with self.subTest(model=value, mode=mode):
                            for call in [lambda: generate.action_price('/api/lumeflow/video-generate', body),
                                         lambda: generate.action_generate('video-generate', body),
                                         lambda: generate.action_generate_with_balance('video-generate', body),
                                         lambda: generate.action_watch('video', body)]:
                                with self.assertRaises(ValueError):
                                    call()
            http.assert_not_called()
            balance.assert_not_called()

    def test_requested_website_ids(self):
        # Contract supplied by the website, independent of catalog construction.
        expected = {'kling1.6': 1, 'kling2.5': 19, 'pix6': 21,
            'pix5': 9, 'pix4.5': 41, 'hailuo02': 3, 'veo3.1': 4, 'veo3fast': 5,
            'viduQ1': 6, 'sora2': 11, 'sora2Pro': 27, 'viduQ2': 26,
            'pix5.5': 28, 'kling3.0': 65, 'seedance2.0': 73,
            'seedance2.0 fast': 71, 'seedance2.0 vip': 86, 'seedance2.0 vip fast': 87,
            'hailuo2.3': 23, 'hailuo2.3 fast': 25, 'wan2.5': 63,
            'viduQ2 turbo': 24, 'wan2.6': 64, 'wan2.7': 89, 'seeance1.5pro': 50,
            'pixC1': 88, 'wanHappyHorse1.1': 151, 'wanHappyHorse': 104,
            'grok_imagine1.5': 95, 'seedance2.5': 168, 'seedance2.0 mini': 150,
            'gemini_omni': 112, 'minimaxH3': 166}
        self.assertEqual(MODEL_IDS, expected)
        for key, model in expected.items():
            with self.subTest(key=key):
                self.assertEqual(resolve_model_type(key), model)
                self.assertEqual(resolve_model_type(MODEL_PROFILES[model]['name']), model)
        self.assertEqual(resolve_model_type('seedance1.5pro'), 50)
        self.assertEqual(resolve_model_type('Pixverse V5'), 41)
        self.assertEqual(resolve_model_type('Lumeflow 3.0'), 9)

    def test_every_model_prices_and_submits_supported_modes(self):
        for key, model in MODEL_IDS.items():
            for kind in MODEL_PROFILES[model]['modes']:
                with self.subTest(key=key, mode=kind), patch.object(generate, 'http_request', return_value={}) as http:
                    original = dict(model_type=key, generate_type=kind, prompt='完整提示词\nShot 2: keep formatting')
                    if kind == 1:
                        original['image'] = 'https://example.com/start.png'
                    snapshot = copy.deepcopy(original)
                    generate.action_price('/api/lumeflow/video-generate', original)
                    priced = http.call_args.kwargs['body'].copy()
                    priced.pop('route')
                    generate.action_generate('video-generate', original)
                    submitted = http.call_args.kwargs['body']
                    self.assertEqual(priced, submitted)
                    self.assertEqual(submitted['model_type'], model)
                    self.assertEqual(submitted['generate_type'], kind)
                    self.assertEqual(submitted['prompt'], snapshot['prompt'])
                    self.assertEqual(original, snapshot)
                    self.assertEqual(normalize_video_request(submitted), submitted)
                    if kind == 1:
                        self.assertTrue(submitted.get('image') or submitted.get('images'))

    def test_duration_resolution_boundaries_from_page_rules(self):
        accepted = [(21, 2, '1080P'), (21, 15, '1080P'), (65, 3, '4K'),
            (65, 15, '4K'), (50, 4, '480P'), (50, 12, '1080P'),
            (168, 4, '480P'), (168, 30, '720P'), (166, 4, '768P'),
            (166, 15, '2K'), (104, 3, '720P'), (151, 15, '1080P'),
            (27, 25, '1080P'), (11, 15, '720P'), (112, 6, '1080P'),
            (112, 10, '720P'), (9, 5, '1080P'), (41, 5, '1080P'), (28, 8, '1080P')]
        for model, duration, resolution in accepted:
            with self.subTest(model=model, duration=duration, resolution=resolution):
                result = normalize_video_request(dict(model_type=model, prompt='Prompt', duration=duration, resolution=resolution))
                self.assertEqual(result['duration'], duration)
                self.assertEqual(result['resolution'], resolution)
        rejected = [(21, 1, '720P'), (65, 2, '720P'), (50, 13, '720P'),
            (168, 31, '720P'), (168, 20, '1080P'), (166, 15, '1080P'),
            (104, 2, '720P'), (151, 16, '720P'), (11, 25, '720P'),
            (27, 25, '720P'), (112, 5, '720P'), (9, 8, '1080P'),
            (41, 8, '1080P'), (28, 10, '1080P')]
        for model, duration, resolution in rejected:
            with self.subTest(model=model, duration=duration, resolution=resolution), self.assertRaises(ValueError):
                normalize_video_request(dict(model_type=model, prompt='Prompt', duration=duration, resolution=resolution))

    def test_models_with_omitted_fields(self):
        q1 = normalize_video_request(dict(model_type=6, prompt='Prompt', duration=5, resolution='720P', motion_mode='2'))
        self.assertNotIn('duration', q1)
        self.assertNotIn('resolution', q1)
        self.assertEqual(q1['moition_range'], '1')
        self.assertEqual(q1['is_switch_audio'], 0)
        veo = normalize_video_request(dict(model_type=4, prompt='Prompt', resolution='1080P'))
        self.assertNotIn('resolution', veo)
        self.assertEqual(veo['duration'], 8)
        hailuo = normalize_video_request(dict(model_type=3, prompt='Prompt', ratio='1:1', is_switch_audio=1))
        self.assertNotIn('ratio', hailuo)
        self.assertEqual(hailuo['is_switch_audio'], 0)
        self.assertEqual(hailuo['resolution'], '768P')

    def test_reference_arrays_survive_omni_normalization(self):
        for model, counts in [(168, (30, 10, 10)), (166, (9, 3, 3)), (150, (9, 3, 3)), (86, (9, 3, 3))]:
            with self.subTest(model=model):
                body = dict(model_type=model, generate_type=1, function_mode=1, prompt='@image1 @video1 @audio1',
                    images=['https://example.com/image.png'] * counts[0],
                    videos=['https://example.com/video.mp4'] * counts[1],
                    audios=['https://example.com/audio.mp3'] * counts[2])
                result = normalize_video_request(body)
                for field in ('images', 'videos', 'audios'):
                    self.assertEqual(result[field], body[field])
                    excessive = copy.deepcopy(body)
                    excessive[field].append('https://example.com/extra')
                    with self.assertRaises(ValueError):
                        normalize_video_request(excessive)
                self.assertIn('duration', result)
                self.assertIn('is_switch_audio', result)
                self.assertNotIn('motion_mode', result)

    def test_happy_horse_image_compatibility(self):
        for model in (104, 151):
            body = dict(model_type=model, generate_type=1, prompt='Prompt', image='https://example.com/image.png')
            result = normalize_video_request(body)
            self.assertEqual(result['images'], [body['image']])
            self.assertNotIn('image', result)
            self.assertNotIn('is_switch_audio', result)
            self.assertNotIn('motion_mode', result)
            for changes in (dict(images=['url'] * 10), dict(videos=['url']), dict(image_tail='url')):
                with self.subTest(model=model, changes=changes), self.assertRaises(ValueError):
                    normalize_video_request({**body, **changes})

    def test_unsupported_modes_are_rejected_before_network(self):
        requests = [dict(model_type=26, generate_type=1, image='url'),
            dict(model_type=24, generate_type=0), dict(model_type=95, generate_type=0),
            dict(model_type=112, generate_type=1, function_mode=1, images=['url']),
            dict(model_type=50, generate_type=1, function_mode=1, images=['url']),
            dict(model_type=166, generate_type=3, videos=['url'])]
        for request in requests:
            with self.subTest(request=request), patch.object(generate, 'http_request') as http:
                with self.assertRaises(ValueError):
                    generate.action_price('/api/lumeflow/video-generate', {**request, 'prompt': 'Prompt'})
                http.assert_not_called()

    def test_frame_ratios_and_end_frame_modes(self):
        for model in (168, 166):
            result = normalize_video_request(dict(model_type=model, generate_type=1, function_mode=0,
                prompt='Prompt', image='url', image_tail='end', ratio='16:9'))
            self.assertEqual(result['ratio'], 'auto')
            self.assertEqual(result['image_tail'], 'end')
        kling = dict(model_type=1, generate_type=1, prompt='Prompt', image='url', image_tail='end')
        self.assertEqual(normalize_video_request(kling)['motion_mode'], '2')
        with self.assertRaises(ValueError):
            normalize_video_request({**kling, 'motion_mode': '1'})
        for model in (63, 64, 95):
            with self.subTest(model=model), self.assertRaises(ValueError):
                normalize_video_request({**kling, 'model_type': model})

    def test_audio_ratios_optional_fields_and_aliases(self):
        for model in (50, 65, 168, 86, 87):
            self.assertEqual(normalize_video_request(dict(model_type=model, prompt='Prompt', is_switch_audio=0))['is_switch_audio'], 0)
        for model in (4, 11, 19, 27, 112, 166):
            self.assertEqual(normalize_video_request(dict(model_type=model, prompt='Prompt', is_switch_audio=0))['is_switch_audio'], 1)
        with self.assertRaises(ValueError):
            normalize_video_request(dict(model_type=63, prompt='Prompt', resolution='480P', ratio='4:3'))
        self.assertEqual(normalize_video_request(dict(model_type=63, prompt='Prompt', resolution='720P', ratio='4:3'))['ratio'], '4:3')
        self.assertEqual(normalize_video_request(dict(model_type=64, prompt='Prompt', shot_type=0))['shot_type'], 'single')
        for old, current in [(130, 21), (22, 63), (32, 64), (76, 71), (153, 150)]:
            self.assertEqual(normalize_video_request(dict(model_type=old, prompt='Prompt'))['model_type'], current)
        self.assertEqual(resolve_model_type(29), 29)
        self.assertEqual(resolve_model_type(30), 30)

    def test_large_and_heic_uploads_are_model_bound(self):
        with patch.object(generate.os.path, 'isfile', return_value=True), \
             patch.object(generate.os.path, 'getsize', return_value=12 * 1024 * 1024):
            with self.assertRaises(ValueError):
                generate.validate_upload_image('image.png')
            with self.assertRaises(ValueError):
                generate.validate_upload_image('image.png', model=168, function_mode=0)
            self.assertEqual(generate.validate_upload_image('image.png', model=168, function_mode=1), 'image/png')
            self.assertEqual(generate.validate_upload_image('image.heic', model=166), 'image/heic')
            self.assertEqual(generate.validate_upload_image('image.heif', model='minimaxH3'), 'image/heif')
            with self.assertRaises(ValueError):
                generate.validate_upload_image('image.heic', model=168, function_mode=1)
        with patch.object(generate.os.path, 'isfile', return_value=True), \
             patch.object(generate.os.path, 'getsize', return_value=31 * 1024 * 1024):
            with self.assertRaises(ValueError):
                generate.validate_upload_image('image.png', model=166)

    def test_read_only_model_cli_needs_no_api_or_login(self):
        with patch.object(sys, 'argv', ['generate.py', '--action', 'models', '--model', 'seedance2.5']), \
             patch.object(generate, 'http_request') as http, patch.object(generate, 'ensure_runtime_config') as config:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                generate.main()
            result = json.loads(output.getvalue())
            self.assertEqual(result['models'][0]['model_type'], 168)
            self.assertEqual(result['models'][0]['durations'][-1], 30)
            http.assert_not_called()
            config.assert_not_called()


if __name__ == '__main__':
    unittest.main()
