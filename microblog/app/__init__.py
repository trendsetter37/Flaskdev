from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import openid
from config import basedir

lm = LoginManager
lm.init_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))

app = Flask(__name__)
app.config.from_object('config') # file named config next to app package
db = SQLAlchemy(app)

from app import views, models