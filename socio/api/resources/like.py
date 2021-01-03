from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from webargs import fields
from webargs.flaskparser import parser
from socio.api.schemas import LikeSchema
from socio.models import Like
from socio.extensions import db
from socio.commons.pagination import paginate


class LikeResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: like_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  comment: LikeSchema
        404:
          description: like does not exists
    put:
      tags:
        - api
      parameters:
        - in: path
          name: like_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              LikeUpdateSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: like updated
                  comment: LikeSchema
        404:
          description: like does not exists
        400:
          description: only owner can update like
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: like_id
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
                    example: like deleted
        404:
          description: like does not exists

    """

    method_decorators = [jwt_required]

    def get(self, like_id):
        schema = LikeSchema()
        like = Like.query.get_or_404(like_id)
        return {"like": schema.dump(like)}

    def delete(self, like_id):
        like = Like.query.get_or_404(like_id)
        db.session.delete(like)
        db.session.commit()

        return {"msg": "comment deleted"}


class LikeList(Resource):
    """Creation and get_all
    ---
    get:
      tags:
        - api
      parameters:
        - in: query
          name: post_id
          schema:
            type: integer
          description: The post_id to filter objects
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
                          $ref: '#/components/schemas/LikeSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              LikeSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: like created
                    post: LikeSchema
    """

    method_decorators = [jwt_required]

    @parser.use_args({"post_id": fields.Int()}, location="query")
    def get(self, args):
        schema = LikeSchema(many=True)
        query = Like.query
        if args:
            query = Like.query.filter_by(**args)
        return paginate(query, schema)

    def post(self):
        schema = LikeSchema()
        like = schema.load(request.json)
        db.session.add(like)
        db.session.commit()

        return {"msg": "like created", "like": schema.dump(like)}, 201
