import csv
import pandas as pd
import copy

# pip install pandas
# pip install xlrd
# pip install openpyxl

src_file = './file_name'

qy_list = []
with open("./qy.csv", 'r', newline='') as fp_src:
    reader = csv.reader(fp_src)
    for row in reader:
        print(row)
        qy_list.append(row)
        # writer.writerow([None, row["B2"], None, row["D4"], None, None, None, None, row["I9"], \
        #                  row["J10"], row["K11"], row["L12"], row["M13"], row["N14"], row["O15"], row["P16"]])
        # outdata.append([row], ignore_index=True)

# outdata = pd.DataFrame(qy_list)

print('企业数量[{}]'.format(len(qy_list)))
mod = len(qy_list)

# outdata.to_excel('./files/un/des.xlsx', index=False, header=None)

data_list = []

with open(src_file, "r") as fp_src:
    for line in fp_src:
        srcid = line.rstrip()
        indx = int(srcid[11:13]) % mod
        info = qy_list[indx][:]
        info.insert(1, srcid)
        # print(info)
        data_list.append(info)

# # src_file.replace('txt', 'xlsx')
outdata = pd.DataFrame(data_list)

outdata.to_excel(src_file.replace('txt', 'xlsx'), index=False, header=None)

# f_des.close()
