from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy.exc import IntegrityError

from db import db
from models import UserModel
from schemas import UserSchema


blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/register")
class UsersRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        try:
            user = UserModel(**user_data)
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            return {"message": "This user name is already registered, please try another"}, 409
        except Exception as exc:
            return str(exc), 400

        return user
    

@blp.route("/user/<int:user_id>")
class User(MethodView):

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "Deleted successfully"}, 203