import contextlib
import io
import logging
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
with patch('logging.FileHandler', return_value=logging.NullHandler()):
    import generate
import task_store


class WatchOutputTests(unittest.TestCase):
    def run_watch(self, responses, debug=False, timeout=600):
        self.clock = 0
        def sleep(seconds):
            self.clock += seconds
        body = dict(generate_type=3, model_type=72, prompt='full prompt ' * 300,
                    ratio='auto', resolution='1K', outputs=1)
        stderr = io.StringIO()
        with tempfile.TemporaryDirectory() as tmp, \
                patch.object(task_store, 'TASK_STORE_PATH', Path(tmp) / 'tasks.json'), \
                patch.object(generate, 'action_generate_with_balance', return_value={
                    'code': 200, 'data': [123], 'integral_used': 10,
                    'integral_remaining': 90}) as submit, \
                patch.object(generate, 'action_query', side_effect=responses), \
                patch.object(generate.time, 'time', side_effect=lambda: self.clock), \
                patch.object(generate.time, 'sleep', side_effect=sleep), \
                contextlib.redirect_stderr(stderr):
            result = generate.action_watch('image', body, poll_timeout=timeout, debug=debug)
            stored = task_store.get_task(result['local_id'])
            submit.assert_called_once()
        return result, stored, stderr.getvalue(), body

    def test_completed_result_is_quiet_and_request_stays_in_store(self):
        pending = {'data': [{'id': 123, 'status': 0, 'prompt': 'x' * 20000}]}
        done = {'data': [{'id': 123, 'status': 1, 'images': [
            {'origin_thumbnail': 'https://example.com/result.png'}]}]}
        result, stored, stderr, body = self.run_watch([pending, pending, done])
        self.assertEqual(result['status'], 'completed')
        self.assertEqual(result['result_urls'], ['https://example.com/result.png'])
        self.assertEqual(result['integral_remaining'], 90)
        self.assertEqual(stderr, '')
        self.assertNotIn('prompt', result)
        self.assertNotIn('body', result)
        self.assertNotIn('raw_query_response', result)
        self.assertEqual(stored['body']['prompt'], body['prompt'])
        self.assertEqual(stored['status'], 'completed')

    def test_debug_retains_diagnostics(self):
        response = {'data': [{'id': 123, 'status': 1, 'image': 'https://example.com/x.png'}]}
        result, _, stderr, body = self.run_watch([response], debug=True)
        self.assertIn('raw response', stderr)
        self.assertEqual(result['raw_query_response'], response)
        self.assertEqual(result['body']['prompt'], body['prompt'])

    def test_failed_result_keeps_error_code_and_reason(self):
        result, stored, stderr, _ = self.run_watch([
            {'data': [{'id': 123, 'status': 3, 'error_code': 2002, 'reason': 'review'}]}])
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['error_code'], 2002)
        self.assertIn('review', result['error'])
        self.assertEqual(stored['status'], 'failed')
        self.assertEqual(stderr, '')

    def test_timeout_keeps_ids_without_resubmitting(self):
        result, stored, stderr, _ = self.run_watch([
            {'data': [{'id': 123, 'status': 0}]}], timeout=8)
        self.assertEqual(result['status'], 'processing')
        self.assertEqual(result['task_ids'], [123])
        self.assertEqual(stored['status'], 'processing')
        self.assertNotIn('raw_query_response', result)
        self.assertEqual(stderr, '')

    def test_missing_url_preserves_recovery_response(self):
        response = {'data': [{'id': 123, 'status': 1, 'unusual_result': 'recoverable'}]}
        result, _, _, _ = self.run_watch([response])
        self.assertEqual(result['status'], 'completed')
        self.assertEqual(result['raw_query_response'], response)
        self.assertNotIn('body', result)


if __name__ == '__main__':
    unittest.main()
