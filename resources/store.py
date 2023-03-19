from sqlite3 import IntegrityError
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_cors import CORS
from models.store import StoreModel
from schemas import PlainStoreSchema, StoreSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError

store_blueprint = Blueprint("stores", __name__, description="Operations on stores")
CORS(store_blueprint, origins=['http://localhost:4200'])

@store_blueprint.route("/store/<string:store_id>")
class Store(MethodView):
    @store_blueprint.response(200, StoreSchema)
    def get(self, store_id):
        return StoreModel.query.get_or_404(store_id)

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return "Store deleted successfully"

@store_blueprint.route("/store")
class StoreList(MethodView):
    @store_blueprint.response(200, StoreSchema(many=True))
    def get(self):
        return db.session.query(StoreModel, StoreModel.id, StoreModel.name, StoreModel.items).all()
    
    @store_blueprint.arguments(StoreSchema)
    @store_blueprint.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="")
        except SQLAlchemyError as sql_error:
            abort(500, message=f"Error when trying to create store {sql_error}")
        return store