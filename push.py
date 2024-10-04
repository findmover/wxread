import requests


def push(content):
    url = "https://www.pushplus.plus/send"
    params = {
        "token": "官网上去复制token",
        "content": content
    }
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
    }

    response = requests.get(url, headers=headers, params=params)
    print(response.text)


