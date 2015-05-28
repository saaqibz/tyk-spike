from app import app, db
from app.models import item
from flask import abort, jsonify, request
import datetime
import json
from index import crossdomain

@app.route('/api/items', methods = ['GET', 'OPTIONS'])
@crossdomain(origin="*")
def get_all_items():
    entities = item.Item.query.all()
    return json.dumps([entity.to_dict() for entity in entities])

@app.route('/api/items/<int:id>', methods = ['GET'])
def get_item(id):
    entity = item.Item.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())

@app.route('/api/items', methods = ['POST', 'OPTIONS'])
@crossdomain(origin="*")
def create_item():
    entity = item.Item(
        name = request.json['name']
        , description = request.json['description']
        , thumbnail = request.json['thumbnail']
    )
    db.session.add(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 201

@app.route('/api/items/<int:id>', methods = ['PUT'])
def update_item(id):
    entity = item.Item.query.get(id)
    if not entity:
        abort(404)
    entity = item.Item(
        id = request.json['id'],
        name = request.json['name'],
        description = request.json['description'],
        thumbnail = request.json['thumbnail'],
    )
    db.session.merge(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 200

@app.route('/api/items/<int:id>', methods = ['DELETE'])
def delete_item(id):
    entity = item.Item.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204
