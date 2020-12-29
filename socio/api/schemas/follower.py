from socio.models import Follower
from socio.extensions import ma, db
from socio.api.schemas.utils import ExtendModelConverter


class FollowerSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field(dump_only=True)
    created_timestamp = ma.auto_field(dump_only=True)

    class Meta:
        model = Follower
        sqla_session = db.session
        include_fk = True
        exclude = ("updated_timestamp",)
        model_converter = ExtendModelConverter
