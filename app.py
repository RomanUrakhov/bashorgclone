from flask import Flask
from config import Configuration

from flask_sqlalchemy import SQLAlchemy

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

#####
from models import *

admin = Admin(app)
admin.add_view(ModelView(Post, db.session))
