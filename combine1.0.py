'''
用于表合并的函数
'''

import pandas as pd
import os

def excel_merger(path, outfile_name):
    os.chdir(path)
    excel_all = None
    sum = 0     # 总和
    for excel in os.listdir('.'):
        temp_df = pd.read_excel(excel)  # 可以让全表的数据类型变成object
        print("表名：" + excel + ": %d" % len(temp_df))
        sum += len(temp_df)
        excel_all = pd.concat((excel_all, temp_df))     # 合并操作

    excel_all.to_excel(outfile_name, index = False)     # 输出
    print("finished!,Total number of row is:"+str(sum))
    print("the output file is :%d"%len(excel_all))



if __name__ == '__main__':
    # 请输入需要合并的文件的目录
    file_path = r"D:\RPA_project\rpa_demand3\result"
    outfile_name = "output_fin.xlsx"
    excel_merger(file_path, outfile_name)
