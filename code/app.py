# simple json api

# for full breakdown see https://github.com/davekznza/challenge/blob/main/1-code.md  

from flask import Flask, request, Response, jsonify
import os, shutil, json

app = Flask(__name__)

@app.route('/system', methods=["GET"])
def system():
    load1, load5, load15 = os.getloadavg()
    total, used, free = shutil.disk_usage("/")
    data = { 
        "load_avg": { '1m': load1, '5m': load5, '15m': load15 },
        "disk_usage": { 'total_gb': total // (2**30), 'used_gb': used // (2**30), 'free_gb': free // (2**30)}
    }
    return jsonify(data), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/tech_assess',methods = ['POST', 'GET'])
def tech_assess():
    if request.method == 'POST':
        request_json = request.get_json()
        updated_value = request_json.get('value')
        with open('./tech_assess.json', 'r') as tech_assess_json:
            tech_assess_data = json.load(tech_assess_json)
        tech_assess_data["tech"]["return_value"] = updated_value
        with open("tech_assess.json", "w") as tech_assess_json:
            json.dump(tech_assess_data, tech_assess_json)
        return jsonify(value=updated_value), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        with open('./tech_assess.json', 'r') as tech_assess_json:
            tech_assess_data = json.load(tech_assess_json)
        return jsonify(tech_assess_data), 200, {'Content-Type': 'application/json; charset=utf-8'}
