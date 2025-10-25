from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

from flask_jwt_extended import JWTManager

jwt = JWTManager()
