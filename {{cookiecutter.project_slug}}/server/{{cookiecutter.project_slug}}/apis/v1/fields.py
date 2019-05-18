from flask_restful import fields

bangumi_fields = {
    'total':
    fields.Integer,
    'page_size':
    fields.Integer,
    'results':
    fields.List(
        fields.Nested({
            'id': fields.Integer,
            'name': fields.String,
            'time': fields.DateTime('iso8601'),
            'url': fields.String
        }))
}