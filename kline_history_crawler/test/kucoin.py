import requests

if __name__ == '__main__':
    # httpUrl = 'https://openapi-v2.kucoin.com/api/v1/currencies'
    httpUrl = 'https://www.google.com/'
    headers = {
        "Content-type": "application/json"
    }
    response = requests.get(httpUrl,headers=headers,timeout=100)
    print(response.content)