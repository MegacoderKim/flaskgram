from socio.models import Like
from socio.extensions import ma, db


class LikeSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field(dump_only=True)
    created_timestamp = ma.auto_field(dump_only=True)

    class Meta:
        model = Like
        sqla_session = db.session
        include_fk = True
        load_instance = True
        exclude = ("updated_timestamp",)


class LikeUpdateSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)
    user_id = ma.auto_field(dump_only=True)
    post_id = ma.auto_field(dump_only=True)
    created_timestamp = ma.auto_field(dump_only=True)

    class Meta:
        model = Like
        sqla_session = db.session
        include_fk = True
        load_instance = True
        exclude = ("updated_timestamp",)
