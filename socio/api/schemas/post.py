from socio.models import Post
from socio.extensions import ma, db


class PostSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field(dump_only=True)
    created_timestamp = ma.auto_field(dump_only=True)

    class Meta:
        model = Post
        sqla_session = db.session
        include_fk = True
        load_instance = True
        exclude = ("updated_timestamp",)


class PostUpdateSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field(dump_only=True)
    user_id = ma.auto_field(dump_only=True)
    created_timestamp = ma.auto_field(dump_only=True)

    class Meta:
        model = Post
        sqla_session = db.session
        include_fk = True
        load_instance = True
        exclude = ("updated_timestamp",)
