from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from webargs import fields
from webargs.flaskparser import parser
from socio.api.schemas import CommentSchema, CommentUpdateSchema
from socio.models import Comment
from socio.extensions import db
from socio.commons.pagination import paginate


class CommentResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: comment_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  comment: CommentSchema
        404:
          description: Comment does not exists
    put:
      tags:
        - api
      parameters:
        - in: path
          name: comment_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              CommentUpdateSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: comment updated
                  comment: CommentSchema
        404:
          description: Comment does not exists
        400:
          description: only owner can update Comment
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: comment_id
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
                    example: Comment deleted
        404:
          description: Comment does not exists

    """

    method_decorators = [jwt_required]

    def get(self, comment_id):
        schema = CommentSchema()
        comment = Comment.query.get_or_404(comment_id)
        return {"comment": schema.dump(comment)}

    def put(self, comment_id):
        owner = get_jwt_identity()
        schema = CommentUpdateSchema(partial=True)
        comment = Comment.query.get_or_404(comment_id)
        if comment.user_id != owner:
            return {"msg": "only owner can update Comment"}, 400
        comment = schema.load(request.json, instance=comment)
        db.session.commit()
        return {"msg": "comment updated", "comment": schema.dump(comment)}

    def delete(self, comment_id):
        comment = Comment.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()

        return {"msg": "comment deleted"}


class CommentList(Resource):
    """Creation and get_all
    ---
    get:
      tags:
        - api
      parameters:
        - in: query
          name: user_id
          schema:
            type: integer
          description: The user_id to filter objects
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
                    post: PostSchema
    """

    method_decorators = [jwt_required]

    @parser.use_args({"post_id": fields.Int()}, location="query")
    def get(self, args):
        schema = CommentSchema(many=True)
        query = Comment.query
        if args:
            query = Comment.query.filter_by(**args)
        return paginate(query, schema)

    def post(self):
        schema = CommentSchema()
        comment = schema.load(request.json)
        db.session.add(comment)
        db.session.commit()

        return {"msg": "comment created", "comment": schema.dump(comment)}, 201
