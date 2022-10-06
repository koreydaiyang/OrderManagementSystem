import pymongo
from Mongodbdata import loadMongoDb

def searchfordetail(c, f, ifCategory, ifCustomer, itemSearch):
    client = pymongo.MongoClient()
    dbExist = client.list_database_names()

    if "inventory" not in dbExist:
        loadMongoDb()
    db = client["inventory"]
    myItems = db["items"]

    if ifCategory:
        dic = {"Category": c}
    elif itemSearch:
        dic = {"ItemID" : c}
    else:
        dic = {"Model" : c}
    

    dic.update(f)

    if ifCustomer: 
        listI = myItems.aggregate([{
        '$lookup':{
            'from': "products",
            'localField': "ProductID",
            'foreignField': "ProductID",
            'as': "combine"
        }
        },{'$match':
            dic},
        {'$group': {"_id" : {"Category": "$Category", "Model":"$Model", "Warranty": "$combine.Warranty (months)","Cost": "$combine.Cost ($)",
                    "Price": "$combine.Price ($)"},
                    "Inventory": { "$sum": 1 }}},
        {'$project': {"_id":0, "Category":"$_id.Category", "Model":"$_id.Model", "Warranty": "$_id.Warranty","Cost": "$_id.Cost",
                    "Price": "$_id.Price", "Inventory_level":"$Inventory"}},
        {'$sort' : {"Category" :1}}
        ])
    elif itemSearch:
        listI = myItems.aggregate([{
        '$lookup':{
            'from': "products",
            'localField': "ProductID",
            'foreignField': "ProductID",
            'as': "combine"
            }
        },{'$match':
            dic},
        {'$project': { "_id":0, "Category":1, "Model":1, "Color":1, "PurchaseStatus":1, "CustomerID":1, "Color": 1, "Factory": 1,
                                       "PowerSupply" : 1, "ProductionYear" :1,
                       "Warranty":"$combine.Warranty (months)" , "Cost": "$combine.Cost ($)"}}
        ])
    else: 
        listI = myItems.aggregate([{
        '$lookup':{
            'from': "products",
            'localField': "ProductID",
            'foreignField': "ProductID",
            'as': "combine"
            }
        },{'$match':
            dic},
        {'$group': {"_id" : {"Category": "$Category", "Model":"$Model", "Warranty": "$combine.Warranty (months)","Cost": "$combine.Cost ($)",
                             "Price": "$combine.Price ($)"},
                    "Inventory": { "$sum": {'$cond' : {'if' : {'$eq' : ['$PurchaseStatus' , 'Sold']}, 'then' : 1, 'else' : 0}}}, 
                    'Sold Items' : { "$sum": {'$cond' : {'if' : {'$eq' : ['$PurchaseStatus' , 'Unsold']}, 'then' : 1, 'else' : 0}}}}},
        {'$project': {"_id":0, "Category":"$_id.Category", "Model":"$_id.Model", "Warranty": "$_id.Warranty","Cost": "$_id.Cost",
                             "Price": "$_id.Price", "Inventory_level":"$Inventory"}},
        {'$sort' : {"Category" :1}}
        ])

    resultListI = list(listI)
    return resultListI


