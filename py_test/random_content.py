import os,sys,csv,imp,random,openpyxl
import xlrd,xlwt
from re import I
from asyncio import LimitOverrunError

cont_f = 'C:/Users/Z_Q/Downloads/填充模板.xlsx'
target_file = 'C:/Users/Z_Q/Desktop/t.xlsx'
target_dir = 'D:/File/WeChat Files/wxid_tdx35uaplmk622/FileStorage/File/2022-05/'

#生成被追加内容文件名
list_file = []
target_files = []
for files in os.walk(target_dir): 
    list_file = files[2]
for f in list_file:
    target_files.append(target_dir + f)

content = dict()
k = []
read_excel = openpyxl.load_workbook('{}'.format(cont_f))  
# 使用指定工作表
r_sheet = read_excel.active

#获取填充文本内容，并存放进字典
for line in list(r_sheet.values):
    content[line[6]] = line
#取出字典生成一个列表
for key in content.keys():
    k.append(key)

l = int(len(k))
#写入填充内容
write_excel = openpyxl.load_workbook('{}'.format(target_file))  
w_sheet = write_excel.active
# 最大列数
maxcolumn = w_sheet.max_column
# 最大行数
maxrow = w_sheet.max_row
# for w_line in range(0,):
#     #print(w_line)
#     if w_line < :
#         # 生成随机值填充内容
#         suiji = random.randint(0,l-1)
#         new_row = list(content[k[suiji]])  # 随机内容
#         #print(suiji,new_row)
#         w_sheet.append(new_row)

write_excel.save("{}".format(target_file))