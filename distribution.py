import openpyxl
import pymongo
import numpy as np  # 加载数学库用于函数描述
import string
import xlwt
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
from packaging.requirements import Requirement
from collections import defaultdict
from tqdm import tqdm
allpackage = 356016
allextra = 24798

if __name__ == '__main__':
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["pypi"]
    package = mydb["package"]
    optional_features = np.zeros(1000)
    extra_dependency = np.zeros(1000)
    every_option_of_extra = np.zeros(1000)
    num = 0
    for x in tqdm(package.find()):
        num = num + 1
        temp = x['requires_dist']
        one_optional_features = set()
        one_extra_dependency = set()
        extra = defaultdict(set)
        for dependency in temp:
            if dependency.find('extra') != -1:
                info = Requirement(dependency)
                func = str(info.marker).split()
                one_extra_dependency.add(info.name)
                one_optional_features.add(func[len(func)-1])
                extra[func[len(func)-1]].add(info.name)
        extra_dependency[len(one_extra_dependency)] = extra_dependency[len(one_extra_dependency)] + 1
        optional_features[len(one_optional_features)] = optional_features[len(one_optional_features)] + 1
        for key,value in extra.items():
            every_option_of_extra[len(value)] = every_option_of_extra[len(value)] + 1
        extra.clear()
        one_optional_features.clear()
        one_extra_dependency.clear()

    f = xlwt.Workbook('encoding = utf-8')  # 设置工作簿编码
    sheet1 = f.add_sheet('sheet1', cell_overwrite_ok=True)  # 创建sheet工作表
    for i in range(len(optional_features)):
        sheet1.write(i, 0, optional_features[i])  # 写入数据参数对应 行, 列, 值
    for i in range(len(extra_dependency)):
        sheet1.write(i,1, extra_dependency[i])  # 写入数据参数对应 行, 列, 值
    for i in range(len(every_option_of_extra)):
        sheet1.write(i,2, every_option_of_extra[i])  # 写入数据参数对应 行, 列, 值
    f.save('analyze.xls')  # 保存.xls到当前工作目录
    print("hh")



