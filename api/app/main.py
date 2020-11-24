# coding: utf-8
# b4sh REST-API
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin

from app.utils import save_bash, get_bash, update_bash

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route("/")
@cross_origin(supports_credentials=True)
def _index():
    return render_template("index.html");


@app.route('/api', methods=['GET'])
@cross_origin(supports_credentials=True)
def _api():
    # Build the response
    return jsonify({
        "status": "success",
        'message': "Welcome to b4sh API.",
        "description": "This API allows you to CRUD your bash commands and share it to others",
        "documentation": ""
    })


@app.route('/api/b', methods=['POST'])
@cross_origin(supports_credentials=True)
def _create():
    result = save_bash(request.json)
    return result, result["code"]


@app.route('/api/b/<bash_id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin(supports_credentials=True)
def _get_update_delete(bash_id):
    result = {}
    if request.method == 'GET':
        result = get_bash(bash_id, request.args.get("password"))
    elif request.method == 'PUT':
        result = update_bash(bash_id, request.args.get("password"))

    return result, result["code"]


@app.route('/api/r/<bash_short_id>', methods=['GET'])
@cross_origin(supports_credentials=True)
def _run(bash_short_id):

    return {}


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=4352)
