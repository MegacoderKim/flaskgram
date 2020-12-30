from socio.models import Post
from socio.extensions import ma, db


class PostSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field(dump_only=True)
    created_timestamp = ma.auto_field(dump_only=True)

    class Meta:
        model = Post
        sqla_session = db.session
        include_fk = True
        exclude = ("updated_timestamp",)