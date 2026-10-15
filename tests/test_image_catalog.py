import copy
import contextlib
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
from image_catalog import IMAGE_IDS, IMAGE_PROFILES, normalize_image_request, resolve_image_model


class ImageCompatibility(unittest.TestCase):
    def test_removed_models_fail_before_network_or_balance(self):
        removed = [(39, 'fluxKontextMax', 'Flux Kontext Max'), (40, 'fluxKontextPro', 'Flux Kontext Pro')]
        with patch.object(generate, 'http_request') as http, patch.object(generate, 'action_balance') as balance:
            for model, key, name in removed:
                for value in (model, str(model), float(model), key, name, key.upper()):
                    for mode in (3, 4):
                        body = dict(model_type=value, generate_type=mode, prompt='Prompt')
                        with self.subTest(model=value, mode=mode):
                            for call in [lambda: generate.action_price('/api/lumeflow/image-generate', body),
                                         lambda: generate.action_generate('image-generate', body),
                                         lambda: generate.action_generate_with_balance('image-generate', body),
                                         lambda: generate.action_watch('image', body)]:
                                with self.assertRaises(ValueError):
                                    call()
            http.assert_not_called()
            balance.assert_not_called()

    def test_ids_and_image_video_namespaces(self):
        self.assertEqual(IMAGE_IDS, {'nanobanana': 18, 'nanobanana2': 72, 'nanobanana21': 179,
            'nanobananaPro': 37, 'seedream4.0': 12, 'seedream5.0': 80,
            'seedream5Pro': 165, 'klingO1': 38, 'gptImage2': 101, 'gptImage25': 174})
        for key, model in IMAGE_IDS.items():
            self.assertEqual(resolve_image_model(key), model)
        self.assertEqual(resolve_image_model('GPT Image 2.5 Sunburst'), 175)
        self.assertEqual(resolve_image_model(175), 175)  # History alias must not overwrite mode.
        self.assertEqual(resolve_image_model(108), 72)
        self.assertEqual(resolve_image_model('klingO1'), 38)
        with self.assertRaises(ValueError):
            generate.resolve_model_type('klingo1')

    def test_price_and_submit_use_same_body_for_every_mode(self):
        for model, p in IMAGE_PROFILES.items():
            for kind in p['modes']:
                with self.subTest(model=model, kind=kind):
                    body = dict(model_type=p['key'], generate_type=kind, prompt=' Full\nprompt ', outputs=2)
                    if kind == 4:
                        body['images'] = ['https://example.com/reference.png']
                    original = copy.deepcopy(body)
                    normalized = normalize_image_request(body)
                    self.assertEqual(normalize_image_request(normalized), normalized)
                    self.assertEqual(normalized['prompt'], original['prompt'])
                    self.assertEqual(body, original)
                    with patch.object(generate, 'http_request', return_value={'code': 200}) as http:
                        generate.action_price('/api/lumeflow/image-generate', body)
                        priced = dict(http.call_args.kwargs['body'])
                        self.assertEqual(priced.pop('route'), '/api/lumeflow/image-generate')
                        generate.action_generate('image-generate', body)
                        self.assertEqual(priced, http.call_args.kwargs['body'])

    def test_nanobanana21_defaults_aliases_and_cli(self):
        for value in (179, '179', 'nanobanana21', 'Nano Banana 2.1', 'Nano Banana V2.1'):
            self.assertEqual(resolve_image_model(value), 179)
            body = normalize_image_request(dict(model_type=value, prompt='Prompt'))
            self.assertEqual(body, dict(model_type=179, prompt='Prompt', generate_type=3,
                                        outputs=1, ratio='auto', resolution='1K'))
        out = io.StringIO()
        with patch.object(sys, 'argv', ['generate.py', '--action', 'image-models', '--model', 'nanobanana21']), contextlib.redirect_stdout(out), patch.object(generate, 'http_request') as http, patch.object(generate, 'ensure_runtime_config') as config:
            generate.main()
            http.assert_not_called()
            config.assert_not_called()
        self.assertEqual(json.loads(out.getvalue())['models'][0]['model_type'], 179)
        with patch('os.path.isfile', return_value=True), patch('os.path.getsize', return_value=10 * 1024 * 1024):
            generate.validate_upload_image('test.png', model='nanobanana21', model_kind='image')
        with patch('os.path.isfile', return_value=True), patch('os.path.getsize', return_value=10 * 1024 * 1024 + 1):
            with self.assertRaises(ValueError):
                generate.validate_upload_image('test.png', model=179, model_kind='image')

    def test_nanobanana21_parameters_and_invalid_requests(self):
        for mode in (3, 4):
            body = dict(model_type=179, prompt='x' * 5000, generate_type=mode, outputs=4)
            if mode == 4:
                body['images'] = ['url'] * 14
            for resolution in ('1K', '2K', '4K'):
                for ratio in ('auto', '1:1', '4:3', '3:4', '16:9', '9:16', '3:2', '2:3', '5:4', '4:5'):
                    result = normalize_image_request(dict(body, resolution=resolution, ratio=ratio))
                    self.assertEqual(result['ratio'], ratio)
                    self.assertEqual(result['resolution'], resolution)
            for changes in (dict(prompt='x' * 5001), dict(resolution='8K'),
                            dict(ratio='21:9'), dict(outputs=0), dict(outputs=5),
                            dict(images=[] if mode == 4 else ['url']),
                            dict(images=['url'] * 15), dict(generate_type=1)):
                invalid = {**body, **changes}
                with self.subTest(mode=mode, changes=list(changes)), patch.object(generate, 'http_request') as http, patch.object(generate, 'action_balance') as balance:
                    for call in [lambda: generate.action_price('/api/lumeflow/image-generate', invalid),
                                 lambda: generate.action_generate('image-generate', invalid),
                                 lambda: generate.action_generate_with_balance('image-generate', invalid),
                                 lambda: generate.action_watch('image', invalid)]:
                        with self.assertRaises(ValueError):
                            call()
                    http.assert_not_called()
                    balance.assert_not_called()

    def test_model_specific_resolution_and_omitted_fields(self):
        def norm(model, **kw):
            return normalize_image_request(dict(model_type=model, prompt='x', **kw))
        self.assertNotIn('resolution', norm(18, resolution='4K'))
        self.assertEqual(norm(12, ratio='auto')['ratio'], '')
        self.assertEqual(norm(37)['resolution'], '2K')
        self.assertEqual(norm(37, generate_type=4, images=['url'])['resolution'], '1K')
        self.assertEqual(norm(101, resolution='4k', moition_range=4)['resolution'], '4K')
        self.assertEqual(norm(101, moition_range=4)['moition_range'], '4')
        self.assertEqual(norm(80, is_web_search=1)['is_web_search'], 1)
        self.assertEqual(norm(12, is_web_search=1)['is_web_search'], 0)
        self.assertNotIn('is_web_search', norm(165, is_web_search=1))
        for model, res in [(80, '1K'), (80, '4K'), (165, '4K'), (37, '1K')]:
            with self.subTest(model=model, res=res), self.assertRaises(ValueError):
                norm(model, resolution=res)
        for model, ratio in [(101, 'auto'), (174, '21:9'), (37, 'auto')]:
            with self.subTest(model=model, ratio=ratio), self.assertRaises(ValueError):
                norm(model, ratio=ratio)

    def test_reference_counts_and_prompt_limits(self):
        for model, p in IMAGE_PROFILES.items():
            body = dict(model_type=model, generate_type=4, prompt='x',
                        images=['url'] * p['reference_images'])
            self.assertEqual(len(normalize_image_request(body)['images']), p['reference_images'])
            for images in ([], ['url'] * (p['reference_images'] + 1), ['']):
                with self.assertRaises(ValueError):
                    normalize_image_request(dict(body, images=images))
            for kind in p['modes']:
                valid = dict(body, generate_type=kind, prompt='x' * p['prompt_limits'][kind - 3])
                if kind == 3:
                    valid.pop('images')
                normalize_image_request(valid)
                with self.assertRaises(ValueError):
                    normalize_image_request(dict(valid, prompt=valid['prompt'] + 'x'))

    def test_invalid_requests_fail_before_network_or_balance(self):
        invalid = [dict(model_type=38, prompt='x'),
                   dict(model_type=174, prompt='x', generate_type=4),
                   dict(model_type=101, prompt='x', moition_range='1'),
                   dict(model_type=72, prompt='x', outputs=5),
                   dict(model_type=72, prompt='x', generate_type=0)]
        with patch.object(generate, 'http_request') as http, patch.object(generate, 'action_balance') as balance:
            for body in invalid:
                for call in [lambda: generate.action_price('/api/lumeflow/image-generate', body),
                             lambda: generate.action_generate('image-generate', body),
                             lambda: generate.action_generate_with_balance('image-generate', body),
                             lambda: generate.action_watch('image', body)]:
                    with self.assertRaises(ValueError):
                        call()
            http.assert_not_called()
            balance.assert_not_called()

    def test_image_upload_limits_and_local_catalog_cli(self):
        with patch('os.path.isfile', return_value=True), patch('os.path.getsize', return_value=6 * 1024 * 1024):
            for model in [101, 174, 175]:
                with self.assertRaises(ValueError):
                    generate.validate_upload_image('test.png', model=model, model_kind='image')
            generate.validate_upload_image('test.png', model='nanobanana2', model_kind='image')
        out = io.StringIO()
        with patch.object(sys, 'argv', ['generate.py', '--action', 'image-models', '--model', 'GPT Image 2.5 Sunburst']), contextlib.redirect_stdout(out), patch.object(generate, 'http_request') as http:
            generate.main()
            http.assert_not_called()
        self.assertEqual(json.loads(out.getvalue())['models'][0]['model_type'], 175)


if __name__ == '__main__':
    unittest.main()
