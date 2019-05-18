import arrow
from flask import current_app
from flask_restful import Resource, marshal_with, reqparse
from {{cookiecutter.project_slug}}.extensions import db
from {{cookiecutter.project_slug}}.models import Bangumi
from {{cookiecutter.project_slug}}.apis.v1.fields import bangumi_fields
from {{cookiecutter.project_slug}}.apis.v1.utils import non_empty_str, non_empty_datetime, non_empty_int


class BangumiApi(Resource):
    def __init__(self):
        self.json_parser = reqparse.RequestParser()
        self.json_parser.add_argument('name',
                                      type=non_empty_str,
                                      location='json')
        self.json_parser.add_argument('time',
                                      type=non_empty_datetime,
                                      location='json')
        self.json_parser.add_argument('url',
                                      type=non_empty_str,
                                      location='json')
        super().__init__()

    @marshal_with(bangumi_fields)
    def get(self, bangumi_id):
        return Bangumi.query.get_or_404(bangumi_id)

    @marshal_with(bangumi_fields)
    def put(self, bangumi_id):
        bangumi = Bangumi.query.get_or_404(bangumi_id)
        args = self.json_parser.parse_args()
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
        self.json_parser = reqparse.RequestParser()
        self.json_parser.add_argument('name',
                                      type=non_empty_str,
                                      required=True,
                                      location='json')
        self.json_parser.add_argument('time',
                                      type=non_empty_str,
                                      location='json')
        self.json_parser.add_argument('url',
                                      type=non_empty_str,
                                      location='json')
        self.args_parser = reqparse.RequestParser()
        self.args_parser.add_argument('page',
                                      type=non_empty_int,
                                      location='args')
        self.args_parser.add_argument('per_page',
                                      type=non_empty_int,
                                      location='args')
        super().__init__()

    @marshal_with(bangumi_fields)
    def get(self):
        args = self.args_parser.parse_args()
        page = args['page']
        per_page = args['per_page'] or current_app.config['BANGUMI_PER_PAGE']
        pagination = Bangumi.query.paginate(page, per_page)
        return {
            'results': pagination.items,
            'total': pagination.total,
            'page_size': per_page
        }

    @marshal_with(bangumi_fields)
    def post(self):
        args = self.json_parser.parse_args()
        bangumi = Bangumi(name=args['name'],
                          time=arrow.get(args['time']).naive,
                          url=args['url'])
        db.session.add(bangumi)
        db.session.commit()
        return bangumi, 201
