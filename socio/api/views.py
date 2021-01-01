from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from socio.extensions import apispec
from socio.api.resources import UserResource, UserList, FollowerResource, PostList, PostResource, CommentList, CommentResource
from socio.api.schemas import UserSchema, FollowerSchema, PostSchema, CommentSchema


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")
api.add_resource(FollowerResource, "/followers/<int:follower_id>", endpoint="follower_by_id")
api.add_resource(PostResource, "/posts/<int:post_id>", endpoint="post_by_id")
api.add_resource(PostList, "/posts", endpoint="posts")
api.add_resource(CommentResource, "/comments/<int:comment_id>", endpoint="comment_by_id")
api.add_resource(CommentList, "/comments", endpoint="comments")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)
    apispec.spec.components.schema("FollowerSchema", schema=FollowerSchema)
    apispec.spec.path(view=FollowerResource, app=current_app)
    apispec.spec.components.schema("PostSchema", schema=PostSchema)
    apispec.spec.path(view=PostResource, app=current_app)
    apispec.spec.path(view=PostList, app=current_app)
    apispec.spec.components.schema("CommentSchema", schema=CommentSchema)
    apispec.spec.path(view=CommentResource, app=current_app)
    apispec.spec.path(view=CommentList, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
