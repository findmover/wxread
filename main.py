# -------------------request-1-----------------------------
# {
#     "appId": "wb182564874663h152492176",
#     "b": "ce032b305a9bc1ce0b0dd2a",
#     "c": "0723244023c072b030ba601",
#     "ci": 60,
#     "co": 336,
#     "sm": "[插图]威慑纪元61年，执剑人在一棵巨树",
#     "pr": 65,
#     "rt": 30,
#     "ts": 1727580275610,
#     "rn": 869,
#     "sg": "aefc57298e0796865d8609165c28958696779eda3649720bf0c55a9687ce247d",
#     "ct": 1727580275,
#     "ps": "48d32f007a4c133dg011052",
#     "pc": "f69321d07a4c133dg01256e",
#     "s": "93912b18"
# }
import random

# -------------------request-2-----------------------------
# {
#     "appId": "wb182564874663h152492176", ✔
#     "b": "ce032b305a9bc1ce0b0dd2a",  ✔
#     "c": "0723244023c072b030ba601", ✔
#     "ci": 60, ✔
#     "co": 336, ✔
#     "sm": "[插图]威慑纪元61年，执剑人在一棵巨树", ✔
#     "pr": 65,    ✔
#     "rt": 88,    ✔
#     "ts": 1727580815581, ✔
#     "rn": 114,
#     "sg": "bfdf7de2fe1673546ca079e2f02b79b937901ef789ed5ae16e7b43fb9e22e724",
#     "ct": 1727580815, ✔
#     "ps": "48d32f007a4c133dg011052", ✔
#     "pc": "f69321d07a4c133dg01256e", ✔
#     "s": "fadcb9de"
# }

import requests
import json
import time
import hashlib
import urllib.parse
from cookie import get_wr_skey
from push import push


def encode_data(data, keys_to_include=None):
    sorted_keys = sorted(data.keys())
    query_string = ''

    for key in sorted_keys:
        if keys_to_include is None or key in keys_to_include:
            value = data[key]
            encoded_value = urllib.parse.quote(str(value), safe='')
            query_string += f'{key}={encoded_value}&'

    if query_string.endswith('&'):
        query_string = query_string[:-1]

    return query_string


def cal_hash(input_string):
    _7032f5 = 0x15051505
    _cc1055 = _7032f5
    length = len(input_string)
    _19094e = length - 1

    while _19094e > 0:
        _7032f5 = 0x7fffffff & (_7032f5 ^ ord(input_string[_19094e]) << (length - _19094e) % 30)
        _cc1055 = 0x7fffffff & (_cc1055 ^ ord(input_string[_19094e - 1]) << _19094e % 30)
        _19094e -= 2

    return hex(_7032f5 + _cc1055)[2:].lower()


headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ko;q=0.5",
    "baggage": "sentry-environment=production,sentry-release=dev-1727596539903,sentry-public_key=ed67ed71f7804a038e898ba54bd66e44,sentry-trace_id=d3cc3a94f5244647b8064ecd77eb8ba6",
    "cache-control": "no-cache",
    "content-type": "application/json;charset=UTF-8",
    "dnt": "1",
    "origin": "https://weread.qq.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://weread.qq.com/web/reader/ce032b305a9bc1ce0b0dd2akd2d32c50249d2ddea18fb39",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sentry-trace": "d3cc3a94f5244647b8064ecd77eb8ba6-93b39e13fa4e5fd6",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
}
# 会话密钥

cookies = {
    "RK": "oxEY1bTnXf",
    "ptcz": "53e3b35a9486dd63c4d06430b05aa169402117fc407dc5cc9329b41e59f62e2b",
    "pac_uid": "0_e63870bcecc18",
    "iip": "0",
    "_qimei_uuid42": "183070d3135100ee797b08bc922054dc3062834291",
    "_qimei_fingerprint": "28ec521da86d1fbc149479d2aa40f951",
    "_qimei_q36": "",
    "_qimei_h38": "cb6de4e4797b08bc922054dc02000005818307",
    "pgv_pvid": "1212703189",
    "fqm_pvqid": "50bb40ea-985c-4d11-9cea-7dfefe6ea1ca",
    "_clck": "15sxecs|1|fl1|0",
    "qq_domain_video_guid_verify": "004329d456c0ef18",
    "wr_vid": "346607432",
    "wr_localvid": "6a8327b0814a8cf486a8884",
    "wr_name": "%E6%9C%AC%20%E6%97%A0%20%E9%81%93",
    "wr_gender": "1",
    "wr_rt": "web%40dz_AYa7CIYk07_ucDIb_AL",
    "wr_avatar": "https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FMCpyjIyiaHicBXjh38REzNMA1xXiaeoWJ321CicmRcyMzeSibgDp1z6XC1FVr4szNr4PUsfIqEPRNXa4l9h2NGQsZDg%2F132",
    "wr_fp": "1659424119",
    "wr_pf": "NaN",
    "wr_skey": "ivnZkd2_"
}
url = "https://weread.qq.com/web/book/read"

data = {
    "appId": "wb182564874663h152492176",
    "b": "ce032b305a9bc1ce0b0dd2a",
    "c": "7cb321502467cbbc409e62d",
    "ci": 70,
    "co": 0,
    "sm": "[插图]第三部广播纪元7年，程心艾AA说",
    "pr": 74,
    "rt": 30,
    "ts": 1727660516749,
    "rn": 31,
    "sg": "991118cc229871a5442993ecb08b5d2844d7f001dbad9a9bc7b2ecf73dc8db7e",
    "ct": 1727660516,
    "ps": "b1d32a307a4c3259g016b67",
    "pc": "080327b07a4c3259g018787",
}
# 加密盐
key = "3c5c8717f3daf09iop3423zafeqoi"
num = 1

while True:
    # 处理数据
    print(f"-------------------第{num}次，共阅读{num * 0.5}分钟-------------------")
    data['ct'] = int(time.time())
    data['ts'] = int(time.time() * 1000)
    data['rn'] = random.randint(0, 1000)  # 1000以内的随机整数值
    data['sg'] = hashlib.sha256(("" + str(data['ts']) + str(data['rn']) + key).encode()).hexdigest()
    print(f"sg:{data['sg']}")
    data['s'] = cal_hash(encode_data(data))
    print(f"s:{data['s']}")

    sendData = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, data=sendData)
    resData = response.json()
    print(response.json())



    if 'succ' in resData:
        print("数据格式正确，阅读进度有效！")
        # 确认无s字段
        num += 1
        time.sleep(30)
    else:
        print("数据格式问题,尝试初始化cookie值")
        cookies['wr_skey'] = get_wr_skey()
        num -= 1

    if num == 200:
        print("阅读脚本运行已完成！")
        push("阅读脚本运行已完成！")
        break

    data.pop('s')
