from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger

db = SQLAlchemy()
migrate = Migrate()
swagger = Swagger()
