from socio.models import Comment
from socio.extensions import ma, db


class CommentSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field(dump_only=True)
    created_timestamp = ma.auto_field(dump_only=True)

    class Meta:
        model = Comment
        sqla_session = db.session
        include_fk = True
        load_instance = True
        exclude = ("updated_timestamp",)


class CommentUpdateSchema(ma.SQLAlchemyAutoSchema):
    id = ma.auto_field(dump_only=True)
    user_id = ma.auto_field(dump_only=True)
    post_id = ma.auto_field(dump_only=True)
    created_timestamp = ma.auto_field(dump_only=True)

    class Meta:
        model = Comment
        sqla_session = db.session
        include_fk = True
        load_instance = True
        exclude = ("updated_timestamp",)
