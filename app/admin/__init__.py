from flask_admin import Admin
from .. import db
from .views import MyAdminIndexView, LogoutMenuLink, UserModelView, RoleModelView, MachineIdentityModelView
from ..models import User, Role, MachineIdentity
from flask_admin.contrib.sqla import ModelView
from flask import url_for


admin = Admin(template_mode='bootstrap3',
			  index_view=MyAdminIndexView(name='Flask Holder',
											url='/'))
def create_module(app, **kwargs):
	admin.init_app(app)

	admin.add_view(UserModelView(User, db.session))
	admin.add_view(RoleModelView(Role, db.session))
	admin.add_view(MachineIdentityModelView(MachineIdentity, db.session))

	admin.add_link(LogoutMenuLink(name='Logout', category='', url="/auth/logout"))
	# admin.add_link(LogoutMenuLink(name='Logout', category='', url=url_for('auth.logout'))
