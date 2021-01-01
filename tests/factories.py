import factory
from socio.models import User, Post, Comment


class UserFactory(factory.Factory):

    username = factory.Sequence(lambda n: "user%d" % n)
    email = factory.Sequence(lambda n: "user%d@mail.com" % n)
    password = "mypwd"

    class Meta:
        model = User


class PostFactory(factory.alchemy.SQLAlchemyModelFactory):

    title = factory.Sequence(lambda n: "title_%d" % n)
    body = factory.Sequence(lambda n: "post body_%d" % n)
    user_fk = factory.SubFactory(UserFactory)

    class Meta:
        model = Post


class CommentFactory(factory.alchemy.SQLAlchemyModelFactory):
    body = factory.Sequence(lambda n: "comment body_%d" % n)
    user_fk = factory.SubFactory(UserFactory)
    post_fk = factory.SubFactory(PostFactory)

    class Meta:
        model = Post
