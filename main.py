import json
import xlwt
import numpy as np
import requests
import pymysql
from lxml import html
import xmlrpc.client
import pyexcel
import pandas as pd
import openpyxl
import pprint
import time
import pymongo
from tqdm import tqdm

def dict_to_excel(dict):
    # dict转二维列表，将字典dict的行列保存
    row = dict.keys()  # 取第一维键值
    col = list(dict.values())[0].keys()  # 取第二维键值，由于第二维的键值都一样，取第一组即可
    excel = [list(dict[u].values()) for u in dict]
    # 将第一维每个键值对应的第二维的values分别取出插入excel，即[[0,1] [1,0]]
    # print(excel)
    # 利用到pandas库中的DataFrame类，建议去查官方文档，或者按住CTRL点击DataFrame查看数据结构即可
    df = pd.DataFrame(data=excel, index=row, columns=col)
    # print(df)
    # 官方文档的ExcelWriter识别不了，用pandas库的即可
    with pd.ExcelWriter('metadata.xlsx') as writer:
        df.to_excel(writer)


if __name__ == '__main__':
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["pypi"]
    mycol = mydb["data"]
    client = xmlrpc.client.ServerProxy('https://pypi.org/pypi')
    package_list = client.list_packages()
    break_point = package_list.index('halfspace')
    package_list = package_list[break_point+1:]
    # version = client.package_releases('jsii-native-python',True)
    # meta_data = {}
    i = 0
    for package in tqdm(package_list):
        i = i + 1
    #     version = client.package_releases('jsii-native-python')
        s = requests.session()
        s.keep_alive = False
        url = 'https://pypi.org/pypi/'+ package + '/json'
        try:
            response = requests.get(url).text
        except:
            time.sleep(1)
            response = requests.get(url).text
        try:
            data = json.loads(response)
        except:
            temp = {'name': package, 'message': 'wrong json'}
            x = mycol.insert_one(temp)
            continue

        data['name'] = package
        if 'info' in data:
            info = data['info'].copy()
            temp = info.update(data)
            info.pop("info")
        else:
            info = data
        # info['metadata'] = response
        # info['releases'] = json.dumps(info['releases'])
        x = mycol.insert_one(info)

        # print(i)



    # dict_to_excel(meta_data)
    print("hh")
