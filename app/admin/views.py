from flask import redirect, url_for, send_file
from flask_login import login_required, current_user
from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from ..models import has_permission


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
		_tablename = self.model.__tablename__

		self.can_create = has_permission(_tablename, current_user, 'create')
		self.can_edit = has_permission(_tablename, current_user, 'update')
		self.can_delete = has_permission(_tablename, current_user, 'delete')

		can_read = has_permission(_tablename, current_user, 'read')

		return True if current_user.is_authenticated and can_read else False

	def inacessible_callback(self, name, **kwargs):
		return redirect(url_for('login'))


class UserModelView(BaseCustomModelView):
	column_exclude_list = exclude_list + ('password_hash',)

	can_view_details = True

class RoleModelView(BaseCustomModelView):
	pass

class MachineIdentityModelView(BaseCustomModelView):
	pass

class ItemFileModelView(BaseCustomModelView):
	column_exclude_list = exclude_list + ('data',)


class ItemFilePlatformModelView(BaseCustomModelView):
	pass

class ItemFileTypeModelView(BaseCustomModelView):
	pass

class DownloadsView(BaseView):
	@expose('/')
	def index(self):
		from ..models import ItemFile, ItemFileType
		doc_type = ItemFileType.query.filter_by(name='doc').first()
		prog_type = ItemFileType.query.filter_by(name='prog').first()

		doc_files = ItemFile.query.filter_by(type=doc_type).all()
		prog_files = ItemFile.query.filter_by(type=prog_type).all()

		return self.render('admin/downloads.html', doc_files=doc_files, prog_files=prog_files)

	@expose('/download/<int:file_id>')
	@login_required
	def download(self, file_id):
		# return self.render('admin/second_page.html')
		from ..models import ItemFile
		obj = ItemFile.query.filter_by(id=file_id).first()
		# print('file_id: {} | file: {}'.format(file_id, obj))

		from io import BytesIO
		return send_file(BytesIO(obj.data), attachment_filename=obj.name, as_attachment=True)

