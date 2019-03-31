from flask_restful import Resource
#from flask_jwt import jwt_required
#from models.item import ItemModel
from flask import request, jsonify
import psycopg2
from psycopg2 import errorcodes
from datetime import datetime

def post(data):
    #reveived data format: {"order":{“first_name”:”Lisa”,”e-mail”:”lisa@gmail.com”,
                            #“item”:
                            #{“A001”:”1”, “A002”:“1”}   #”品號”:”數量”
                            #}}
    #data = request.get_json()
    if data.get("order", None) == None:
        return {"message":"input data invalid!"}

    order = data.get("order")
    first_name = order['first_name']
    e_mail = order['e-mail']
    items = order['item']

    #connect_db
    db = psycopg2.connect(database="meetjobs", user="kivy", password="kivy", host="192.168.163.128", port="5432")
    cur = db.cursor()
    l_sql = "SELECT COUNT(1) FROM Product WHERE ProductId = %s AND StockQty >= %s"
    l_sql2 = "SELECT ProductName1 FROM Product WHERE ProductId = %s"
    #check if the stock qty is satisfied
    err_msg = []
    shopping_dict = {}
    for productId, qty in items.items():
        try:
            cur.execute(l_sql, (productId, qty))
        except Exception as e:
            db.close()
            return {"message":errorcodes.lookup(e.pgcode)}
        cnt = cur.fetchone()[0]
        if cnt == 0 or cnt == None:
            try:
                cur.execute(l_sql2, (productId,))
            except Exception as e:
                db.close()
                return {"message":errorcodes.lookup(e.pgcode)}
            productName = cur.fetchone()[0]
            err_msg.append("Product ID: {}, Product Name: {} had been sold out!".format(productId, productName))
        else:
            shopping_dict[productId] = float(qty)
    if err_msg != []:
        db.close()
        return {"message": err_msg}

    #Generate Customer ID
    try:
        cur.execute("SELECT MAX(customerid) FROM customer")
        customerId = cur.fetchone()
        if customerId[0] == None:
            customerId = 1
        else:
            customerId = int(customerId[0])
            customerId += 1
    except Exception as e:
        db.close()
        return {"message":errorcodes.lookup(e.pgcode)}

    #add a customer to database
    l_sql3 = "INSERT INTO Customer(CustomerId,CustomerName,Email,Status) VALUES(%s,%s,%s,%s)"
    try:
        cur.execute(l_sql3,(customerId,e_mail,first_name,"Y"))
    except Exception as e:
        db.close()
        return {"message":errorcodes.lookup(e.pgcode)}

    #Generate Order ID
    try:
        cur.execute("SELECT MAX(orderid) FROM orderd")
        orderId = cur.fetchone()
        if orderId[0] == None:
            orderId = 1
        else:
            orderId = int(orderId[0])
            orderId += 1
    except Exception as e:
        db.close()
        return {"message":errorcodes.lookup(e.pgcode)}

    #add a order to database
    l_sql4 = "INSERT INTO Orderd(orderid,OrderTime,CustomerID,Status) VALUES(%s,%s,%s,%s)"
    try:
        cur.execute(l_sql4,(orderId,datetime.now(),customerId,"Y"))
    except Exception as e:
        db.close()
        return {"message":errorcodes.lookup(e.pgcode)}

    #add orderlist to database
    l_sql5 = """INSERT INTO OrderList(OrderId,OrderSeq,ProductId,UnitPrice,Quantity,Amount,Tax,Status)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
             """
    orderSeq = 0
    for productId, Quantity in shopping_dict.items():
        #lookup UnitPrice
        try:
            cur.execute("SELECT UnitPrice FROM product WHERE productId = %s",(productId,))
        except Exception as e:
            db.close()
            return {"message":errorcodes.lookup(e.pgcode)}
        unitPrice = cur.fetchone()[0]
        unitPrice = float(unitPrice)
        orderSeq += 1

        try:
            cur.execute(l_sql5,(orderId,"{}-{:03}".format(orderId, orderSeq),productId,unitPrice,Quantity,Quantity*unitPrice,0,"Y"))
        except Exception as e:
            db.close()
            return {"message":errorcodes.lookup(e.pgcode)}

        #update  StockQty
        l_sql6 = "UPDATE Product SET StockQty = StockQty - %s"
        try:
            cur.execute(l_sql6,(Quantity,))
        except Exception as e:
            db.close()
            return {"message":errorcodes.lookup(e.pgcode)}


    #Generate Sendmail ID
    try:
        cur.execute("SELECT MAX(sendid) FROM sendmail")
        sendId = cur.fetchone()
        if sendId[0] == None:
            sendId = 1
        else:
            sendId = int(sendId[0])
            sendId += 1
    except Exception as e:
        db.close()
        return {"message":errorcodes.lookup(e.pgcode)}


    f_cnt = 1
    order_str = ""
    for productId, Quantity in shopping_dict.items():
        #lookup ProductName1
        try:
            cur.execute("SELECT productName1 FROM product WHERE ProductId = %s",(productId,))
        except Exception as e:
            db.close()
            return {"message":errorcodes.lookup(e.pgcode)}
        productName1 = cur.fetchone()[0]
        order_str += "\n{}. Product ID: {} Product Name: {} Quntity: {}"\
                        .format(f_cnt, productId, productName1, Quantity)
        f_cnt += 1

    l_content = "Dear {},\nOrder number:{} has been received.\n Your order list:{}"\
                    .format(first_name, orderId, order_str)

    #add Sendmail to database
    l_sql7 = """INSERT INTO SendMail(SendId,ToAddress,CcAddress,SecretCcAddress,Title,Article,Status)
                VALUES(%s,%s,%s,%s,%s,%s,%s)
             """
    try:
        cur.execute(l_sql7,(sendId,e_mail,"","","Order Confirmed",
                    l_content,"N"))
    except Exception as e:
        db.close()
        return {"message":errorcodes.lookup(e.pgcode)}
    db.commit()
    db.close()
    return {"message":"The order has been received!"}




l_dict = {"order":{"first_name":"Lisa","e-mail":"lisa@gmail.com","item":{"A001":"1","A002":"2"}}}
#l_json = jsonify(l_dict)
l_message = post(l_dict)
