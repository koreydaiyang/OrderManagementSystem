import pymysql
import pymongo
import json
import pprint
from Customers import DB_NAME, MY_SQL_PASSWORD, USERNAME
from Mongodbdata import loadMongoDb
from Search import searchfordetail


class Administrator(object):
        
    def login(self, userid, password):
        conn = pymysql.connect(host='localhost', port=3306, user=USERNAME, password=MY_SQL_PASSWORD, db=DB_NAME,
                               charset='utf8')
        cursor = conn.cursor()
        sql = "select password from administrator where id = '%s'" % userid
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

    def registration(self, userid, password, name, gender, number):
        conn = pymysql.connect(host='localhost', port=3306, user=USERNAME, password=MY_SQL_PASSWORD, db=DB_NAME,
                               charset='utf8')
        cursor = conn.cursor()
        sql = "select * from administrator where id = '%s'" % userid
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is not None:
            conn.close()
            cursor.close()
            return ("User ID exists, please enter a new username.", False)
        elif password != "" and userid != "":
            sql = """
            INSERT INTO administrator(id, password, name, gender, phone_number) values({}, '{}', '{}', '{}', '{}')
            """
            sql = sql.format(userid, password, name, gender, number)
            cursor.execute(sql)
            conn.commit()
            conn.close()
            cursor.close()
            return ("Registration successful", True)
        else:
            conn.close()
            cursor.close()
            return ("Empty id or password", False)
    
    def product_manage(self):
        conn = pymysql.connect(host='localhost', port=3306, user=USERNAME, password=MY_SQL_PASSWORD, db=DB_NAME,
                               charset='utf8')
        cursor = conn.cursor()
        sql = """
        SELECT product_id, COUNT(purchase_status = 'Sold' or null), COUNT(purchase_status = 'Unsold' or null)
        FROM item
        GROUP BY product_id
        ORDER BY product_id
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        num_rows = len(results)
        values = ()
        pointer = 0
        for i in range(1, 8):
            if pointer == num_rows:
                values = values + ((i, 0, 0), )
            elif i == 1:
                if results[0][0] == 1:
                    values = (results[0], )
                    pointer = pointer + 1
                else:
                    values = ((1, 0, 0), )
            else:
                if results[pointer][0] == i:
                    values = values + (results[pointer],)
                    pointer = pointer + 1
                else:
                    values = values + ((i, 0, 0),)
        return values

    def customers_with_fee_unpaid(self):
        conn = pymysql.connect(host='localhost', port=3306, user=USERNAME, password=MY_SQL_PASSWORD, db=DB_NAME,
                                charset='utf8')
        cursor = conn.cursor()
        try:
            sql1 = "USE " + DB_NAME
            sql2 = """SELECT customer_id, name, fee_amount, phone_number, address, email_address
                        FROM request AS r, customer AS c
                        WHERE customer_id = c.id AND request_status ='Sub and Wait'
                        ORDER BY customer_id, name"""
            cursor.execute(sql1)
            cursor.execute(sql2)
            cursor.close()
            results = cursor.fetchall()
            return results
        except:
            cursor.close()
            return "Error: unable to fecth data"

    def items_under_service(self):
        conn = pymysql.connect(host='localhost', port=3306, user=USERNAME, password=MY_SQL_PASSWORD, db=DB_NAME,
                                charset='utf8')
        cursor = conn.cursor()
        try:
            sql2 = """SELECT id, item_id, service_status, request_status
                        FROM request
                        WHERE service_status='Waiting' OR service_status='Progress'
                        ORDER BY id"""
            cursor.execute(sql2)
            results = cursor.fetchall()
            conn.close()
            return results
        except:
            conn.close()
            return "Error: unable to fecth data"

    def call_num_of_items_sold(self):
        conn = pymysql.connect(host='localhost', port=3306, user=USERNAME, password=MY_SQL_PASSWORD, db=DB_NAME,
                                charset='utf8')
        cursor = conn.cursor()
    
        try:
            sql1 = "USE " + DB_NAME
            sql2 = """SELECT category, model, COUNT(id) as num_sold
                        FROM item
                        WHERE purchase_status='Yes'
                        GROUP BY category, model
                        ORDER BY category, model"""
            cursor.execute(sql1)
            cursor.execute(sql2)
            cursor.close()
            results = cursor.fetchall()
            return (('category','model','num_of_items_sold'), results)
        except:
            cursor.close()
            return "Error: unable to fecth data"

    def A_ID_Search(self, ID, f):
        return searchfordetail(ID, f, False, False, True)

    def A_models_Search(self, m, f):
        return searchfordetail(m, f, False, False, False)

    def A_categories_Search(self, c, f):
        return searchfordetail(c, f, True, False, False)

#print(Administrator().A_models_Search("Light1",{}))
Administrator().items_under_service()

