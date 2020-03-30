from flask_admin import Admin
from .. import db
from .views import MyAdminIndexView
from ..models import User, Role, MachineIdentity
from flask_admin.contrib.sqla import ModelView


admin = Admin(template_mode='bootstrap3',
			  index_view=MyAdminIndexView(name='Flask Holder',
											url='/'))
def create_module(app, **kwargs):
	admin.init_app(app)

	models = [User, Role, MachineIdentity]

	for model in models:
		admin.add_view(ModelView(model, db.session))
