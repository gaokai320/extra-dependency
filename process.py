import pymongo
import numpy as np  # 加载数学库用于函数描述
import string
import matplotlib
import matplotlib.pyplot as plt
import xlwt
from matplotlib import style
from packaging.requirements import Requirement
from collections import defaultdict
from tqdm import tqdm
allpackage = 356016
allextra = 24798

if __name__ == '__main__':
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["pypi"]
    package = mydb["package_copy1"]
    extra = np.zeros(105)
    noextra = np.zeros(105)

    for x in tqdm(package.find()):
        temp = x['requires_dist']
        num = len(temp)
        if num > 100:
            num = 100
        sign = x['sign']
        if sign == 1:
            extra[num] = extra[num] + 1
        elif sign == 0:
            noextra[num] = noextra[num] + 1
        # for dependency in temp:
        #     if dependency.find('extra') != -1:
        #         sign = 1
        #     new.add(dependency.replace(" ",''))
        # package.update_one({"_id":x['_id']},{"$set":{"requires_dist":list(new),"sign":sign}})
    f = xlwt.Workbook('encoding = utf-8')  # 设置工作簿编码
    sheet1 = f.add_sheet('sheet1', cell_overwrite_ok=True)  # 创建sheet工作表
    for i in range(len(extra)):
        sheet1.write(i, 0, extra[i])  # 写入数据参数对应 行, 列, 值
    for i in range(len(noextra)):
        sheet1.write(i,1, noextra[i])  # 写入数据参数对应 行, 列, 值

    f.save('analyze2.xls')  # 保存.xls到当前工作目录