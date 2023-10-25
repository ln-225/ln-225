#Py匹配IP正则
import re
from typing import Pattern
# pattern=re.compile('([0-9]{1,})(\.[0-9]{1,}){3}')
# str=['192.168.211.221','11.11.11.11','11.152.156.153','11.11.156.253','12345695841','96.256.153.153','1.123.123.123']
# for i in str:
#     print(pattern.search(i))

import re
pattern = re.compile('[^市]')
str = ['杭州市','重庆','重庆','六盘水市','重庆']
for i in str:
    print(pattern.search(i))

