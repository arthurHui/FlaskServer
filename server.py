from flask import (Flask, jsonify, request)
import hashlib
import ntplib
import time
import json
import sqlite3
import threading
app = Flask(__name__)

#define product attributes
product={}
product["id"] = []
product["desc"] = []
product["price"] = []
product["stock"] = []
product["status"] = []
product["paid"] = []       

#get a product detail function
@app.route("/find/<int:id>", methods=["GET"])
def get_product(id):
    try :
        #get connection
        conn = sqlite3.connect('product_data.db')
        c = conn.cursor()
     
        #get all id
        cursor = c.execute("SELECT id from PRODUCT")
        item_id =""
        for item in cursor:         
            item_id += str(item)  
          
        #check the id correctly
        if str(id) not in item_id:   
            #return error message
            return jsonify(exe_id,{"error": "invalid id"}), 404
    
        #get data using input id
        cursor = c.execute(f"SELECT id, DESC, PRICE, STOCK  from PRODUCT WHERE id = {id}")
        
        #get product detail in database
        for item in cursor:
            product["id"] = item[0]
            product["desc"] = item[1]
            product["price"] = item[2]
            product["stock"] = item[3]
          
        #close the connection
        conn.close()
        
        #return product detail using json
        return jsonify(exe_id,product)
    except:
        #return error message
        return jsonify(exe_id,{"error": "server error"}), 404

#buy a porduct function
@app.route("/buy", methods=["PUT"])
def buy_product():
    with lock:
        #set the paid amount to 0
        product["paid"] = 0 
        #get connection
        data = json.loads(request.data)
        id = data.get("id")
        quantity = data.get("quantity")
        card = data.get("card")
        #connect to database
        conn = sqlite3.connect('product_data.db')
        c = conn.cursor()
        #get all id from database
        cursor = c.execute("SELECT id from PRODUCT")
          
        item_id =""
        #get all id
        for item in cursor:             
            item_id += str(item)  
            
        #check the id correctly    
        if str(id) not in item_id:    
            return jsonify(exe_id,{"error": "invalid id"}), 404
        
        #check the card available
        if len(card) != 16:
            return jsonify(exe_id,{"error": "invalid card"}), 404
          
        #get data using input id
        cursor = c.execute(f"SELECT id, DESC, PRICE, STOCK  from PRODUCT WHERE id = {id}")
        
        #get product detail in database
        for item in cursor:
            product["id"] = item[0]
            product["desc"] = item[1]
            product["price"] = item[2]
            product["stock"] = item[3]
    
        #check the quantity is or not int 
        try: 
            int(quantity)
        except ValueError:
            return jsonify(exe_id,{"error": "invalid item quantity"}), 400
        
        #check the data is missing or not
        if not quantity:
            conn.close()
            return jsonify(exe_id,{"error": "missing item quantity"}), 400
        #check the quantity and stock
        if quantity > product["stock"]:
            conn.close()
            
            #set the status of the result
            product["status"] = []
            product["status"] = "unsuccess"
            
            #return product detail using json
            return jsonify(exe_id,product)
        else:
            #reduce stock and save to the database
            stock = product["stock"] - quantity
            
            #update data with id and quantity
            c.execute(f"UPDATE PRODUCT set STOCK = {stock} where ID={id}")
            conn.commit()
            
            #get updated data
            cursor = c.execute(f"SELECT id, DESC, PRICE, STOCK  from PRODUCT WHERE id = {id}")            
            for item in cursor:
                product["id"] = item[0]
                product["desc"] = item[1]
                product["price"] = item[2]
                product["stock"] = item[3]
            
            #close the connection
            conn.close()
            
            #set the status of the result
            product["status"] = "success"
            product["paid"] = quantity * product["price"]
            
            #return product detail using json
            return jsonify(exe_id,product) 

#replenish a porduct function
@app.route("/replenish", methods=["PUT"])
def replenish_product():
    product["paid"] = 0 
    product["status"] =""
    #get the data from request
    data = json.loads(request.data)
    id = data.get("id")
    quantity = data.get("quantity")
    
    #connect to database
    conn = sqlite3.connect('product_data.db')
    c = conn.cursor()
    
    #get all id from database
    cursor = c.execute("SELECT id from PRODUCT")
          
    item_id =""
    #get all id
    for item in cursor:            
        item_id += str(item)  
        
    #check the id correctly    
    if str(id) not in item_id:    
        return jsonify(exe_id,{"error": "invalid id"}), 404
    
    #get data with input id
    cursor = c.execute(f"SELECT id, DESC, PRICE, STOCK  from PRODUCT WHERE id = {id}")
    
    #get product detail in database   
    for item in cursor:
        product["id"] = item[0]
        product["desc"] = item[1]
        product["price"] = item[2]
        product["stock"] = item[3]
         
    #check the quantity is or not int 
    try: 
        int(quantity)
    except ValueError:
        return jsonify(exe_id,{"error": "invalid item quantity"}), 400
    
    #check the data is missing or not
    if not quantity:
        conn.close()
        return jsonify(exe_id,{"error": "missing item quantity"}), 400       
    
    #check the quantity
    if quantity <= 0 :
        conn.close()
        #return quantity error message
        return jsonify(exe_id,{"error": "invalid item quantity"}), 400
    else:
        #increase stock and save to the database
        stock = product["stock"] + quantity
        
        #update data with id and quantity
        c.execute(f"UPDATE PRODUCT set STOCK = {stock} where ID={id}")
        conn.commit()
        
        #get updated data
        cursor = c.execute(f"SELECT id, DESC, PRICE, STOCK  from PRODUCT WHERE id = {id}")            
        for item in cursor:
            product["id"] = item[0]
            product["desc"] = item[1]
            product["price"] = item[2]
            product["stock"] = item[3]
            
        #close the connection
        conn.close()
        #return product detail using json
        return jsonify(exe_id,product)

if __name__ == "__main__":
    try : 
       #try to find database
       conn = sqlite3.connect('product_data.db')
       c = conn.cursor()
       cursor = c.execute("SELECT id, DESC, PRICE, STOCK  from PRODUCT")
       conn.close()
    except:
        #create database when not create yet
        conn = sqlite3.connect('product_data.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE PRODUCT
               (ID INT PRIMARY KEY     NOT NULL,
               DESC           TEXT    NOT NULL,
               PRICE            INT     NOT NULL,
               STOCK        INT NOT NULL);''')
               
        c.execute("INSERT INTO PRODUCT (ID,DESC,PRICE,STOCK) \
                  VALUES (1, 'Apple', 5, 5)")
      
        c.execute("INSERT INTO PRODUCT (ID,DESC,PRICE,STOCK) \
              VALUES (2, 'Banana', 3, 10)")
        
        c.execute("INSERT INTO PRODUCT (ID,DESC,PRICE,STOCK) \
              VALUES (3, 'Blueberries', 10, 3)")
              
        c.execute("INSERT INTO PRODUCT (ID,DESC,PRICE,STOCK) \
              VALUES (4, 'Cherries', 11, 2)")      
        
        c.execute("INSERT INTO PRODUCT (ID,DESC,PRICE,STOCK) \
              VALUES (5, 'Lemon', 4, 12)")
              
        c.execute("INSERT INTO PRODUCT (ID,DESC,PRICE,STOCK) \
              VALUES (6, 'Mango', 5, 7)")
        
        c.execute("INSERT INTO PRODUCT (ID,DESC,PRICE,STOCK) \
              VALUES (7, 'Orange', 5, 5)")
              
        c.execute("INSERT INTO PRODUCT (ID,DESC,PRICE,STOCK) \
              VALUES (8, 'Pear', 7, 12)")
              
        c.execute("INSERT INTO PRODUCT (ID,DESC,PRICE,STOCK) \
              VALUES (9, 'Pineapple', 20, 2)")
              
        c.execute("INSERT INTO PRODUCT (ID,DESC,PRICE,STOCK) \
              VALUES (10, 'Raspberries', 15, 4)")
              
        conn.commit()
        conn.close()
    #get daytime 
    ntp = ntplib.NTPClient()
    response = ntp.request("time-a-g.nist.gov")
    INSTANCESYSTIME=response.tx_time
    #Convert time string to bytes
    time = time.ctime(INSTANCESYSTIME)
    exe_id = hashlib.sha256(time.encode("utf-8")).hexdigest()
    #set the lock
    lock = threading.Lock()
    app.run()
    
