import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError


items_blueprint = Blueprint("Items", "items", description="Operations on items")

@items_blueprint.route("/item/<string:item_id>")
class Item(MethodView):
    @items_blueprint.response(200, ItemSchema)
    def get(self, item_id):
        return ItemModel.query.get_or_404(item_id)

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    @items_blueprint.arguments(ItemUpdateSchema)
    @items_blueprint.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(**item_data)
        
        db.session.add(item)
        db.session.commit()

        return item


@items_blueprint.route("/item")
class ItemList(MethodView):
    @items_blueprint.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @items_blueprint.arguments(ItemSchema)
    @items_blueprint.response(201, ItemSchema)
    def post(self, item_data):
        
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as exc:
            abort(500, "Register error")

        return item