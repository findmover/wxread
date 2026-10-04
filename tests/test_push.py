"""Offline push regressions. Run: python -m unittest discover -s tests -v."""
import json
import unittest
from unittest.mock import call, patch

import requests

# Import only the notification module; main performs reading at import time.
import push


SECRET = "credential-must-not-appear"
CONTENT = "private-notification-content"
CHAT = "private-chat-id"
LEAK = f"https://example.invalid/{SECRET}/{CONTENT}/{CHAT} raw-provider-body"
CHANNELS = {
    "pushplus": ("code", 200, "post"),
    "wxpusher": ("code", 1000, "get"),
    "serverchan": ("code", 0, "post"),
    "telegram": ("ok", True, "post"),
}


def response(body=None, status=200, raw=None):
    """Real requests status handling and JSON decoder, never a live request."""
    result = requests.Response()
    result.status_code = status
    result.url = LEAK
    result.reason = LEAK
    result.encoding = "utf-8"
    result._content = (raw if raw is not None else json.dumps(body)).encode("utf-8")
    return result


class PushTests(unittest.TestCase):
    def setUp(self):
        # Both verbs and every wait are mocked for every test, including failures.
        self.post = self.start_patch("push.requests.post")
        self.get = self.start_patch("push.requests.get")
        self.sleep = self.start_patch("push.time.sleep")
        self.randint = self.start_patch("push.random.randint", return_value=180)
        self.notifier = push.PushNotification()
        self.notifier.proxies = {"http": "http://proxy.invalid", "https": None}

    def start_patch(self, target, **kwargs):
        patcher = patch(target, **kwargs)
        mock = patcher.start()
        self.addCleanup(patcher.stop)
        return mock

    def reset_mocks(self):
        for mock in (self.post, self.get, self.sleep, self.randint):
            mock.reset_mock(return_value=True, side_effect=True)
        self.randint.return_value = 180

    def send(self, channel):
        if channel == "pushplus":
            return self.notifier.push_pushplus(CONTENT, SECRET, False)
        if channel == "wxpusher":
            return self.notifier.push_wxpusher(CONTENT, SECRET)
        if channel == "serverchan":
            return self.notifier.push_serverChan(CONTENT, SECRET, False)
        return self.notifier.push_telegram(CONTENT, SECRET, CHAT)

    def assert_redacted(self, logs):
        text = "\n".join(logs.output)
        for forbidden in (SECRET, CONTENT, CHAT, LEAK, "https://", "raw-provider-body"):
            self.assertNotIn(forbidden, text)
        for record in logs.records:
            self.assertIsNone(record.exc_info)

    def assert_attempts(self, channel, count):
        verb = CHANNELS[channel][2]
        transport = self.get if verb == "get" else self.post
        other = self.post if verb == "get" else self.get
        self.assertEqual(transport.call_count, count)
        other.assert_not_called()
        if channel == "telegram":
            self.sleep.assert_not_called()
            self.randint.assert_not_called()
            self.assertEqual(transport.call_args_list[0], call(
                self.notifier.telegram_url.format(SECRET),
                json={"chat_id": CHAT, "text": CONTENT},
                proxies=self.notifier.proxies, timeout=30))
            if count == 2:
                self.assertEqual(transport.call_args_list[1], call(
                    self.notifier.telegram_url.format(SECRET),
                    json={"chat_id": CHAT, "text": CONTENT}, timeout=30))
        else:
            self.assertEqual(self.randint.call_args_list, [call(180, 360)] * (count - 1))
            self.assertEqual(self.sleep.call_args_list, [call(180)] * (count - 1))

    def test_success_and_current_transport(self):
        for channel, (field, code, verb) in CHANNELS.items():
            with self.subTest(channel=channel):
                self.reset_mocks()
                transport = self.get if verb == "get" else self.post
                transport.return_value = response({field: code, "message": LEAK})
                with self.assertLogs(push.logger, level="INFO") as logs:
                    self.assertIs(self.send(channel), True)
                self.assert_redacted(logs)
                self.assert_attempts(channel, 1)
                if channel == "wxpusher":
                    # Deliberately retain upstream GET; POST is a separate PR.
                    self.get.assert_called_once_with(
                        self.notifier.wxpusher_simple_url.format(SECRET, CONTENT), timeout=10)
                elif channel in ("pushplus", "serverchan"):
                    args, kwargs = self.post.call_args
                    self.assertEqual(kwargs["timeout"], 10)
                    self.assertEqual(kwargs["headers"], self.notifier.headers)
                    payload = json.loads(kwargs["data"].decode("utf-8"))
                    self.assertEqual(payload["title"], "微信阅读-失败")
                    if channel == "pushplus":
                        self.assertEqual(args, (self.notifier.pushplus_url,))
                        self.assertEqual(payload, {"token": SECRET, "title": "微信阅读-失败", "content": CONTENT})
                    else:
                        self.assertEqual(args, (self.notifier.server_chan_url.format(SECRET),))
                        self.assertEqual(payload, {"title": "微信阅读-失败", "desp": CONTENT})

    def test_rejections_exhaust_policy_and_redact(self):
        for channel, (field, code, verb) in CHANNELS.items():
            invalid = [
                {field: -1, "message": LEAK}, {}, {field: None},
                {field: str(code)}, {field: False}, {field: 1},
                {field: float(code)}, [], None, LEAK,
            ]
            # Telegram must require literal True, not integer or string truthiness.
            cases = [("business", response(body)) for body in invalid]
            cases += [(f"http-{status}", response({field: code}, status))
                      for status in (400, 401, 429, 500, 503)]
            cases += [("invalid-json", response(raw=LEAK)),
                      ("transport", requests.exceptions.ConnectionError(LEAK)),
                      ("timeout", requests.exceptions.Timeout(LEAK))]
            for label, outcome in cases:
                with self.subTest(channel=channel, case=label, outcome=str(outcome)):
                    self.reset_mocks()
                    transport = self.get if verb == "get" else self.post
                    if isinstance(outcome, Exception):
                        transport.side_effect = outcome
                    else:
                        transport.return_value = outcome
                    with self.assertLogs(push.logger, level="INFO") as logs:
                        self.assertIs(self.send(channel), False)
                    self.assert_redacted(logs)
                    self.assert_attempts(channel, 2 if channel == "telegram" else 5)

    def test_recovery_stops_retries_and_telegram_fallback_validates(self):
        for channel, (field, code, verb) in CHANNELS.items():
            for failure in (response({field: -1, "message": LEAK}),
                            response({field: code}, 503),
                            response(raw=LEAK), requests.exceptions.Timeout(LEAK)):
                with self.subTest(channel=channel, failure=str(failure)):
                    self.reset_mocks()
                    transport = self.get if verb == "get" else self.post
                    transport.side_effect = [failure, response({field: code, "message": LEAK})]
                    with self.assertLogs(push.logger, level="INFO") as logs:
                        self.assertIs(self.send(channel), True)
                    self.assert_redacted(logs)
                    self.assert_attempts(channel, 2)

    def test_retry_delay_keeps_both_random_bounds(self):
        for channel in ("pushplus", "wxpusher", "serverchan"):
            with self.subTest(channel=channel):
                self.reset_mocks()
                self.randint.side_effect = [180, 360, 181, 359]
                transport = self.get if channel == "wxpusher" else self.post
                transport.return_value = response({"code": -1})
                with self.assertLogs(push.logger, level="INFO"):
                    self.assertIs(self.send(channel), False)
                self.assertEqual(transport.call_count, 5)
                self.assertEqual(self.randint.call_args_list, [call(180, 360)] * 4)
                self.assertEqual(self.sleep.call_args_list, [call(x) for x in (180, 360, 181, 359)])

    def test_missing_credentials_skip_network(self):
        for empty in (None, ""):
            cases = [
                (self.notifier.push_pushplus, (CONTENT, empty, True)),
                (self.notifier.push_wxpusher, (CONTENT, empty)),
                (self.notifier.push_serverChan, (CONTENT, empty, True)),
                (self.notifier.push_telegram, (CONTENT, empty, CHAT)),
                (self.notifier.push_telegram, (CONTENT, SECRET, empty)),
            ]
            for method, args in cases:
                with self.subTest(method=method.__name__, empty=empty):
                    with self.assertLogs(push.logger, level="WARNING") as logs:
                        self.assertIs(method(*args), False)
                    self.assert_redacted(logs)
        self.post.assert_not_called()
        self.get.assert_not_called()
        self.sleep.assert_not_called()
        self.randint.assert_not_called()

    def test_dispatch_and_unknown_channel_redaction(self):
        for channel, method, credentials in (
            ("pushplus", "push_pushplus", (SECRET, False)),
            ("wxpusher", "push_wxpusher", (SECRET,)),
            ("serverchan", "push_serverChan", (SECRET, False)),
            ("telegram", "push_telegram", (SECRET, CHAT)),
        ):
            with self.subTest(channel=channel), patch.multiple(
                push, PUSHPLUS_TOKEN=SECRET, WXPUSHER_SPT=SECRET,
                SERVERCHAN_SPT=SECRET, TELEGRAM_BOT_TOKEN=SECRET, TELEGRAM_CHAT_ID=CHAT
            ), patch.object(push.PushNotification, method, return_value=True) as sender:
                self.assertIs(push.push(CONTENT, channel.upper(), False), True)
                sender.assert_called_once_with(CONTENT, *credentials)
        for method in (None, "", LEAK):
            with self.assertLogs(push.logger, level="WARNING") as logs:
                self.assertIs(push.push(CONTENT, method), False)
            self.assert_redacted(logs)
        self.post.assert_not_called()
        self.get.assert_not_called()


if __name__ == "__main__":
    unittest.main()
