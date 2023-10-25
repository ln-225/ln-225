#!/usr/bin/env python3
# coding=utf-8

from asyncio import LimitOverrunError
import csv
import openpyxl
import datetime
from glob import glob
from collections import defaultdict,namedtuple

#sr_f = '/share/tmp/zengq/file_compare/test/dawei.xlsx'
sr_f = 'C:/Users/Z_Q/Downloads/dawei.xlsx'

def getFileList(src_path: str, file_prefix: str, datestr: list) -> list:
    srcFiles = []
    for dt in datestr:
        p_mode = '{}/{}.{}'.format(src_path, file_prefix, dt)
        srcFiles.extend(glob(p_mode))
    return sorted(srcFiles)

# def gettimestamp(time : str):
#     timestamp = []
#     t = datetime.datetime.strptime('{}'.format(time),'%Y%m%d')
#     for i in range(4):
#         obj_time = (t + datetime.timedelta(days = -i)).strftime("%Y%m%d")
#         timestamp.append(obj_time)
#     return timestamp

subports_tel = dict()
excel = openpyxl.load_workbook('{}'.format(sr_f))  # 有路径应带上路径
# 使用指定工作表
sheet = excel.active
#从第二行，第一列开始遍历读取所需的表格数据
for lines in sheet.iter_rows(min_row=2, min_col=1, values_only=True):
    #for row in list(sheet.values[]):
    row = list(lines)
    subports = row[3]
    tel = row[6].replace('*','')
    reporting_time = row[4][:10].replace('-','')
    l = set()
    tel_dict = dict()
    s_t = subports_tel.get(subports, None)
    if s_t is None:
        tel_dict[tel] = reporting_time
        l.add(tel_dict)
        subports_tel[subports] = l 
    else:
        tel_dict[tel] = reporting_time
        subports_tel[subports].add(tel_dict)

print(subports_tel)  
w_f = open('/share/tmp/zengq/file_compare/test/w_f', 'w')
# # 获取文件时间戳方法
# for tel_time in subports_tel.values():
#     for time_value in tel_time:
#         file_timestamp = gettimestamp(time_value[1])
#         for f in file_timestamp:
srcfiles = getFileList('/share/B/sms_mr', 'mr.log', ['202205*'])
with open(srcfiles, 'r') as target_file:
    for lines in target_file.readlinse():
        row = lines.split(",")
        subp = '{}{}'.format(row[16], row[17][:12])
        tel = '{}{}'.format(row[2][:4], row[2][7:])
        t_t = subports_tel.get(subp, None)
        if t_t is not None :
            w_f.write('{},{}\n'.format(subp, row[2]))
            subports_tel.pop(subp)

# w_f.close()


