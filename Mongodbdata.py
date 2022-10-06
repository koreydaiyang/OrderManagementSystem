import pymongo
import json
import pprint

client = pymongo.MongoClient()

dbExist = client.list_database_names()

def loadMongoDb():
    with open("items.json") as f:
        items = json.load(f)

    with open("products.json") as p:
        products = json.load(p)

    inventory = client["inventory"]
    myItems = inventory["items"]
    myProducts = inventory["products"]

    
    myItems.insert_many(items)
    myProducts.insert_many(products)

    myItems.update_many({"Category": 'Lights', "Model": 'Light1'},
                        {"$set":{"ProductID": 1}})

    myItems.update_many({"Category": 'Lights', "Model": 'Light2'},
                       {"$set":{"ProductID": 2}})

    myItems.update_many({"Category": 'Lights', "Model": 'SmartHome1'},
                       {"$set":{"ProductID": 3}})

    myItems.update_many({"Category": 'Locks', "Model": 'Safe1'},
                       {"$set":{"ProductID": 4}})

    myItems.update_many({"Category": 'Locks', "Model": 'Safe2'},
                       {"$set":{"ProductID": 5}})

    myItems.update_many({"Category": 'Locks', "Model": 'Safe3'},
                       {"$set":{"ProductID": 6}})

    myItems.update_many({"Category": 'Locks', "Model": 'SmartHome1'},
                       {"$set":{"ProductID": 7}})

                                                   


    myItems.update_many({"PurchaseStatus":"Sold"}, {"$set":{"CustomerID": "12"}}) ##This is for data given


