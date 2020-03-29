from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_admin import Admin
from flask_login import LoginManager


bootstrap = Bootstrap()
db = SQLAlchemy()
admin = Admin(template_mode='bootstrap3')
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
	admin.init_app(app)
	# from .main.views import MyAdminIndexView

	# admin.init_app(app, 
	# 				template_mode='bootstrap3',
				# 	index_view=MyAdminIndexView(name='Flask Holder',
				# 								url='/'))

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	from .admin import admin_bp as admin_blueprint
	app.register_blueprint(admin_blueprint)

	return app
