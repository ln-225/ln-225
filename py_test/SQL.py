from os import readlink
import cx_Oracle
#连接数据库
con=cx_Oracle.connect('sms168','dev123456','127.0.0.4:1521/cms')
#建立游标
cur=con.cursor()
user_dict=sign_dict=dict()
#通过游标将查询数据库的结果利用row变量遍历出来   user_name/signature/mt_success_number 
for row in cur.execute(
    'select username,signature,rp_success_number from stat_extcode where send_time=20210920 order by username asc,rp_success_number desc'
    ):
#    print(row)  
#row[0]——user  row[1]——sign row[2]——number  其结果为一个列表，列表每个元素数据类型是元组
    for i in range(5):
        # user=row[0] 
        # sign=row[1] 
        # num=row[2]
        if row[0] not in user_dict:
            user_dict[row[0]]={row[1]:row[2]}
            i+=1
        print(user_dict)
con.close()
