import openpyxl
import pymongo
import numpy as np  # 加载数学库用于函数描述
import string
import xlwt
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import seaborn
from packaging.requirements import Requirement
from collections import defaultdict
from tqdm import tqdm
allpackage = 356016
allextra = 24798

if __name__ == '__main__':
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["pypi"]
    package = mydb["extra2017"]
    optional_features = []
    extra_dependency = []
    every_option_of_extra = []
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
        if len(one_optional_features) != 0:
            optional_features.append(len(one_optional_features))
        if len(one_extra_dependency) != 0:
            extra_dependency.append(len(one_extra_dependency))
        for key,value in extra.items():
            every_option_of_extra.append(len(value))
        extra.clear()
        one_optional_features.clear()
        one_extra_dependency.clear()

    pic1 = seaborn.boxenplot(x=optional_features)
    pic1.set_title("optional_features")
    plt.show()
    pic2 = seaborn.boxenplot(x=extra_dependency)
    pic2.set_title("extra_dependency")
    plt.show()
    pic3 = seaborn.boxenplot(x=every_option_of_extra)
    pic3.set_title("每个option功能需要几个extra依赖")
    plt.show()
