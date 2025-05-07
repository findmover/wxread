import asyncio
import hashlib
import json
import random
import re
import time
import urllib.parse
from typing import Callable

import requests
from loguru import logger


class WXReader:
    """微信读书SDK"""

    def __init__(
        self,
        headers: dict,
        cookies: dict,
        book: list = None,
        chapter: list = None,
        payload: dict = None,
    ):
        self.cookies: dict = cookies
        self.headers: dict = headers
        data = {
            "appId": "wb182564874663h152492176",
            "b": "ce032b305a9bc1ce0b0dd2a",
            "c": "7cb321502467cbbc409e62d",
            "ci": 70,
            "co": 0,
            "sm": "[插图]第三部广播纪元7年，程心艾AA说",
            "pr": 74,
            "rt": 30,
            "ps": "b1d32a307a4c3259g016b67",
            "pc": "080327b07a4c3259g018787",
        }
        self.book = book or [
            "36d322f07186022636daa5e",
            "6f932ec05dd9eb6f96f14b9",
            "43f3229071984b9343f04a4",
            "d7732ea0813ab7d58g0184b8",
            "3d03298058a9443d052d409",
            "4fc328a0729350754fc56d4",
            "a743220058a92aa746632c0",
            "140329d0716ce81f140468e",
            "1d9321c0718ff5e11d9afe8",
            "ff132750727dc0f6ff1f7b5",
            "e8532a40719c4eb7e851cbe",
            "9b13257072562b5c9b1c8d6",
        ]
        self.chapter = chapter or [
            "ecc32f3013eccbc87e4b62e",
            "a87322c014a87ff679a21ea",
            "e4d32d5015e4da3b7fbb1fa",
            "16732dc0161679091c5aeb1",
            "8f132430178f14e45fce0f7",
            "c9f326d018c9f0f895fb5e4",
            "45c322601945c48cce2e120",
            "d3d322001ad3d9446802347",
            "65132ca01b6512bd43d90e3",
            "c20321001cc20ad4d76f5ae",
            "c51323901dc51ce410c121b",
            "aab325601eaab3238922e53",
            "9bf32f301f9bf31c7ff0a60",
            "c7432af0210c74d97b01b1c",
            "70e32fb021170efdf2eca12",
            "6f4322302126f4922f45dec",
        ]
        self.payload: dict = payload or data

    @staticmethod
    def encode_data(data):
        """数据编码"""
        return "&".join(
            f"{k}={urllib.parse.quote(str(data[k]), safe='')}"
            for k in sorted(data.keys())
        )

    def _fix_no_synckey(self):
        """修复无 synckey 的情况"""
        FIX_SYNCKEY_URL = "https://weread.qq.com/web/book/chapterInfos"
        requests.post(
            FIX_SYNCKEY_URL,
            headers=self.headers,
            cookies=self.cookies,
            data=json.dumps({"bookIds": ["3300060341"]}, separators=(",", ":")),
        )

    @staticmethod
    def cal_hash(input_string):
        """计算哈希值"""
        _7032f5 = 0x15051505
        _cc1055 = _7032f5
        length = len(input_string)
        _19094e = length - 1

        while _19094e > 0:
            _7032f5 = 0x7FFFFFFF & (
                _7032f5 ^ ord(input_string[_19094e]) << (length - _19094e) % 30
            )
            _cc1055 = 0x7FFFFFFF & (
                _cc1055 ^ ord(input_string[_19094e - 1]) << _19094e % 30
            )
            _19094e -= 2

        return hex(_7032f5 + _cc1055)[2:].lower()

    @staticmethod
    def _get_wr_skey(headers, cookies):
        """刷新cookie密钥"""
        RENEW_URL = "https://weread.qq.com/web/login/renewal"
        COOKIE_DATA = {"rq": "%2Fweb%2Fbook%2Fread"}
        response = requests.post(
            RENEW_URL,
            headers=headers,
            cookies=cookies,
            data=json.dumps(COOKIE_DATA, separators=(",", ":")),
        )
        for cookie in response.headers.get("Set-Cookie", "").split(";"):
            if "wr_skey" in cookie:
                return cookie.split("=")[-1][:8]
        return None

    def refresh_cookie(self):
        """
        刷新cookie密钥
        """
        new_skey = self._get_wr_skey(self.headers, self.cookies)
        logger.info(f"刷新wr_skey: {self.cookies['wr_skey']}")
        if new_skey:
            self.cookies.update(wr_skey=new_skey)
            logger.info(f"刷新wr_skey成功: {self.cookies['wr_skey']}")
            return True
        return False

    def _prepare_payload(self, lastTime: int):
        """准备请求负载"""
        KEY = "3c5c8717f3daf09iop3423zafeqoi"
        b = random.choice(self.book)
        c = random.choice(self.chapter)
        ct = int(time.time())
        rt = ct - lastTime
        ts = int(ct * 1000) + random.randint(0, 1000)
        rn = random.randint(0, 1000)
        sg = hashlib.sha256(f"{ts}{rn}{KEY}".encode()).hexdigest()
        self.payload.update(
            {
                "b": b,
                "c": c,
                "ct": ct,
                "rt": rt,
                "ts": ts,
                "rn": rn,
                "sg": sg,
            }
        )

    def read(self, lastTime: int) -> dict:
        """阅读接口"""
        READ_URL = "https://weread.qq.com/web/book/read"

        self._prepare_payload(lastTime)
        s = self.cal_hash(self.encode_data(self.payload))
        response = requests.post(
            READ_URL,
            headers=self.headers,
            cookies=self.cookies,
            data=json.dumps({**self.payload, "s": s}, separators=(",", ":")),
        )
        return response.json()

    @staticmethod
    def parse_curl(curl_cmd):
        """
        解析 curl 命令，提取 headers、cookies 和 payload 并转换为字典。
        """
        headers = {}
        cookies = {}
        payload = {}

        header_pattern = r"-H \'(.*?): (.*?)\'"
        header_matches = re.findall(header_pattern, curl_cmd)
        for key, value in header_matches:
            headers[key] = value

        cookie_pattern = r"-b \'(.*?)\'"
        cookie_match = re.search(cookie_pattern, curl_cmd)
        if cookie_match:
            cookie_str = cookie_match.group(1)
            cookie_pairs = cookie_str.split("; ")
            for pair in cookie_pairs:
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    cookies[key] = value

        payload_pattern = r"--data-raw \'(.*?)\'"
        payload_match = re.search(payload_pattern, curl_cmd)
        if payload_match:
            payload_str = payload_match.group(1)
            try:
                payload = json.loads(payload_str)
            except json.JSONDecodeError:
                raise ValueError("Could not parse payload as JSON.")
        # 移除 s 参数，避免后续操做要每次移除
        payload.pop("s", None)
        return {"headers": headers, "cookies": cookies, "payload": payload}

    @classmethod
    def from_curl_bash(cls, bash_path: str):
        """
        从curl中提取 headers、cookies 和 payload，然后创建实例，
        """
        with open(bash_path, "r", encoding="utf8") as f:
            curl_command = f.read()
        config = cls.parse_curl(curl_command)
        return cls(**config)  # type: ignore

    async def sync_run(
        self,
        loop_num: int = 5,
        onStart: Callable = logger.info,
        onSuccess: Callable = logger.success,
        onDebug: Callable = logger.debug,
        onFail: Callable = logger.error,
        onFinish: Callable = logger.info,
    ):
        RESIDENCE: int = 30
        self.refresh_cookie()
        index = 1
        lastTime = int(time.time()) - RESIDENCE
        while index <= loop_num:
            onStart(f"⏱️ 尝试第 {index}/{loop_num} 次阅读...")
            resData: dict = self.read(lastTime)
            if "succ" in resData:
                if "synckey" in resData:
                    lastTime: int = self.payload["ct"]
                    index += 1

                    await asyncio.sleep(RESIDENCE)
                    onSuccess(
                        f"✅ 阅读成功，阅读进度：{(index - 1) * (RESIDENCE / 60)} 分钟"
                    )
                else:
                    onDebug("❌ 无 synckey，尝试修复...")
                    self._fix_no_synckey()
            else:
                logger.warning("❌ cookie 已过期，尝试刷新...")
                if self.refresh_cookie():
                    onSuccess("🔄 重新本次阅读。")
                    continue
                else:
                    msg = "❌ 无法获取新密钥或者WXREAD_CURL_BASH配置有误，终止运行。"
                    onFail(msg)
                    raise Exception(msg)
        onFinish(f"🎉 阅读脚本已完成！成功阅读 {loop_num*(RESIDENCE / 60)} 分钟")


if __name__ == "__main__":
    reader = WXReader.from_curl_bash("./curl.sh")
    asyncio.run(reader.sync_run(loop_num=120))
