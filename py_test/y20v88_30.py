#账号下发量预警查询
#!/usr/bin/env python3
from datetime import datetime,timedelta
import cx_Oracle
import json
import os

ad=datetime.now()
y=datetime.now().year
m=int(ad.strftime('%m'))
d=int(ad.strftime('%d'))
h=int(ad.strftime('%H'))  #当前小时
b_h=h-1     #前一个小时
b_h_=h-2    #前两个小时
b_h_file='/share/tmp/zengq/30_warning/'+'w'+str(b_h_)
d_d=str(y)+str(m)+'%'

#查询日志目录文件名
file_path='/alidata02/data/sms_mt/'+'mt.log.'+str(y)+str(m)+str(d)+str(b_h)+'.sgip.172.17.65.83'
#print(file_path)

#连接数据库
stat_config=dict()
stat_config['db_user'] = 'sms168'
stat_config['db_pass'] = 'test123456'
stat_config['db_tnsname'] = 'smoc3'

sum=dict()
multiple=200000
sum[b_h]=0
#imms_from=['10682073','10690639','10691050','10691313','10691967']
src_path='/share/tmp/zengq/30_warning/'
b_cnt_f=src_path+'w'+str(b_h)

#读取前前一个小时的下发成功数量
with open(b_h_file,'rt') as th_f:
    for line in th_f:
        sum[b_h_]=int(line)

#开始统计本月至前一个小时的下发成功数总量
with open(file_path,'rt') as count:
    for lines in count:
        row=lines.split(',')
        if row[4]=="0" and row[3]=="y20v88":
            sum[b_h]+=1
            s=sum[b_h]+sum[b_h_]
            with open(b_cnt_f,'w') as b_cnt:
                if b_h==7:
                    with cx_Oracle.connect(stat_config['db_user'],stat_config['db_pass'],stat_config['db_tnsname']) as con:
                        cur=con.cursor()
                        sql="select sum(mt_success_number) from stat_extcode where username='"'y20v88'"' and send_time like ('%s')" %(d_d)
                        for row in cur.execute(sql):
                            sum[sq]=row[0]
                            s=sum[sq]+sum[b_h]+sum[b_h_]
                            b_cnt.write(str(s))
                            os.system('rm -f {b_h_file}'.format(b_h_file=b_h_file))
                else:
                    b_cnt.write(str(s))
                    os.system('rm -f {b_h_file}'.format(b_h_file=b_h_file))

            #定义curl命令参数
            header='curl -H "Type":"application/json" --data-urlencode '
            apiurl=' http://172.17.65.87:5880/template/send'
            data={
                'username':'b_h9999',
                'password':'123456',
                'templateid':'10004000',
                'extcode':'449',
                'content':["15629972470|账号y20v88成功提交量已超过{cnt}条，请及时修改imms_from参数".format(cnt=s)],#"18971069423|账号y20v88成功提交量已超过{cnt}条，请及时修改imms_from参数".format(cnt=s)],
            }
            #将data从json的数据格式转换成shell命令行的数据格式
            js_str=json.dumps(data)
            cur=header+' '+chr(39)+js_str+chr(39)+apiurl
            #值到达开始预警
            for i in range(100):
                if s > (i*multiple) and s < ((i+1)*multiple):
                    target_file=src_path+'w'+str(b_h)
                    with open(target_file,'w') as w_cnt:
                        w_cnt.write(str(s))
                        os.system(cur)


##########测试部分##########
#!/usr/bin/env python3 
#from datetime import datetime,timedelta
#import os
#import json
#import requests
#
#header='curl -H "Type":"application/json" --data-urlencode '
#apiurl=' http://172.17.65.87:5880/template/send'
#data={
#    'username':'h19999',
#    'password':'123456',
#    'templateid':'10004000',
#    'extcode':'449',
#    'content':["15629972470|test"]
#}
#
#js_str=json.dumps(data)

#command=header+' '+chr(39)+js_str+chr(39)+apiurl
#os.system(command)
#sr='/share/tmp/zengq/30_warning/1'
#with open(sr,'r') as sr_cnt:
#    for i in sr_cnt:
#        print(int(i)+1)

#with open(sr,'w') as f:
    #f.write('1')

#print()
#ad=datetime.now()
#y=datetime.now().year
#m=int(ad.strftime('%m'))
#d=int(ad.strftime('%d'))
#h=int(ad.strftime('%H'))  #当前小时
#b_h=h-1     #前一个小时
#b_h_=h-2    #前两个小时
#file1='/share/tmp/zengq/30_warning/'+'w'+str(b_h)
#file2='/share/tmp/zengq/30_warning/'+'w'+str(b_h_)
#os.system('touch {file1}'.format(file1=file1))
#os.system('rm -f {file2}'.format(file2=file2))