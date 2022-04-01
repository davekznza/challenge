# Code

## Overview

Create python3 virtual environment and install Flask:
```sh
$ cd ~/
$ python3 -m venv myapi
$ cd ~/myapi
$ source bin/activate

(myapi) $ pip3 install flask
(myapi) $ vim app.py
```

app.py
```python
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

```

Run the app, this binds it to http://localhost:5555/:
```sh
(venv) python3 -m flask run -h 127.0.0.1 -p 5555

 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5555/ (Press CTRL+C to quit)
 
127.0.0.1 - - [31/Mar/2022 21:25:19] "GET / HTTP/1.1" 200 -

^C
```

## Tests

### GET /system

Returns avg server load & avail disk space on current fs

```sh
$ curl -H "Content-Type: application/json" -X GET http://localhost:5555/system
{"disk_usage":{"free_gb":152,"total_gb":231,"used_gb":66},"load_avg":{"15m":0.58,"1m":0.65,"5m":0.53}}
```

### GET /tech_assess

Returns value of the key called `return_value` in file `tech_assess.json`

```sh
$ cat tech_assess.json 
{"tech": {"return_value": "1337"}}

$ curl -H "Content-Type: application/json" -X GET http://localhost:5555/tech_assess 
{"tech":{"return_value":"1337"}}
```

### POST /tech_assess

Overwrites value of key called `return_value` in file `tech_assess.json`. This results in `GET /tech_assess` returning the new value previously written.

```sh
$ cat tech_assess.json 
{"tech": {"return_value": "1337"}}

$ curl -d '{"value":"12345"}' -H "Content-Type: application/json" -X POST http://localhost:5555/tech_assess
{"value":"12345"}

$ curl -H "Content-Type: application/json" -X GET http://localhost:5555/tech_assess 
{"tech":{"return_value":"12345"}}
```