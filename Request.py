import pymysql
from Customers import DB_NAME, MY_SQL_PASSWORD, USERNAME
from Admins import Administrator
import datetime


class Request(object):
    def submit_request(self, userid, itemid):
        conn = pymysql.connect(host='localhost', port=3306, user=USERNAME, password=MY_SQL_PASSWORD, db=DB_NAME,
                               charset='utf8')
        cursor = conn.cursor()
        sql1 = """
        SELECT id
        FROM item
        WHERE customer_id = {}
        """
        sql1 = sql1.format(userid)
        cursor.execute(sql1)
        items = list(map(lambda x:x[0], cursor.fetchall()))
        if int(itemid) in items:
            sql3 = """
            SELECT purchase_date, product_id
            FROM item
            WHERE id = {}
            """
            sql3 = sql3.format(itemid)
            cursor.execute(sql3)
            result = cursor.fetchone()
            purchase_date = result[0].strftime('%Y-%m-%d')
            productid = result[1]
            sql4 = """
            SELECT warranty
            FROM product
            WHERE id = {}
            """
            sql4 = sql4.format(productid)
            cursor.execute(sql4)
            warranty = cursor.fetchone()[0]
            current_date = datetime.date.today().strftime('%Y-%m-%d')
            ifinwarranty = self.ifwarranty(purchase_date, current_date, warranty)
            if ifinwarranty:  # purchase status lack
                sql2 = """
                INSERT request (date, request_status, service_status, customer_id, item_id, fee_amount) 
                VALUES(CURDATE(), 'Progress', 'Progress', {}, {}, 0)
                """
                sql2 = sql2.format(userid, itemid)
                cursor.execute(sql2)
                conn.commit()
                conn.close()
                return (0,"Submmited")

            else:
                sql2 = """
                INSERT request (date, request_status, service_status, customer_id, item_id, fee_amount) 
                VALUES(now(), 'Sub and Wait', 'Waiting', {}, {}, {})
                """
                fee = self.calculateFee(itemid)  # write a function to calculate
                sql2 = sql2.format(userid, itemid, fee)
                cursor.execute(sql2)
                conn.commit()
                conn.close()
                return (1,"Submmited and Waiting")
        else:
            return (2,"Cannot submit items for others")

    def ifwarranty(self, purchase_date, current_date, warranty):
        purchase_year = int(purchase_date[0:4])
        purchase_month = int(purchase_date[5:7])
        purchase_day = int(purchase_date[-2:-1])
        current_year = int(current_date[0:4])
        current_month = int(current_date[5:7])
        current_day = int(current_date[-2:-1])
        expire_month = purchase_month + warranty
        expire_year = purchase_year
        if expire_month > 12:
            expire_year = expire_year + expire_month // 12
            expire_month = expire_month % 12
        if expire_year > current_year:
            return True
        elif expire_year == current_year & expire_month > current_month:
            return True
        elif expire_year == current_year & expire_month == current_month & purchase_day >= current_day:
            return True
        else:
            return False

    def calculateFee(self, itemid):
        conn = pymysql.connect(host='localhost', port=3306, user=USERNAME, password=MY_SQL_PASSWORD, db=DB_NAME,
                               charset='utf8')
        cursor = conn.cursor()
        sql = "SELECT product_id FROM item WHERE id = {}".format(itemid)
        cursor.execute(sql)
        productid = cursor.fetchone()[0]
        sql2 = "SELECT price FROM product WHERE id = {}".format(productid)
        cursor.execute(sql2)
        price = cursor.fetchone()[0]
        return 40 + 0.2 * price


    def payment(self, requestid):
        conn = pymysql.connect(host='localhost', port=3306, user=USERNAME, password=MY_SQL_PASSWORD, db=DB_NAME,
                           charset='utf8')
        cursor = conn.cursor()
        sql = """
        UPDATE request
        SET request_status = 'Progress', service_status = 'Progress', payment_date = now()
        WHERE id = {}
        """
        sql = sql.format(requestid)
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return print("Payment successful")

    def cancel(self, requestid, userid):
        conn = pymysql.connect(host='localhost', port=3306, user=USERNAME, password=MY_SQL_PASSWORD, db=DB_NAME,
                           charset='utf8')
        cursor = conn.cursor()

        sql = """
        UPDATE request
        SET request_status = 'Cancel', service_status = 'Completed'
        WHERE id = {} AND customer_id = {}
        """
        sql = sql.format(requestid, userid)
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return "Request cancelled"

    def approve(self, requestid, adminid):
        conn = pymysql.connect(host='localhost', port=3306, user=USERNAME, password=MY_SQL_PASSWORD, db=DB_NAME,
                               charset='utf8')
        cursor = conn.cursor()
        sql0 = """
        SELECT id
        FROM request
        WHERE request_status = 'Progress'
        """
        cursor.execute(sql0)
        requests = list(map(lambda x:x[0], cursor.fetchall()))
        if int(requestid) not in requests:
            return "Request cannot be approved"
        sql = """
                UPDATE request
                SET request_status = 'Approved', admin_id = {}
                WHERE id = {}
                """
        sql = sql.format(adminid, requestid)
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return "Request approved"

    def complete(self, requestid, adminid):
        conn = pymysql.connect(host='localhost', port=3306, user=USERNAME, password=MY_SQL_PASSWORD, db=DB_NAME,
                               charset='utf8')
        cursor = conn.cursor()
        #Check whether can serve
        sql = """
        SELECT id
        FROM request
        WHERE service_status = "Progress"
        """
        cursor.execute(sql)
        requests = cursor.fetchall()
        requests = list(map(lambda x : x[0], requests))
        if int(requestid) not in requests:
            return "The request is not ready to be served."
        #if can, serve it
        sql1 = """
                UPDATE request
                SET service_status = "Completed", request_status = 'Complete', admin_id = {}
                WHERE id = {}
                """
        sql1 = sql1.format(adminid, requestid)
        cursor.execute(sql1)
        conn.commit()
        conn.close()
        return "Request completed"

    
    def track(self, userid):
        conn = pymysql.connect(host='localhost', port=3306, user=USERNAME, password=MY_SQL_PASSWORD, db=DB_NAME,
                               charset='utf8')
        cursor = conn.cursor()
        sql1 = """
                SELECT id, item_id, service_status, fee_amount
                FROM request
                WHERE customer_id = {}
                """
        sql1 = sql1.format(userid)
        cursor.execute(sql1)
        result = cursor.fetchall()
        conn.close()
        return result
    
    def all_items(self, userid):
        conn = pymysql.connect(host='localhost', port=3306, user=USERNAME, password=MY_SQL_PASSWORD, db=DB_NAME,
                               charset='utf8')
        cursor = conn.cursor()
        sql1 = """
        SELECT id, category, model, product_id, purchase_date
        FROM item
        WHERE customer_id = {}
        """
        sql1 = sql1.format(userid)
        cursor.execute(sql1)
        result = cursor.fetchall()
        conn.close()
        return result

# Request().submit_request('1', '1001', True)
# Request().submit_request('1', '1001', False)
# Request().payment(5)
# Request().cancel(6)
# Request().all_items(1)
# Request().approve('1', '1')
print(Request().submit_request('1', '1001'))
