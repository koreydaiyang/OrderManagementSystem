import os
import sys
sys.path.append(os.getcwd())
import pymysql
import pymongo
from dotenv import load_dotenv
from Mongodbdata import loadMongoDb
from Search import searchfordetail
load_dotenv()
MY_SQL_PASSWORD = os.getenv('MY_SQL_PASSWORD')
SQL_FILE = os.getenv('SQL_FILE')
DB_NAME = os.getenv('DB_NAME')
USERNAME = 'root'

class Customer:
    def __init__(self) -> None:
        super().__init__()
        
    def login(self, userid, password):
        conn = pymysql.connect(host='localhost', port=3306, user=USERNAME, password=MY_SQL_PASSWORD, db=DB_NAME,
                               charset='utf8')
        cursor = conn.cursor()
        sql = "select password from customer where id = '%s'" % userid
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is None:
            conn.close()
            cursor.close()
            return ("Wrong user id!", False)
        elif result[0] == password:
            conn.close()
            cursor.close()
            return ("Login successful", True)
        else:
            conn.close()
            cursor.close()
            return ("Wrong password", False)

    def registration(self, userid, password, name, gender, number, address, email):
        conn = pymysql.connect(host='localhost', port=3306, user=USERNAME, password=MY_SQL_PASSWORD, db=DB_NAME,
                               charset='utf8')
        cursor = conn.cursor()
        sql = "select * from customer where id = '%s'" % userid
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is not None:
            conn.close()
            cursor.close()
            return ("User ID exists, please enter a new username.", False)
        elif password != "" and userid != "":
            sql = """
            INSERT INTO customer(id, password, name, gender, phone_number, address, email_address) 
            VALUES({}, '{}', '{}', '{}', '{}', '{}', '{}')
            """
            sql = sql.format(userid, password, name, gender, number, address, email)
            cursor.execute(sql)
            conn.commit()
            conn.close()
            cursor.close()
            return ("Registration successful", True)
        else:
            conn.close()
            cursor.close()
            return ("Empty id or password", False)

    def C_categories_Search(self, c, f):
        return searchfordetail(c, f, True, True, False)
    
    def C_models_Search(self, m, f):
        return searchfordetail(m, f, False, True, False)

    def purchaseDB(self, Iid, Cid):
        client = pymongo.MongoClient()
        dbExist = client.list_database_names()

        conn = pymysql.connect(host='localhost', port=3306, user=USERNAME, password=MY_SQL_PASSWORD, db=DB_NAME,
                               charset='utf8')
        cursor = conn.cursor()
        if "inventory" not in dbExist:
            loadMongoDb()
        db = client["inventory"]
        myItems = db["items"]
        if Iid == None:
            return None
        else: 
            myItems.update_one({"ItemID": Iid}, {"$set":{"CustomerID": Cid, "PurchaseStatus": "Sold"}})
            sql = "update item set customer_id = %s,purchase_status= 'Sold' ,purchase_date= now() where id=%u" % (Cid,int(Iid))
            cursor.execute(sql)
            conn.commit()
        conn.close()


    def purchase(self, requirement):
        client = pymongo.MongoClient()
        dbExist = client.list_database_names()

        if "inventory" not in dbExist:
            loadMongoDb()
        db = client["inventory"]
        myItems = db["items"]

        requirement["PurchaseStatus"]="Unsold"
        result = myItems.aggregate([{
        '$lookup':{
            'from': "products",
            'localField': "ProductID",
            'foreignField': "ProductID",
            'as': "combine"
            }
        },{'$project': { "_id":0, "ItemID":1, "Category":1, "Model":1, "Color":1, "PurchaseStatus":1, "CustomerID":1, "Color": 1, "Factory": 1,
                                       "PowerSupply" : 1, "ProductionYear" :1,
                       "Warranty":"$combine.Warranty (months)" , "Cost": "$combine.Cost ($)"}},
            {'$match':
            requirement}])
        resultlist = list(result)
        if len(resultlist)==0:
            return None
        else: 
            return resultlist[0]['ItemID']
        
    def purchasedList(self, userid):
        client = pymongo.MongoClient()
        dbExist = client.list_database_names()

        if "inventory" not in dbExist:
            loadMongoDb()
        db = client["inventory"]
        myItems = db["items"]
        listI = myItems.aggregate([{
        '$lookup':{
            'from': "products",
            'localField': "ProductID",
            'foreignField': "ProductID",
            'as': "combine"
            }
        },{'$match':
            {"CustomerID":userid}},
        {'$project': { "_id":0, "Category":1, "Model":1, "Color":1, "PurchaseStatus":1, "CustomerID":1, "Color": 1, "Factory": 1,
                                       "PowerSupply" : 1, "ProductionYear" :1,
                       "Warranty":"$combine.Warranty (months)" , "Cost": "$combine.Cost ($)"}}
                
        ])

        resultlist = list(listI)[0]
        return resultlist


        

#Customer().registration("03", "1221")
#print(Customer().C_categories_Search("Lights", {}))
#print(Customer().purchase({"Color": "White"}))
