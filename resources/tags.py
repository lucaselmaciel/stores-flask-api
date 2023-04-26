from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blue_print = Blueprint("Tags", "tags", description="Operations on tags")


@blue_print.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):
    @blue_print.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blue_print.arguments(TagSchema)
    @blue_print.response(201, TagSchema)
    def post(self, tag_data, store_id):
        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag


@blue_print.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @blue_print.response(200, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        try:
            item.tags.append(tag)
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as exp:
            abort(500, message=exp)

        return tag


@blue_print.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blue_print.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
