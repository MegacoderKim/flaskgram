from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from socio.api.schemas import PostSchema
from socio.models import Post
from socio.extensions import db
from socio.commons.pagination import paginate


class PostResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: post_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  user: PostSchema
        404:
          description: post does not exists
    put:
      tags:
        - api
      parameters:
        - in: path
          name: post_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              PostSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: post updated
                  user: PostSchema
        404:
          description: post does not exists
        400:
          description: only owner can update post
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: post_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: post deleted
        404:
          description: post does not exists

    """
    method_decorators = [jwt_required]

    def get(self, post_id):
        schema = PostSchema()
        post = Post.query.get_or_404(post_id)
        return {"post": schema.dump(post)}

    def put(self, post_id):
        owner = get_jwt_identity()
        schema = PostSchema(partial=True)
        post = Post.query.get_or_404(post_id)
        if post.user_id != owner:
            return {"msg": "only owner can update post"}, 400
        post = schema.load(request.json, instance=post)
        db.session.commit()

        return {"msg": "post updated", "post": schema.dump(post)}

    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()

        return {"msg": "post deleted"}


class PostList(Resource):
    """Creation and get_all
    ---
    get:
      tags:
        - api
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/PostSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              PostSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: post created
                  user: PostSchema
    """

    method_decorators = [jwt_required]

    def get(self):
        schema = UserSchema(many=True)
        query = User.query
        return paginate(query, schema)

    def post(self):
        schema = PostSchema()
        post = schema.load(request.json)
        db.session.add(post)
        db.session.commit()

        return {"msg": "post created", "post": schema.dump(post)}, 201
