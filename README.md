# FlaskServer

File names:
-server.py
The server program provides web services for managing the product data.
Including:
        -find a product using input id
        -buy a product using input id, credit card number, and quantity
        -replenish a product using input id and quantity


-testcase.py
Have some test cases to test the server function like find_product, buy_product, and replenish_product.
-product_data.db (will be built when first time run the server)
store the product data


Instructions for setting up and executing the application


Import module:
-Flask from flask How to install: pip install Flask
Use the flask to create the app and make the web

-jsonify from flask
How to install: pip install Flask
Make the web server response return JSON formatted data.

-request from flask
How to install: pip install Flask
Make the web server have the GET, PUT function to get the request.

-ntplib
How to install: install python-ntplib
Offers a simple interface to query NTP servers from Python.

-time
How to install: pip install python-time
Converts a time expressed in seconds since the epoch to a string representing local time.

-hashlib
How to install: pip install hashlib
Convert the time string to bytes, and find the SHA256 checksum of the bytes.

-sqlite3
How to install: pip install pysqlite3
A built-in SQLite function of python to save the data.

-threading
How to install: pip install threading
Threading can run multiple I/O-bound tasks simultaneously.

Executing the application:
The first time who runs the server that will create the database file. The user can use the product id to get all attributes. In curl, the user can input commands like
“curl http://localhost:5000/find/1” to get the product1 attributes. Then, the server will return the execution ID and JSON formatted responses. Second, when the user wants to buy a product, the user can input a product id, a quantity
to buy, and a credit card number. In curl, the user can input commands like “curl -d "{\"id\":1,\"quantity\":1,\"card\":\"WERDFRGTYFGTRHYU\"}" -H "Content-Type: application/json" -X PUT http://localhost:5000/buy” to buy a product. In addition, the user can input a product ID and a quantity to replenish the stock of the product, and then update the quantity in the database. In curl, the user can input commands like “curl -d "{\"id\":1,\"quantity\":1}" -H "Content-Type: application/json" -X PUT http://localhost:5000/replenish” to update the stock of the product.

Instructions for setting up and executing the unit tests

Import module:
-json
How to install: installed by default
The encoder and decoder for JSON format.

-unittest
How to install: installed by default
The unittest unit testing framework supports test automation, sharing of setup, and shutdown code for tests.

-HTTPError from urllib.error
How to install: installed by default
An HTTPError allows the program to handle the exception without terminating the program.

-Request from urllib.request
How to install: pip install urllib3
The request indicates the HTTP request to be generated.

-urlopen from urllib.request
How to install: pip install urllib3
The urlopen get the return data from the website

Executing the application:
When the server is running, we can run the test case file to test the different situations in the server. First, the first test case to test a query about a product returns the correct product attributes. Second, we will test whether buying a product with sufficient stock in the server succeeds and the quantity in stock is updated and buying a product with insufficient stock in the server fails and the quantity in stock remains unchanged. Next, we will test replenishing a product and update the database’s quantity in stock. Then, test the input issue, when the product ID does not exist, the server returns the 404 status code, and when some required input data is missing or invalid, the server returns the 400 status code. Finally, has a test case to test when the two requests for buying the same product arrive almost simultaneously and the quantity in stock is insufficient for the second request, the server must not mistakenly fulfill the second request.
