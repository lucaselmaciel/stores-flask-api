from marshmallow import Schema, fields, post_load
from models.item import ItemModel
from models.store import StoreModel


class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class ItemUpdateSchema(Schema):
    price = fields.Float()
    name = fields.Str(required=True)
    store_id = fields.Int()


class PlainStoreSchema(Schema):
    class Meta:
        model: StoreModel

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class ItemSchema(PlainItemSchema):
    class Meta:
        model: ItemModel

    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema)
    tags = fields.Nested(PlainTagSchema, dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()))
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)