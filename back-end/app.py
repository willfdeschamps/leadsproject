from flask import Flask
from flask import request as req
from flask import json

from controllers.lead import data as lead_data
from controllers.lead import lead as lead_insert

import datetime


app = Flask(__name__)

#TODO criar função para ler a requisição
@app.route('/lead', methods=['POST'])
def lead():
    return lead_insert()

@app.route('/data', methods=['GET'])
def data():
    return lead_data()

if __name__ == '__main__':
    app.run()