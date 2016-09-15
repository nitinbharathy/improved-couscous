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
        
        
    print("step 0")
    
    sessionId = req.get("sessionId")
    result = req.get("result")
    parameters = result.get("parameters")
    
    
    print("step 1")
    print(sessionId)
    generic_category_query = parameters.get("generic_category_query")
    
    print("step 2")

    # cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}
    
    menutable={'vegetarian':'We just launched the veggie crunch','chicken':'The mc chicken and mc spicy are good choices','burger':'You should try the big mac or the mc spicy','beef':'Peoples favourites are the cheeseburger or the big mac','recommendations':'Please do not eat here - cook your own food!'}

    # speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."
    speech = "You asked for " + generic_category_query + ". "+ menutable[generic_category_query]+" for session "+ sessionId + "."
    
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
