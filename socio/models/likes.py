from datetime import datetime
from socio.extensions import db


class Like(db.Model):
    """
    A database like object
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    created_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_timestamp = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    user = db.relationship("User", lazy="joined")
    post = db.relationship("Post", lazy="joined")

    def __repr__(self):
        return f"<Like:{self.id}"
