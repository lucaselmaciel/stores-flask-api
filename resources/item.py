from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError


items_blueprint = Blueprint("Items", "items", description="Operations on items")

@items_blueprint.route("/item/<string:item_id>")
class Item(MethodView):
    @jwt_required()
    @items_blueprint.response(200, ItemSchema)
    def get(self, item_id):
        return ItemModel.query.get_or_404(item_id)

    @jwt_required()
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    @jwt_required()
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
    @jwt_required()
    @items_blueprint.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required()
    @items_blueprint.arguments(ItemSchema)
    @items_blueprint.response(201, ItemSchema)
    def post(self, item_data):
        
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError as e:
            abort(409, str(e))
        except SQLAlchemyError as exc:
            abort(500, "Register error")

        return item