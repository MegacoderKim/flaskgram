from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from socio.api.schemas import FollowerSchema
from socio.models import Follower
from socio.extensions import db
from socio.commons.pagination import paginate


class FollowerResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: follower_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  follower: FollowerSchema
        404:
          description: follower does not exists
    put:
      tags:
        - api
      parameters:
        - in: path
          name: follower_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              FollowerSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: follower updated
                  follower: FollowerSchema
        404:
          description: follower does not exists
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: follower_id
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
                    example: follower deleted
        404:
          description: follower does not exists
    """

    method_decorators = [jwt_required]

    def get(self, follower_id):
        schema = FollowerSchema()
        user = Follower.query.get_or_404(follower_id)
        return {"follower": schema.dump(user)}

    def put(self, follower_id):
        schema = FollowerSchema(partial=True)
        follower = Follower.query.get_or_404(follower_id)
        follower = schema.load(request.json, instance=follower)

        db.session.commit()

        return {"msg": "follower updated", "follower": schema.dump(follower)}

    def delete(self, follower_id):
        follower = Follower.query.get_or_404(follower_id)
        db.session.delete(follower)
        db.session.commit()

        return {"msg": "follower deleted"}
