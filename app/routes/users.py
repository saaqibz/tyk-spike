from app import app, db
from app.models.user import User
from flask import abort, jsonify, request
import datetime
import json
import pdb

@app.route('/api/user', methods = ['GET'])
def get_all_users():
    entities = User.query.all()
    return json.dumps([entity.to_dict() for entity in entities])

@app.route('/api/user/<int:id>', methods = ['GET'])
def get_user(id):
    entity = User.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())

@app.route('/auth/createuser', methods=['POST'])
@app.route('/api/user', methods = ['POST'])
def create_user():
    entity = User(
        email = request.json['email']
        , clientId = request.json['clientId']
        , password = request.json['password']
        , tokens = None
    )
    try:
        db.session.add(entity)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": e.message}), 400
    return jsonify(entity.to_dict()), 201

@app.route('/api/user/<int:id>', methods = ['PUT'])
def update_user(id):
    entity = User.query.get(id)
    if not entity:
        abort(404)
    entity = User(
        email = request.json['email'],
        password = request.json['password'],
        tokens = request.json['tokens'],
        id = id
    )
    db.session.merge(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 200

@app.route('/api/user/<int:id>', methods = ['DELETE'])
def delete_user(id):
    entity = User.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204



def add_token(email, cid, token):
    entity = User.query.filter(User.email==email, User.clientId==cid).first()
    if not entity:
        raise Exception('User Not Found')
    entity.tokens = token
    db.session.merge(entity)
    db.session.commit()