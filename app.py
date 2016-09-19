#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
    

def makeWebhookResult(req):
    
    validApiActionList=["generic.queries","dummy"]
    
    if req.get("result").get("action") not in validApiActionList:
        return {}
    
    if req.get("result").get("action")=="generic.queries":
        return functionGenericQueries(req)
    elif:
        return functionOrder(req)
    
def functionOrder(req):
    sessionId = req.get("sessionId")
    result = req.get("result")
    parameters = result.get("parameters")

    process_order=parameters.get("process_order")
    
    speech = "You asked for " + process_order + "."
    
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-generic-queries"
    }
    
    
def functionGenericQueries(req):
    sessionId = req.get("sessionId")
    result = req.get("result")
    parameters = result.get("parameters")

    generic_category_query = parameters.get("generic_category_query")
    
    menutable={'vegetarian':'We just launched the veggie crunch','chicken':'The mc chicken and mc spicy are good choices','burger':'You should try the big mac or the mc spicy','beef':'Peoples favourites are the cheeseburger or the big mac','recommendations':'Please do not eat here - cook your own food!'}

    speech = "You asked for " + generic_category_query + ". "+ menutable[generic_category_query]+" for session "+ sessionId + "."
    
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-generic-queries"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
