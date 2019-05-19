from flask_restful import fields

bangumi_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'time': fields.DateTime('iso8601'),
    'url': fields.String
}

bangumis_fields = {
    'total': fields.Integer,
    'page_size': fields.Integer,
    'results': fields.List(fields.Nested(bangumi_fields))
}