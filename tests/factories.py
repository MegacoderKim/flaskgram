from datetime import datetime
import factory
from socio.extensions import db
from socio.models import User, Post, Comment, Like


class UserFactory(factory.Factory):

    username = factory.Sequence(lambda n: "user%d" % n)
    email = factory.Sequence(lambda n: "user%d@mail.com" % n)
    password = "mypwd"

    class Meta:
        model = User


class PostFactory(factory.alchemy.SQLAlchemyModelFactory):

    title = factory.Sequence(lambda n: "title_%d" % n)
    body = factory.Sequence(lambda n: "post body_%d" % n)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Post
        sqlalchemy_session = db.session


class CommentFactory(factory.alchemy.SQLAlchemyModelFactory):
    body = factory.Sequence(lambda n: "comment body_%d" % n)
    created_timestamp = factory.LazyFunction(datetime.now)
    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)

    class Meta:
        model = Comment
        sqlalchemy_session = db.session


class LikeFactory(factory.alchemy.SQLAlchemyModelFactory):
    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
    created_timestamp = factory.LazyFunction(datetime.now)

    class Meta:
        model = Like
        sqlalchemy_session = db.session
