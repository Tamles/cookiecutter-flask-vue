from flask import Blueprint
from flask_cors import CORS
from flask_restful import Api
from {{cookiecutter.project_slug}}.apis.v1 import resources

bp = Blueprint('api_v1', __name__)
CORS(bp)
api = Api(bp)

api.add_resource(resources.BangumiApi, '/bangumis/<int:bangumi_id>', endpoint='bangumi')
api.add_resource(resources.BangumiListApi, '/bangumis', endpoint='bangumis')
