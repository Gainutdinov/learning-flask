from flask import Flask, jsonify, request, Response
from MovieModel import *
from settings import *
import json

import jwt, datetime
from UserModel import User
from functools import wraps

movies = Movie.get_all_movies()

DEFAULT_PAGE_LIMIT = 3

app.config['SECRET_KEY'] = 'secret'

@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])

    match = User.username_password_match(username, password)
    
    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response('', 401, mimetype='application/json')

    

# GET /movies/page/<int:page_number>
# GET /movies?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MzA5NzU5NjZ9.MgTNDJJEqafaICiftiNXeYwD6nHdU1G6LIadKkA8BfQ
#/movies/page/1?limit=100
@app.route('/movies/page/<int:page_number>')
def get_paginated_movies(page_number):
    print(type(request.args.get('limit')))
    LIMIT = request.args.get('limit', DEFAULT_PAGE_LIMIT, int)
    startIndex = page_number*LIMIT-LIMIT
    endIndex = page_number*LIMIT
    print(startIndex)
    print(endIndex)
    return jsonify({'movies': movies[startIndex:endIndex]})

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Need a valid token to view this page'}), 401
    return wrapper

#POST /movies
# {
#     'name': 'B',
#     'price': 6.99,
#     'identity': 1122334455    
# }

@app.route('/movies')
@token_required
def get_movies():
    return jsonify({'movies': movies})

def validMovieObject(movieObject):
    if ("name" in movieObject and "price" in movieObject and "identity" in movieObject):
        return True
    else:
        return False

#/movies/identity_number

@app.route('/movies', methods=['POST'])
def add_movie():
    request_data = request.get_json()
    if(validMovieObject(request_data)):
        Movie.add_movie(request_data['name'], request_data['price'], request_data['identity'])
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/movies/" + str(request_data['identity'])
        return response
    else:
        invalidMovieObjectErrorMsg = {
            "error": "Invalid movie object passed in request",
            "helpString": "Data passed in similar to this {'name': 'moviename', 'price':7.99, 'identity':1234567890}"
        }
        response = Response(json.dumps(invalidmovieObjectErrorMsg), status=400, mimetype='application/json')
        return response

def valid_put_request_data(request_data):
    if("name" in request_data and "price" in request_data):
        return True
    else:
        return False

def valid_patch_request_data(request_data):
    if("name" in request_data or "price" in request_data):
        return True
    else:
        return False

@app.route('/movies/<int:identity>')
def get_movie_by_identity(identity):
    return_value = Movie.get_movie(identity)
    return jsonify(return_value)

#PATCH  /movies/91283127313
# {
#     'name': 'The homer',
#     'price': 0.88
# }

#PUT
@app.route('/movies/<int:identity>', methods=['PUT'])
def replace_movie(identity):
    request_data = request.get_json()
    if(not valid_put_request_data(request_data)):
        invalidMovieObjectErrorMsg = {
            "error": "Valid movie object must be passed in the request",
            "helpString": "Data passed in similar to this {'name':'moviename', 'price':7.99}"
        }
        response = Response(json.dumps(invalidMovieObjectErrorMsg), status=400, mimetype='application/json')
        return response

    Movie.replace_movie(identity, request_data['name'], request_data['price'])
    response = Response("", status=204)
    return response

# PATCH /movies/1238193871293
# {
#   'price': 39.99
# }

@app.route('/movies/<int:identity>', methods=['PATCH'])
def update_movie(identity):
    request_data = request.get_json()
    if(not valid_patch_request_data(request_data)):
        invalidMovieObjectErrorMsg({
            "error": "Invalid movie object passed in request",
            "helpString": "Data should be passed in similar to this {'name':'moviename', 'price':'7.99'}"
        })
        response = Response(json.dumps(invalidMovieObjectErrorMsg), status=400, mimetype='application/json')
        return Response
    if("name" in request_data):
        Movie.update_movie_name(identity, request_data['name'])
    if("price" in request_data):
        Movie.update_movie_price(identity, request_data['price'])
    response = Response("", status=204)
    response.headers['Location'] = "/movies/" + str(identity)
    return response

# DELETE /movies/110987654321
# Body: {'name': 'asdfasdf'}

@app.route('/movies/<int:identity>', methods=['DELETE'])
def delete_movie(identity):
    if(Movie.delete_movie(identity)):
        response = Response("", status=204)
        return response
    invalidMovieObjectErrorMsg = {
        "error": "Movie with the identity number that was provided was not found, so therefore unable to delete"
    }
    response = Response(json.dumps(invalidMovieObjectErrorMsg), status=404, mimetype='application/json')
    return response



app.run(port=5000)