#!/usr/bin/env python3

import psutil
from flask import Flask, jsonify

app = Flask(__name__)
 
@app.route('/')
def startowa():
    return '<h1>Strona startowa</h1> \n Inne odnosniki: /version, /cpu'

@app.route('/version')
def check_ver():
    return 'Version: [0.1]'

@app.route('/cpu/', methods=['GET'])
def cpu_info():
    cpus = [
        {'liczba cpu':psutil.cpu_count()},
        {'statyski cpu':psutil.cpu_stats()}
    ]
    return jsonify(cpus)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
