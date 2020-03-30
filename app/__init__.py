from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_admin import Admin
from flask_login import LoginManager


bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)


	with app.app_context():

		from .auth import auth as auth_blueprint
		app.register_blueprint(auth_blueprint, url_prefix='/auth')

		from .admin import create_module as admin_create_module
		admin_create_module(app)


		return app
