from flask import redirect, url_for
from flask_login import login_required, current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink


exclude_list = ('creation_time', 'modification_time')

class MyAdminIndexView(AdminIndexView):
	def is_accessible(self):
		return current_user.is_authenticated

	def inaccessible_callback(self, name, **kwargs):
		# redirect to login page if user doesn't have access
		return redirect(url_for('auth.login'))


class LogoutMenuLink(MenuLink):

	def is_accessible(self):
		return current_user.is_authenticated 


class BaseCustomModelView(ModelView):

	column_exclude_list = exclude_list

	def is_accessible(self):
		self.can_create = True
		self.can_edit = True
		self.can_delete = True

		return current_user.is_authenticated

	def inacessible_callback(self, name, **kwargs):
		return redirect(url_for('login'))


class UserModelView(BaseCustomModelView):
	# pass
	column_exclude_list = exclude_list + ('password_hash',)

	can_view_details = True

class RoleModelView(BaseCustomModelView):
	pass

class MachineIdentityModelView(BaseCustomModelView):
	pass
