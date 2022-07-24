import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES


@app.route('/drinks', methods=['GET'])
def get_all_drinks():
    selection = Drink.query.order_by(Drink.id).all()
    drinks = [drink.short() for drink in selection]
    return {
        "success": True,
        "drinks": drinks
        }


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_all_drinks_detail(jwt):
    selection = Drink.query.order_by(Drink.id).all()
    drinks = [drink.long() for drink in selection]
    return {
        "success": True,
        "drinks": drinks
        }


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drink(jwt):
    body = request.get_json()
    title = body['title']
    recipe = body['recipe']
    recipe = json.dumps(recipe)
    try:
        drink = Drink(title=title, recipe=recipe)
        drink.insert()
        drink = [drink.long()]
        return {
            "success": True,
            "drinks": drink
            }
    except Exception:
        abort(422)


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, id):
    body = request.get_json()
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink is None:
        abort(404)
    try:
        if 'title' in body:
            drink.title = body['title']
        if 'recipe' in body:
            drink.recipe = json.dumps(body['recipe'])
        drink.update()

        drink2 = Drink.query.filter(Drink.id == id).one_or_none()
        if drink2 is None:
            abort(404)
        return {
            "success": True,
            "drinks": [drink2.long()]
            }
    except Exception:
        abort(422)


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink is None:
            abort(404)
        drink.delete()
        return jsonify({
            "success": True,
            "delete": id
        })
    except Exception:
        abort(422)

# Error Handling


'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
        }), 500


@app.errorhandler(AuthError)
def handle_auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error["description"]
    }), error.status_code
