from datetime import datetime
from socio.extensions import db


class Post(db.Model):
    """
    A database post object
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(200), nullable=True)
    body = db.Column(db.Text, nullable=True)
    created_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_timestamp = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    user = db.relationship("User", lazy="joined")

    def __repr__(self):
        return f"<Post:{self.title}"
