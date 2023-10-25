#type(username)    #!!!判断数据类型！！！
import os
#定义文件对象的路径
path='C:/Users/Z_Q/Desktop/us/route/sms_mr/'
#遍历一个目录下多个文件夹，并判断日志文件名是否有对应的时间字符串（starswish(string.starswish(子字符串,beg=(起始位置)，end=(结束位置)))）
for file_name in os.listdir(path):
    if file_name[7:15].startswith('20210801')==True:
        files_name=path+file_name
        #定义字典
        ec_dict=dict()
        #open函数打开文件对象
        with open(files_name,'rt',encoding='utf-8') as files:
        #对文件内容进行遍历，即读文件
            for i in files.readlines():
        #将读取的每一行，以逗号作为分隔符放进列表row里，元素数据类型为字符串string
                row=i.split(",",-1)
                if row[4]=='0' and row[14][:10]=='2021-08-01':
                    username=row[18]  
                    sign=row[26]
                    if username not in ec_dict:                      #当username第一次出现时，将其初始化给字典ec_dict作为键
                        ec_dict[username]={sign:1}
                    else:                                           #当username在字典ec_dict里出现时，去进行下一层签名sign的判断                              
                        sign_dict=ec_dict[username]                  #当签名sign不在字典username里时，将其初始化给字典username作为键
                        if username not in sign_dict:    
                            sign_dict[sign]=1                       #对应的value为1（出现一次）
                        else:
                            sign_dict[sign]+=1                      #对ec和签名sign的出现次数逐渐累加
            dode_dict=dict()
            #dict.items：将字典变为列表，列表元素为元组，元组元素是对应的键值
            for username,sign in ec_dict.items():                    #将username和ec_dic两个参数传进嵌套字典里
                code_list=sorted(sign.items(),key=lambda x: x[1])[:5]   #利用sorted函数将嵌套字典里的sign_dict字典的第二位（值）抽取出来作为排序关键并取排名前五的签名
                dode_dict[username]=code_list                        #以排序好的签名sign找到对应的签名的username放到dode_dict字典里
            print(dode_dict)                                #将对应的username和sign的条数打印出来
                 


                                                
        
        