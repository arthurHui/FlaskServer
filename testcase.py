import json, unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

#server location
SERVER = "localhost:5000"

def ws_client(url, method=None, data=None):
    #check the method
    if not method:
        method = "POST" if data else "GET"
    #check the data
    if data:
        data = json.dumps(data).encode("utf-8")
    headers = {"Content-type": "application/json; charset=UTF-8"} \
                if data else {}
    req = Request(url=url, data=data, headers=headers, method=method)
    #get the result from request
    with urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result

class TestServer(unittest.TestCase):

    #Test produst returns
    def test_find_item(self):
        id = 1
        list_resp = ws_client(f"http://{SERVER}/find/{id}")
        #test correct product attributes
        self.assertIsNotNone(list_resp[1]["id"])
        self.assertIsNotNone(list_resp[1]["desc"])
        self.assertIsNotNone(list_resp[1]["price"])
        self.assertIsNotNone(list_resp[1]["stock"])
    
    #Test buying a product with sufficient stock in the server succeeds
    def test_buy_item_success(self):
        id = 1
        #get the stock before buy
        list_resp = ws_client(f"http://{SERVER}/find/{id}")
        num_before_buy = list_resp[1]["stock"]
        buy_resp = ws_client(f"http://{SERVER}/buy", "PUT", {"id":1,"quantity": 1,"card":"GFRWJHYTHEWDFSFE"})  
        #check quantity in stock is updated
        if num_before_buy >= 1:
            self.assertEqual(num_before_buy - 1, buy_resp[1]["stock"])
        
    #Test buying a product with insufficient stock in the server fails
    def test_buy_item_unsuccess(self):
        id = 1
        list_resp = ws_client(f"http://{SERVER}/find/{id}")
        #set the buynum always greater than stock
        buynum = list_resp[1]["stock"] + 1
        #get the stock before buy
        num_before_buy = list_resp[1]["stock"]
        buy_resp = ws_client(f"http://{SERVER}/buy", "PUT", {"id":1,"quantity": buynum,"card":"GFRWJHYTHEWDFSFE"})
        #check quantity in stock remains unchanged
        self.assertEqual(num_before_buy, buy_resp[1]["stock"])
        
    #Test replenish a produst
    def test_replenish_item(self):
        id = 1
        replenishnum = 1
        #get the stock before buy
        list_resp = ws_client(f"http://{SERVER}/find/{id}")
        num_before_replenish = list_resp[1]["stock"]
        replenish_resp = ws_client(f"http://{SERVER}/replenish", "PUT", {"id":1,"quantity": replenishnum})
        #check quantity in stock is updated
        self.assertEqual(num_before_replenish + 1, replenish_resp[1]["stock"])
        
    #Test product ID does not exist
    def test_find_item_error(self):
        try:
            #set the not exist id
            id = 999
            ws_client(f"http://{SERVER}/find/{id}")
            self.assertTrue(False)
        except HTTPError as e:
            #return 404 status code
            self.assertEqual(404, e.code)
     
    #Test required input data are invalid
    def test_buy_item_error(self):
        try:
            #set the invalid buynum
            buynum = "wewr"
            ws_client(f"http://{SERVER}/buy", "PUT", {"id":1,"quantity": buynum,"card":"GFRWJHYTHEWDFSFE"})
            self.assertTrue(False)
        except HTTPError as e:
            #return 400 status code
            self.assertEqual(400, e.code)
        
    #Test required input data are missing
    def test_buy_item_error2(self):
        try:
            #set the missing buynum
            buynum = ""
            ws_client(f"http://{SERVER}/buy", "PUT", {"id":1,"quantity": buynum,"card":"GFRWJHYTHEWDFSFE"})
            self.assertTrue(False)
        except HTTPError as e:
            #return 400 status code
            self.assertEqual(400, e.code)

    #avoid mistakenly fulfill the second request
    def test_two_request_buy(self):
        
        id = 1
        list_resp = ws_client(f"http://{SERVER}/find/{id}")
        #get the stock before buy
        num_before_buy = list_resp[1]["stock"]
        #two request 
        buy_resp_1 = ws_client(f"http://{SERVER}/buy", "PUT", {"id":1,"quantity": 1,"card":"GFRWJHYTHEWDFSFE"})  
        buy_resp_2 = ws_client(f"http://{SERVER}/buy", "PUT", {"id":1,"quantity": 1,"card":"GFRWJHYTHEWDFSFE"})
        #Do the checking when last stock
        if num_before_buy == 1:
            self.assertEqual("success", buy_resp_1[1]["status"])
            self.assertEqual("unsuccess", buy_resp_2[1]["status"])

if __name__ == "__main__":
    unittest.main()
