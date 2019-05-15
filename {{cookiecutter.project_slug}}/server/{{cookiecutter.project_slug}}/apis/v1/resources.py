import arrow
from flask_restful import Resource, marshal_with, reqparse
from {{cookiecutter.project_slug}}.extensions import db
from {{cookiecutter.project_slug}}.models import Bangumi
from {{cookiecutter.project_slug}}.apis.v1.fields import bangumi_fields
from {{cookiecutter.project_slug}}.apis.v1.utils import non_empty_str, non_empty_datetime


class BangumiApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=non_empty_str)
        self.parser.add_argument('time', type=non_empty_datetime)
        self.parser.add_argument('company', type=non_empty_str)
        super().__init__()

    @marshal_with(bangumi_fields)
    def get(self, bangumi_id):
        return Bangumi.query.get_or_404(bangumi_id)

    @marshal_with(bangumi_fields)
    def put(self, bangumi_id):
        bangumi = Bangumi.query.get_or_404(bangumi_id)
        args = self.parser.parse_args()
        for k, v in args.items():
            setattr(bangumi, k, v)
        db.session.commit()
        return bangumi, 201

    def delete(self, bangumi_id):
        bangumi = Bangumi.query.get_or_404(bangumi_id)
        db.session.delete(bangumi)
        db.session.commit()
        return '', 204


class BangumiListApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=non_empty_str, required=True)
        self.parser.add_argument('time', type=non_empty_str)
        self.parser.add_argument('company', type=non_empty_str)
        super().__init__()

    @marshal_with(bangumi_fields)
    def get(self):
        return Bangumi.query.all()

    @marshal_with(bangumi_fields)
    def post(self):
        args = self.parser.parse_args()
        bangumi = Bangumi(name=args['name'], time=arrow.get(args['time']).naive, company=args['company'])
        db.session.add(bangumi)
        db.session.commit()
        return bangumi, 201
