# coding: utf-8
# b4sh REST-API
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin

from app.utils import *

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route("/")
@cross_origin(supports_credentials=True)
def _index():
    return render_template("index.html");


# /
@app.route('/api', methods=['GET'])
@cross_origin(supports_credentials=True)
def _api():
    # Build the response
    return jsonify({
        "status": "success",
        'message': "Welcome to b4sh API.",
        "description": "This API allows you to CRUD your bash commands and share it to others",
        "documentation": "https://documenter.getpostman.com/view/11958813/TVmHFL95"
    })


# bash
@app.route('/api/b', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def _create():
    if request.method == 'GET':
        result = get_all_publics_bash()
    elif request.method == 'POST':
        result = save_bash(request.json)
    else:
        result = {
            "status": "error",
            "code": "403",
            "message": "action not allow"
        }

    return result, result["code"]


# bash/bash-id
@app.route('/api/b/<bash_id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin(supports_credentials=True)
def _get_update_delete(bash_id):
    if request.method == 'GET':
        result = get_bash(bash_id, request.args.get("password"))
    elif request.method == 'DELETE':
        result = delete_bash(bash_id, request.args.get("password"))
    elif request.method == 'PUT':
        result = update_bash(bash_id, request.args.get("password"))
    else:
        result = {
            "status": "error",
            "code": "403",
            "message": "action not allow"
        }

    return result, result["code"]


# bash/raw/key
@app.route('/api/b/r/<key>', methods=['GET'])
@cross_origin(supports_credentials=True)
def _run(key):
    result = get_content_by_key(key)
    return result, result["code"]


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=4352)
