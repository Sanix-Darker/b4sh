# coding: utf-8
# b4sh REST-API
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin

from app.utils import *

app = Flask(__name__)
CORS(app, support_credentials=True)


# /
@app.route("/")
@cross_origin(supports_credentials=True)
def _index():
    return render_template("index.html")


# /api/
@app.route('/api', methods=['GET'])
@cross_origin(supports_credentials=True)
def _api():
    # Build the response
    return jsonify({
        "status": "success",
        'message': "Welcome to b4sh API.",
        "description": "This API allows you to CRUD your bash commands and share it to others.",
        "documentation": "https://documenter.getpostman.com/view/11958813/TVmJhJmA"
    })


# /api/bash
@app.route('/api/b', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def _create():
    try:
        if request.method == 'GET':
            result = get_all_publics_bash()
        elif request.method == 'POST':
            # Check if there is a parameter depends on and then add it or revoke
            result = save_bash(request.json)
        else:
            result = {
                "code": "403",
                "reason": "Action not allow!"
            }
    except Exception as es:
        get_trace()
        result = {
            "code": "500",
            "reason": "An error occur, please check logs!"
        }

    return result, result["code"]


# /api/bash/bash-id
@app.route('/api/b/<bash_id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin(supports_credentials=True)
def _get_update_delete(bash_id):
    try:
        if request.method == 'GET':
            result = get_bash(bash_id, request.args.get("password"))
        elif request.method == 'DELETE':
            result = delete_bash(bash_id, request.args.get("password"))
        elif request.method == 'PUT':
            result = update_bash(bash_id, request.json, request.args.get("password"))
        else:
            result = {
                "code": "403",
                "reason": "Action not allow!"
            }
    except Exception as es:
        get_trace()
        result = {
            "code": "500",
            "reason": "An error occur, please check logs!"
        }

    return result, result["code"]


# /api/bash/raw/key
@app.route('/api/b/r/<key>', methods=['GET'])
@cross_origin(supports_credentials=True)
def _run(key):
    try:
        result = get_content_by_key(key)
    except Exception as es:
        get_trace()
        result = {
            "code": "500",
            "reason": "An error occur, please check logs!"
        }

    return result, result["code"]


# /api/bash/up-vote/key
@app.route('/api/b/up/<key>', methods=['PATCH'])
@cross_origin(supports_credentials=True)
def _up(key):
    try:
        result = up_vote(key)
    except Exception as es:
        get_trace()
        result = {
            "code": "500",
            "reason": "An error occur, please check logs!"
        }

    return result, result["code"]


# /api/bash/down-vote/key
@app.route('/api/b/down/<key>', methods=['PATCH'])
@cross_origin(supports_credentials=True)
def _down(key):
    try:
        result = down_vote(key)
    except Exception as es:
        get_trace()
        result = {
            "code": "500",
            "reason": "An error occur, please check logs!"
        }

    return result, result["code"]


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=4352)
