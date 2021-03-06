from socio.models import User
from socio.extensions import ma, db


class UserSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    password = ma.String(load_only=True, required=True)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ("_password", "created_timestamp", "updated_timestamp")

    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("api.user_by_id", values=dict(user_id="<id>")),
            "collection": ma.URLFor("api.users"),
        }
    )
