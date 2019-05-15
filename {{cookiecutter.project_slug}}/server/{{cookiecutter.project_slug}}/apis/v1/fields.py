from flask_restful import fields

bangumi_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'time': fields.DateTime('iso8601'),
    'company': fields.String
}