import pymongo
import numpy as np  # 加载数学库用于函数描述
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style



if __name__ == '__main__':
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["pypi"]
    extra = mydb["extra"]
    # count = mycol.count_documents({"requires_dist":{"$ne":None}})
    year = []
    allnum = []
    extranum = []
    ratio = []
    for i in range(2005,2022):
        year.append(i)
        target = mydb["extra"+str(i)]
        # pipeline = [
        #     {'$match':{ "$and" : [{"upload_time" : { "$gte" : "{start}-01-01".format(start=i) }}, {"upload_time" : { "$lt" : "{end}-01-01".format(end=i+1) }}] }},
        #     {"$group": {
        #         "_id": {"name": "$name"},
        #         "count": {"$sum": 1},
        #         "upload_time": {"$min": "$upload_time"},
        #         "requires_dist": {"$addToSet": "$requires_dist"}
        #     }},
        #     {"$addFields": {
        #         "requires_dist": {
        #             "$reduce": {
        #                 "input": "$requires_dist",
        #                 "initialValue": [],
        #                 "in": {"$setUnion": ["$$value", "$$this"]}
        #             }
        #         }
        #     }},
        #     {"$project": {
        #         "_id": 0,
        #         "name": "$_id.name",
        #         "count": "$count",
        #         "upload_time": "$upload_time",
        #         "requires_dist": "$requires_dist"
        #     }},
        # ]
        # target.delete_many({})
        # ans = extra.aggregate(pipeline,allowDiskUse = True)
        # target.insert_many(ans)
        q = {"requires_dist" : {'$regex':".*extra.*"}}
        extranum.append(target.count_documents(q))
        allnum.append(target.count_documents({}))
        ratio.append(target.count_documents(q)/target.count_documents({}))
    plt.plot(year,allnum,label="all")
    plt.plot(year,extranum,label="extra")

    for x,y in zip(year,allnum):
        plt.text(x,y,y)
    for x,y in zip(year,extranum):
        plt.text(x,y,y)
    plt.show()
    plt.plot(year,ratio,label="ratio")
    for x,y in zip(year,ratio):
        plt.text(x,y,y)
    plt.show()

    print("hh")
