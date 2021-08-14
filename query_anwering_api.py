import os
import sys
import time
import random
import pprint
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from magic_google import MagicGoogle
import trafilatura
import flask
from flask import request
from flask_cors import CORS
import json
import csv
import requests

app = flask.Flask(__name__)
CORS(app)

host = '0.0.0.0'
port = 9600
newHeaders = {'Content-type': 'application/json'}

PROXIES1 = [{
    'http': 'http://127.0.0.1:1087',
    'https': 'http://127.0.0.1:1087'
}]
PROXIES2 = None

# Or MagicGoogle()
mg = MagicGoogle(PROXIES2)
data = []
qa_url = "https://api.convai.com/qa_api"
genqa_url = "https://api.convai.com/gen_qa"
headers = {
    "Content-Type": "application/json"
}


@app.route("/query_answer_restricted", methods=["POST"])
def getRestrictedAnswer():
    data = request.get_json()
    genQA_flag = data["use_ans_extender"]
    start_time = time.time()
    results = []
    [results.append(trafilatura.extract(trafilatura.fetch_url(url)))
     for url in list(mg.search_url(query=data["question"]))[:1]]
    for pageData in results:
        payload = {"question": data["question"],
                   "input_context": pageData, "use_ans_extender": genQA_flag}
        response = requests.request(
            "POST", qa_url, headers=headers, json=payload)
        # response  = response.json()
        if(len(response["result"]) > 0):
            print("Time:", (time.time() - start_time))
            return json.dumps(response.json())

    return (json.dumps({"result": "", "context": "No possible context for the given query", "p": 1.0}))


@app.route("/query_answer", methods=["POST"])
def getAnswer():
    try:
        data = request.get_json()
        genQA_flag = data["use_ans_extender"]
        start_time = time.time()
        for url in list(mg.search_url(query=data["question"])):
            result = trafilatura.extract(trafilatura.fetch_url(url))
            payload = {"question": data["question"],
                       "input_context": result, }
            response = requests.request(
                "POST", qa_url, headers=headers, json=payload, verify=False)
            response = response.json()
            if len(response["result"]) > 0:
                payload = {
                    "question": data["question"],
                    "input_context": response["result"]
                }
                response = requests.request(
                    "POST", genqa_url, headers=headers, json=payload, verify=False)
                return json.dumps(response.json())
    
    except:
        return (json.dumps({"result": "Sorry. I don't have an answer to that.", "context": "No possible context for the given query", "p": 1.0}))


if __name__ == "__main__":
    app.run(host=host, port=port, debug=True,
            threaded=True, use_reloader=False)
