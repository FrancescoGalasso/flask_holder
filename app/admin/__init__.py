from flask_admin import Admin
from .. import db
from ..models import (User, 
					  Role, 
					  MachineIdentity,
					  ItemFile,
					  ItemFilePlatform,
					  ItemFileType)
from .views import (MyAdminIndexView,
					LogoutMenuLink,
					UserModelView,
					RoleModelView,
					MachineIdentityModelView,
					ItemFileModelView,
					ItemFilePlatformModelView,
					ItemFileTypeModelView,
					DownloadsView)
from flask_admin.contrib.sqla import ModelView
from flask import url_for


admin = Admin(template_mode='bootstrap3',
			  index_view=MyAdminIndexView(name='Flask Holder',
											url='/'))
def create_module(app, **kwargs):
	admin.init_app(app)

	# custom_model_views = [UserModelView(User, db.session),
	# 					  RoleModelView(Role, db.session),
	# 					  MachineIdentityModelView(MachineIdentity, db.session),
	# 					  ItemFileModelView(MachineIdentity, db.session),
	# 					  ItemFilePlatformModelView(MachineIdentity, db.session),
	# 					  ItemFileTypeModelView(MachineIdentity, db.session)]

	admin.add_view(UserModelView(User, db.session))
	admin.add_view(RoleModelView(Role, db.session))
	admin.add_view(MachineIdentityModelView(MachineIdentity, db.session))
	admin.add_view(ItemFileModelView(ItemFile, db.session))
	admin.add_view(ItemFilePlatformModelView(ItemFilePlatform, db.session)),
	admin.add_view(ItemFileTypeModelView(ItemFileType, db.session))
	admin.add_view(DownloadsView(name='Downloads', endpoint='downloads'))

	# for model_view in custom_model_views:
	# 	admin.add_view(model_view)

	admin.add_link(LogoutMenuLink(name='Logout', category='', url="/auth/logout"))
