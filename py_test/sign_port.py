#!/usr/bin/env python3
# coding=utf-8
# 按日期 提取 指定码号 签名 数量

from glob import glob
from collections import defaultdict

channel = {'1052','1142','1172','1169','1173','1174','1175','1194','1182','1195','1208','1217','1177','1210','1212','1998','1205','1206','1186','1191','1192','1207','1222','1995','1993','1269','1241','1235','1259','1260','1261','1263','1249','1253','1258','1268','1310','1312','1313','1314','1294','1301','1303','1309','1318','1315'}
ec = set()
port = set()
ec_dict = dict()
src_path = '/share/B/sms_mr'

def getFileList(src_path: str, file_prefix: str, datestr: list) -> list:
    srcFiles = []
    for dt in datestr:
        p_mode = '{}/{}.{}'.format(src_path, file_prefix, dt)
        print(p_mode)
        srcFiles.extend(glob(p_mode))
    return sorted(srcFiles)
# 得到源文件列表
#srcfiles = getFileList('/share/B/sms_mr', 'mr.log', ['2022051[3-8]*.cmpp*'])
srcfiles = getFileList('/share/B/sms_mr', 'mr.log', ['2022051301*.cmpp*'])
# 循环处理文件 签名计数
for s_file in srcfiles:
    with open(s_file, 'r') as fp_src:
        print(s_file)
        for line in fp_src:
            row = line.rstrip().split(',')
            if row[0] in channel and row[4] == '0' and row[9] == '1' :
                #"ec":{【xxx】:{"10680739,102939303",xxx,xx}}
                sign_key = ec_dict.get(row[3], None)
                if sign_key is None:
                    ec_port = {'{},{}'.format(row[16],row[17])}
                    ec_dict[row[3]] = {row[26]:ec_port}
                else : 
                    s_key = sign_key.get(row[26],None)
                    if s_key is None:
                        sign_key[row[26]] = {'{},{}'.format(row[16],row[17])}
                    else :
                        if len(s_key) <= 10 :
                            s_key.add('{},{}'.format(row[16],row[17]))

ec_f = dict()
for e in ec_dict.keys():
    ec_f[e] = open('{}.txt'.format(e), 'w')

# 写文件
for ec_key in ec_dict.keys():
    for zsign , zport in ec_dict[ec_key].items():
        for s in zport:
            ec_f[ec_key].write('{},{}\n'.format(zsign , s))

for e in ec_dict.keys():
    ec_f[e].close()