# config.py 自定义配置,包括阅读次数、推送token的填写
import os
import re

"""
可修改区域
默认使用本地值如果不存在从环境变量中获取值
"""

# 阅读次数 默认120次/60分钟
READ_NUM = int(os.getenv('READ_NUM') or 120)
# 需要推送时可选，可选pushplus、wxpusher、telegram
PUSH_METHOD = "" or os.getenv('PUSH_METHOD')
# pushplus推送时需填
PUSHPLUS_TOKEN = "" or os.getenv("PUSHPLUS_TOKEN")
# telegram推送时需填
TELEGRAM_BOT_TOKEN = "" or os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = "" or os.getenv("TELEGRAM_CHAT_ID")
# wxpusher推送时需填
WXPUSHER_SPT = "" or os.getenv("WXPUSHER_SPT")
# read接口的bash命令，本地部署时可对应替换headers、cookies
curl_str = os.getenv('WXREAD_CURL_BASH')

# headers、cookies是一个省略模版，本地或者docker部署时对应替换
cookies = {
    'RK': '/U1VY/LPdb',
    'ptcz': 'feb3de917f87400787fbf5934e2b46b5466545f34bf8a5c7adbdc5bc8ab371ae',
    'wr_avatar': 'https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FQ0j4TwGTfTI51cu6AvvQV8cIicf5ezL7PjKjTdrgTss6icXBsJSibTykIkMTGQzI0QxHDKs4KbKOmrUxbjC9u9ZVQ%2F132',
    'wr_gender': '1',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'baggage': 'sentry-environment=production,sentry-release=dev-1743523268690,sentry-public_key=ed67ed71f7804a038e898ba54bd66e44,sentry-trace_id=f28b984c208449548d5d2b40dc3d3876',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36',
}


"""
建议保留区域|默认读三体，其它书籍自行测试时间是否增加
"""
dataArray = [{
    "appId": "wb182564874603h266381671",
    "b": "ce032b305a9bc1ce0b0dd2a",
    "c": "7f632b502707f6ffaa6bf2e",
    "ci": 27,
    "co": 389,
    "sm": "19聚会《三体》网友的聚会地点是一处僻静",
    "pr": 74,
    "rt": 15,
    "ts": 1744264311434,
    "rn": 466,
    "sg": "2b2ec618394b99deea35104168b86381da9f8946d4bc234e062fa320155409fb",
    "ct": 1744264311,
    "ps": "b1b32fa07a65893cg017095",
    "pc": "30732cc07a65893cg019b2f",
    "s": "36cc0815"
},{
    "appId": "wb182564874603h266381671",
    "b": "ce032b305a9bc1ce0b0dd2a",
    "c": "025324d028602522a2b2084",
    "ci": 49,
    "co": 381,
    "sm": "序章褐蚁已经忘记这里曾是它的家园。这段时",
    "pr": 74,
    "rt": 7,
    "ts": 1744276779146,
    "rn": 59,
    "sg": "06edab0b34eb67493117b85c22f77cb714ed4d2d637c19cff70d67910ed3fd63",
    "ct": 1744276779,
    "ps": "ef432ee07a658e13g01049f",
    "pc": "60532a107a658e13g01684b",
    "s": "75cf4dab"
},{
    "appId": "wb182564874603h266381671",
    "b": "55532930813ab9ce5g01675f",
    "c": "ecc32f3013eccbc87e4b62e",
    "ci": 3,
    "co": 354,
    "sm": "第1章　诡画我自幼生长在黄河边，天天守着",
    "pr": 0,
    "rt": 4,
    "ts": 1744276822574,
    "rn": 343,
    "sg": "36b3bd28fc2851a2b28ec2c0c0efea931b4c7fa9647aa20ebd27e405ffccfcf3",
    "ct": 1744276822,
    "ps": "79932d907a658e20g015ee4",
    "pc": "85e320007a658e21g015f26",
    "s": "89aa5fb9"
},{
    "appId": "wb182564874603h266381671",
    "b": "55532930813ab9ce5g01675f",
    "c": "3c5327902153c59dc0488e1",
    "ci": 21,
    "co": 354,
    "sm": "第19章　不祥预感情况是明摆着的，年轻人",
    "pr": 0,
    "rt": 24,
    "ts": 1744276853945,
    "rn": 8,
    "sg": "6d54f3592168ed3bff1a29a998ebf03b39d97ab7dfae7c86eba736e5d2ee9d04",
    "ct": 1744276853,
    "ps": "79932d907a658e20g015ee4",
    "pc": "85e320007a658e21g015f26",
    "s": "6b30162c"
},{
    "appId": "wb182564874603h266381671",
    "b": "b4132bb0719db176b41f10e",
    "c": "1ff325f02181ff1de7742fc",
    "ci": 8,
    "co": 358,
    "sm": "五七夕节：除了谈恋爱，你还应该知道啥？[",
    "pr": 43,
    "rt": 30,
    "ts": 1744278758874,
    "rn": 910,
    "sg": "d331a3ad0e446ed9dc04f483b66234e8e1eb7b5b565c144b7beb5611bfe30883",
    "ct": 1744278758,
    "ps": "41b324d07a658ee0g011e19",
    "pc": "6d032ec07a658ee0g012eee",
    "s": "a5bc9996"
},{
    "appId": "wb182564874603h266381671", 
    "b": "a44320e05d2407a44db0ca3", 
    "c": "ecc32f3013eccbc87e4b62e", 
    "ci": 3, 
    "co": 392, 
    "sm": "内容简介人生不能有遗憾，想去的地方一定要", 
    "pr": 0, 
    "rt": 10, 
    "ts": 1744279281444, 
    "rn": 776, 
    "sg": "abfe2104e5ae45e09b93e5943a416708e18d5faaa2100727e50c39fa932381ae", 
    "ct": 1744279281, 
    "ps": "5b232f507a658ef1g018663", 
    "pc": "a5432cb07a658ef2g012f51", 
    "s": "976b96bd"
},{
    "appId": "wb182564874603h266381671", 
    "b": "8c9327105e03d38c94541e7", 
    "c": "c4c329b011c4ca4238a0201", 
    "ci": 1, 
    "co": 10258, 
    "sm": "整体来说，很多精神失常的人比正常人要更加", 
    "pr": 0, 
    "rt": 4, 
    "ts": 1744279324912, 
    "rn": 587, 
    "sg": "4bd1ef0e33f1aa07f5d24ade34feae6ce0784545b8f0c94b77b53afd196e66f7", 
    "ct": 1744279324, 
    "ps": "0c0324707a658f1bg0132dc", 
    "pc": "d0832a607a658f1bg016c67", 
    "s": "59c50e4e"
}]


def convert(curl_command):
    """提取bash接口中的headers与cookies
    支持 -H 'Cookie: xxx' 和 -b 'xxx' 两种方式的cookie提取
    """
    # 提取 headers
    headers_temp = {}
    for match in re.findall(r"-H '([^:]+): ([^']+)'", curl_command):
        headers_temp[match[0]] = match[1]

    # 提取 cookies
    cookies = {}
    
    # 从 -H 'Cookie: xxx' 提取
    cookie_header = next((v for k, v in headers_temp.items() 
                         if k.lower() == 'cookie'), '')
    
    # 从 -b 'xxx' 提取
    cookie_b = re.search(r"-b '([^']+)'", curl_command)
    cookie_string = cookie_b.group(1) if cookie_b else cookie_header
    
    # 解析 cookie 字符串
    if cookie_string:
        for cookie in cookie_string.split('; '):
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                cookies[key.strip()] = value.strip()
    
    # 移除 headers 中的 Cookie/cookie
    headers = {k: v for k, v in headers_temp.items() 
              if k.lower() != 'cookie'}

    return headers, cookies


headers, cookies = convert(curl_str) if curl_str else (headers, cookies)
