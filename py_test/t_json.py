import requests
import urllib3
import json
url = "http://127.0.0.3:1180/balance/get"
payload = json.dumps({
  "username": "h19999",
  "password": "123456"
})
headers = {
  'Content-Type': 'application/json'   
}
response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)

import json
data = { '李四' : 1, '掌声' : 2, '王五' : '\?', 'd' : 4, 'e' : 5 }
jd=json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
print(json.dumps(jd,ensure_ascii=False,encoding='utf-8'))
js = '{"a":1,"%":2,"c":3,"d":4,"e":5}'
print(json.loads(js))
