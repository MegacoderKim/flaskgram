from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

from socio.extensions import db, pwd_context


class User(db.Model):
    """Basic user model"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    first_name = db.Column(db.String(200), nullable=True)
    last_name = db.Column(db.String(200), nullable=True)
    profile_description = db.Column(db.Text, nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)

    created_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    updated_timestamp = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def __repr__(self):
        return f"<User {self.username}>"
