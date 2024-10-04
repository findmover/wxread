import pprint

import requests
import json

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ko;q=0.5",
    "baggage": "sentry-environment=production,sentry-release=dev-1727596539903,sentry-public_key=ed67ed71f7804a038e898ba54bd66e44,sentry-trace_id=b1368d5b893944dca7444ee29f874d4b",
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
    "sentry-trace": "b1368d5b893944dca7444ee29f874d4b-a674f5481b216fa4",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
}
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
    "wr_pf": "NaN"
}


def get_wr_skey():
    url = "https://weread.qq.com/web/login/renewal"
    data = {
        "rq": "%2Fweb%2Fbook%2Fread"
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    # print(response.text)
    cookie_str = response.headers['Set-Cookie']
    # print(cookie_str)
    wr_key = ""
    for cookie in cookie_str.split(';'):
        if cookie.__contains__("wr_skey"):
            wr_skey = cookie[-8:]
            print("数据初始化成功！")
            return wr_skey
