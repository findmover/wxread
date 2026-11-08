import unittest
from unittest.mock import Mock, patch
import requests
import push


class BarkTests(unittest.TestCase):
    def setUp(self):
        self.notifier = push.PushNotification()

    def test_payload_and_dispatch(self):
        response = Mock()
        response.json.return_value = {'code': 200}
        with patch.object(push, 'BARK_DEVICE_KEY', 'test-device'), patch.object(push.requests, 'post', return_value=response) as post:
            self.assertTrue(push.push('完成次数：40/40', 'bark', is_success=False))
            args, kwargs = post.call_args
            self.assertNotIn('test-device', args[0])
            self.assertEqual(kwargs['json']['device_key'], 'test-device')
            self.assertEqual(kwargs['json']['title'], '微信读书-失败')
            self.assertEqual(kwargs['json']['body'], '完成次数：40/40')
            self.assertEqual(kwargs['json']['group'], 'wxread')

    def test_missing_key_never_sends(self):
        with patch.object(push.requests, 'post') as post:
            self.assertFalse(self.notifier.push_bark('result', '', True))
            post.assert_not_called()

    def test_rejected_business_code_is_failure(self):
        response = Mock()
        response.json.return_value = {'code': 400}
        with patch.object(push.requests, 'post', return_value=response) as post:
            self.assertFalse(self.notifier.push_bark('result', 'test', True))
            self.assertEqual(post.call_count, 1)

    def test_transient_network_failure_retries(self):
        response = Mock()
        response.json.return_value = {'code': 200}
        with patch.object(push.requests, 'post', side_effect=[requests.Timeout('timeout'), response]) as post, patch.object(push.time, 'sleep') as sleep:
            self.assertTrue(self.notifier.push_bark('result', 'test', True))
            self.assertEqual(post.call_count, 2)
            sleep.assert_called_once_with(1)

    def test_bad_json_exhausts_retries(self):
        response = Mock()
        response.json.side_effect = ValueError('invalid JSON')
        with patch.object(push.requests, 'post', return_value=response) as post, patch.object(push.time, 'sleep'):
            self.assertFalse(self.notifier.push_bark('result', 'test', True))
            self.assertEqual(post.call_count, 3)

    def test_custom_server_and_level(self):
        with patch.object(push, 'BARK_SERVER_URL', 'https://bark.example/'), patch.object(push, 'BARK_LEVEL', 'passive'), patch.object(push.requests, 'post') as post:
            post.return_value.json.return_value = {'code': 200}
            self.assertTrue(push.PushNotification().push_bark('result', 'test', True))
            self.assertEqual(post.call_args.args[0], 'https://bark.example/push')
            self.assertEqual(post.call_args.kwargs['json']['level'], 'passive')


if __name__ == '__main__':
    unittest.main()
