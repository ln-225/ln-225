# def pretty_print():
#     infos=[[11,12,13,14,15,16,17],[21,22,23,24,25,26,27],[31,32,33,34,35,36,37]]
#     ptable=PrettyTable('list1 list2 list3 list4 list5 list6 list7'.split())
#     for info in infos:
#         ptable.add_row(info)
#     print(ptable)
# pretty_print()
from operator import length_hint
import cx_Oracle

#连接数据库
stat_config=dict()
stat_config['db_user'] = 'xysms'
stat_config['db_pass'] = 'dev123456'
stat_config['db_tnsname'] = '127.0.0.2:1521/cms'
#con = cx_Oracle.connect('xysms','dev123456','127.0.0.2:1521/cms')
#建立游标
with cx_Oracle.connect(stat_config['db_user'],stat_config['db_pass'],stat_config['db_tnsname']) as con:
    cur = con.cursor()
    ec_dict = sign_dict = dict()
    sql = '''
        select a.*,b.* from
        (select main_user,ec_name from security_user)a 
        right join
        (select username,sum(rp_success_number) as rp from stat_extcode where 
        send_time = (select to_char(trunc(sysdate - 1),'yyyymmdd') from dual) group by username)b 
        on a.main_user = b.username order by rp desc
    '''
    ec_ec_name_rp_num = list()
    for row in cur.execute(sql):
        ec_ec_name_rp_num.append(row[0])
        ec_ec_name_rp_num.append(row[1])
        ec_ec_name_rp_num.append(row[3])
        #print(ec_name,rp_num)
    #print(ec_ec_name_rp_num)
    #取ec,ec_name,rp_num
    for i in range(0,len(ec_ec_name_rp_num)):
        if i % 3 == 0:
            ec = ec_ec_name_rp_num[i]
            ec_name = ec_ec_name_rp_num[i+1]
            rp_num = ec_ec_name_rp_num[i+2]
            #print(ec,ec_name,rp_num)
            sql = '''
                select signature,sum(rp_success_number) as rp 
                from stat_extcode where send_time = (select to_char(trunc(sysdate - 1),'yyyymmdd') from dual) 
                and username = ('%s') group by signature order by rp desc
            ''' %(ec)
            for row in cur.execute(sql):
                sign = row[0]
                sign_num = row[1]
                #print(sign,sign_num)

                

    
            





