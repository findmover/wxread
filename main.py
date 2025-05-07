# main.py 主逻辑：包括字段拼接、模拟请求
import hashlib
import json
import logging
import random
import re
import time
import urllib.parse

import requests

# 配置日志格式
from loguru import logger  # 新增：导入 loguru 的 logger

from config import PUSH_METHOD, READ_NUM, book, chapter, cookies, data, headers
from push import push

# 加密盐及其它默认值
KEY = "3c5c8717f3daf09iop3423zafeqoi"
COOKIE_DATA = {"rq": "%2Fweb%2Fbook%2Fread"}
READ_URL = "https://weread.qq.com/web/book/read"
RENEW_URL = "https://weread.qq.com/web/login/renewal"
FIX_SYNCKEY_URL = "https://weread.qq.com/web/book/chapterInfos"


def encode_data(data):
    """数据编码"""
    return "&".join(
        f"{k}={urllib.parse.quote(str(data[k]), safe='')}" for k in sorted(data.keys())
    )


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


def get_wr_skey():
    """刷新cookie密钥"""
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


def fix_no_synckey():
    requests.post(
        FIX_SYNCKEY_URL,
        headers=headers,
        cookies=cookies,
        data=json.dumps({"bookIds": ["3300060341"]}, separators=(",", ":")),
    )


def refresh_cookie():
    logger.info(f"🍪 刷新cookie")  # 修改：使用 loguru 的 logger 替代 logging
    new_skey = get_wr_skey()
    if new_skey:
        cookies["wr_skey"] = new_skey
        logger.success(
            f"✅ 密钥刷新成功，新密钥：{new_skey}"
        )  # 修改：使用 loguru 的 logger 替代 logging
        logger.info(f"🔄 重新本次阅读。")  # 修改：使用 loguru 的 logger 替代 logging
    else:
        ERROR_CODE = "❌ 无法获取新密钥或者WXREAD_CURL_BASH配置有误，终止运行。"
        logger.error(ERROR_CODE)  # 修改：使用 loguru 的 logger 替代 logging
        push(ERROR_CODE, PUSH_METHOD)
        raise Exception(ERROR_CODE)


refresh_cookie()
index = 1
lastTime = int(time.time()) - 30
while index <= READ_NUM:
    data.pop("s")
    data["b"] = random.choice(book)
    data["c"] = random.choice(chapter)
    thisTime = int(time.time())
    data["ct"] = thisTime
    data["rt"] = thisTime - lastTime
    data["ts"] = int(thisTime * 1000) + random.randint(0, 1000)
    data["rn"] = random.randint(0, 1000)
    data["sg"] = hashlib.sha256(f"{data['ts']}{data['rn']}{KEY}".encode()).hexdigest()
    data["s"] = cal_hash(encode_data(data))

    logger.info(
        f"⏱️ 尝试第 {index} 次阅读..."
    )  # 修改：使用 loguru 的 logger 替代 logging
    logger.debug(f"📕 data: {data}")  # 修改：使用 loguru 的 logger 替代 logging
    response = requests.post(
        READ_URL,
        headers=headers,
        cookies=cookies,
        data=json.dumps(data, separators=(",", ":")),
    )
    resData = response.json()
    logger.debug(f"📕 response: {resData}")  # 修改：使用 loguru 的 logger 替代 logging

    if "succ" in resData:
        if "synckey" in resData:
            lastTime = thisTime
            index += 1
            time.sleep(30)
            logger.success(
                f"✅ 阅读成功，阅读进度：{(index - 1) * 0.5} 分钟"
            )  # 修改：使用 loguru 的 logger 替代 logging
        else:
            logger.warning(
                "❌ 无synckey, 尝试修复..."
            )  # 修改：使用 loguru 的 logger 替代 logging
            fix_no_synckey()
    else:
        logger.warning(
            "❌ cookie 已过期，尝试刷新..."
        )  # 修改：使用 loguru 的 logger 替代 logging
        refresh_cookie()

logger.info("🎉 阅读脚本已完成！")  # 修改：使用 loguru 的 logger 替代 logging
