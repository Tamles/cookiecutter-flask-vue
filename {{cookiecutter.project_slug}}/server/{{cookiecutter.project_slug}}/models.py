from datetime import datetime
from {{cookiecutter.project_slug}}.extensions import db


class Bangumi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), index=True, unique=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now)
    company = db.Column(db.String(160))

    def __repr__(self):
        return f'<{type(self).__name__} {self.name}>'
