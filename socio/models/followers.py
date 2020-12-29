import enum
from datetime import datetime
from socio.extensions import db


class FollowerStatusEnum(enum.Enum):
    pending = 'pending'
    accepted = 'accepted'
    rejected = 'rejected'
    cancelled = 'cancelled'


class Follower(db.Model):
    """
    Users following each other by requests 
    """
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(
        db.Enum(FollowerStatusEnum),
        default=FollowerStatusEnum.pending,
        nullable=False
    )
    created_timestamp = db.Column(db.DateTime, nullable=False,
                                  default=datetime.utcnow)
    updated_timestamp = db.Column(db.DateTime, nullable=False,
                                  default=datetime.utcnow, onupdate=datetime.utcnow)
    from_user = db.relationship("User", lazy="joined", foreign_keys=[from_user_id])
    to_user = db.relationship("User", lazy="joined", foreign_keys=[to_user_id])
