from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config.from_object('config') # file named config next to app package
db = SQLAlchemy(app)

from app import views, models