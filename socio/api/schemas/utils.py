from sqlalchemy.types import Enum
from marshmallow import fields
from marshmallow_sqlalchemy import ModelConverter


class EnumField(fields.Field):
    """
    Support serialization of enum types by marshmallow
    """

    def __init__(self, *args, **kwargs):
        self.column = kwargs.get('column')
        super(EnumField, self).__init__(*args, **kwargs)

    def _serialize(self, value, attr, obj):
        field = super(EnumField, self)._serialize(value, attr, obj)
        return field.name if field else field

    def deserialize(self, value, attr=None, data=None, **kwargs):
        field = super(EnumField, self).deserialize(value, attr, data)
        if isinstance(field, str) and self.column is not None:
            return self.column.type.python_type[field]
        return field


class ExtendModelConverter(ModelConverter):
    SQLA_TYPE_MAPPING = {
        **ModelConverter.SQLA_TYPE_MAPPING,
        Enum: EnumField,
    }

    def _add_column_kwargs(self, kwargs, column):
        super()._add_column_kwargs(kwargs, column)
        if hasattr(column.type, 'enums'):
            kwargs['column'] = column
