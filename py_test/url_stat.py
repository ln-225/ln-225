#!/usr/bin/env python3
# coding=utf-8
import os
import sys
import time
import datetime
import re
import cx_Oracle
from collections import defaultdict


# 参数配置
stat_config = dict()

# 日志文件路径

# oracle数据库信息
stat_config['db_user'] = 'sms168'
stat_config['db_pass'] = 'dev123456'
stat_config['db_tnsname'] = 'smoc3'
# mysql库 信息
stat_config['mysql_user'] = 'sms168'
stat_config['mysql_pass'] = 'test123456'
stat_config['mysql_db'] = 'cms'

# 发送过 超过 阈值 数量的短链才需要提取信息
stat_config['d_threhold'] = 3000

# stat_config['root_path'] = '/share/B/mina-cmpp-data/mr_receive/'
stat_config['root_path'] = '/alidata/mina-cmpp/data/mr_receive/'
# stat_config['root_path'] = '/share/tmp/yyzq/mr_data/'
# 命令行参数  yyyymm
yearmonth = sys.argv[1]
stat_config['file_prefix'] = 'mr.receive.{}'.format(yearmonth)

begin = time.time()

# {ec：{短链:条数,..}}
ec_domain = dict()
# {域名: 注册主体}
domain_info = dict()

# 表里已经解析过的域名
existed_domains = set()
# 表里已经解析过的域名
existed_ec_domain = dict()
# 最终待解析的域名
domains = set()
ec_set = set()



# 获取 需要处理的ec 列表
con_time = None
if len(yearmonth) == 8:
    con_time = " ={} ".format(yearmonth)
elif len(yearmonth) == 6:
    con_time = " between {} and {} ".format(int(yearmonth)*100+1, int(yearmonth)*100+31)
else:
    print("时间格式错误")
    sys.exit(1)

# 账号关键字
ec_keys = ["金融","信用卡","网贷","个贷","保险","游戏"]
# 额外ec列表
ec_extra = {"h11085","h10085","h12085"}
con_ecname = " ec_name like \'%{}%\' ".format(ec_keys[0])
for i in ec_keys[1:]:
    con_ecname += " or ec_name like \'%{}%\' ".format(i)


def get_ec_list():
    global ec_set
    with cx_Oracle.connect(stat_config['db_user'], stat_config['db_pass'], stat_config['db_tnsname']) as conn:
        with conn.cursor() as cursor:
            # 金融营销类 ec
            sql = '''select username from 
                (select username  from stat_send y 
                where send_time {} group by y.username having sum(y.rp_success_number) >1000) a 
                 inner join 
                (select login_name as b_username from security_user where {} and status =1 
                ) b on a.username = b.b_username'''.format(con_time, con_ecname)
            for ec in cursor.execute(sql):
                ec_set.add(ec[0])


get_ec_list()
if len(ec_extra) >0:
    ec_set = ec_set.union(ec_extra)

print(f'获取目标ec[{ec_set}]')

# exp = r'(?:https?://)?([-\w.]+)/(?:[-\w./]*)'
# exp = r'(?:https?://)?([-\w.]+)/(?:[-\w./]{4,})'
exp = r'^【(.*?)】.*?(?:https?://)?([-\w.]+)/(?:[-\w./]{2,})'
p = re.compile(exp, re.A)


print('提取数据。。。')

for dirpath, dirnames, filenames in os.walk(stat_config['root_path']):
    for f_name in filenames:
        if f_name.startswith(stat_config['file_prefix']):
            f_srcfile = os.path.join(dirpath, f_name)
            print('[{}]'.format(f_srcfile))
            with open(f_srcfile, 'rt', encoding='utf8') as f_src:
                for line in f_src:
                    row = line.split(',')
                    # 只匹配 指定ec 且成功 的记录
                    if row[5] != 'DELIVRD' or row[4] not in ec_set:
                        continue
                    m = p.search(row[12])
                    if m:
                        # 过滤 不是域名的
                        if re.search('\.', m.group(2)) is None:
                            continue
                        domain_dict = ec_domain.get(row[4], None)
                        if domain_dict is None:
                            ec_domain[row[4]] = domain_dict = defaultdict(int)
                        # 域名|签名 计数
                        domain_dict[m.group(2)+'|'+m.group(1)] += 1
                        # 域名剔重
                        # domains.add(m.group(2))


for ec, info_dict in ec_domain.items():
    for d_s, cnt in info_dict.items():
        # 大于阈值 才处理
        d, s = d_s.split('|')
        if cnt > stat_config['d_threhold']:
            print(f'{d}|{ec}|【{s}】|{cnt}')


end = time.time()
print("time[{}]".format(end-begin))

