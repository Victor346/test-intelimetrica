from flask import Flask


app = Flask(__name__)

import test_intelimetrica.routes
#This flask app will be used to expose the CRUD API as well as the other special endpoints
#Note: All endpoints in this app will return valid JSON data to allow better integration with the client side


