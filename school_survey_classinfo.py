import requests
import pandas as pd
import time

#获取token

corpid = 'guh3qh6VLMwyzq4j5jU3'

url = 'https://openplatform-api.xiaobao100.com/token/get_token'

json = {'accessKeyId': '606ff939c3d1c80001c69dcf',
'accessKeySecret': 'TVEL3YTZ3KkZRQ6BgT45ROOPoHmPEjZTq31w4zUJ',
'corpid': 'guh3qh6VLMwyzq4j5jU3'}

r = requests.request(method='POST', url=url, json=json)

print(r.text)


json = {'token': r.text,
'corpid': 'guh3qh6VLMwyzq4j5jU3',
'xb-timestamp':str(time.time()),
}
url = 'https://openplatform-api.xiaobao100.com/open-platform/Class/v2/GetAdministrativeClassList'
classinfo = requests.request(method='get', url=url, json=json)

print(classinfo.text)