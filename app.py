#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from flask import Flask, session, render_template, url_for, request, redirect


# Flask app should start in global layout
app = Flask(__name__)

app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KTheythere'

def sumSessionCounter():
  try:
    session['counter'] += 1
  except KeyError:
    session['counter'] = 1


@app.route('/webhook', methods=['POST'])
def webhook():
    sumSessionCounter()
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
    
    validApiActionList=["generic.queries","process.order"]
    
    #if req.get("result").get("action") not in validApiActionList:
    #    return {}
    
    print("starting...")
    print req.get("result").get("action")
    
    print("the counter is")
    print session['counter']
    
    if req.get("result").get("action")=="generic.queries":
        print("here 1")
        print session['counter']
        return functionGenericQueries(req)
    elif req.get("result").get("action")=="process.order":
        print("here B-2")
        print session['counter']
        return functionOrder(req)
    else:
        print("Invalid API.AI Action: ")
        print req.get("result").get("action")
        print("Returning")
        return {}
        
    
def functionOrder(req):
    sessionId = req.get("sessionId")
    result = req.get("result")
    parameters = result.get("parameters")
    
    amt=parameters.get("amount").get("amount")
    burger=parameters.get("burger").get("burger")
    cust=parameters.get("customisation").get("customisation")
    
    session['counter'] = session['counter'] + 1
    
    speech = "You asked for " + str(amt) + " quantity of " + burger + " with " + cust + " customisations. Would you like to make this a meal? " + str(session['counter'])
    
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
    print("here 2")
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
