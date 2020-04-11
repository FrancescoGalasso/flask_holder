from flask import redirect, url_for, send_file
from flask_login import login_required, current_user
from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from ..models import has_permission
from flask_admin.form.upload import FileUploadField
# from wtforms import FileUploadField
# from app import config
# print('config: {}'.format(config.get('UPLOADED_FILE_FOLDER')))

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

	def __init__(self, app, model, session, name=None, category=None, endpoint=None, url=None, static_folder=None,
				 menu_class_name=None, menu_icon_type=None, menu_icon_value=None):

		# Override form field to use Flask-Admin FileUploadField
		path_uploaded_files = app.config.get('UPLOADED_FILE_FOLDER')
		self.form_args = {
			'item_path': {
				'label': 'File Upload',
				'base_path':  path_uploaded_files,
				'allow_overwrite': True,
			}
		}

		super().__init__(model, session, name, category, endpoint, url, static_folder, menu_class_name,
						 menu_icon_type, menu_icon_value)

	column_exclude_list = exclude_list + ('realname',)

	form_overrides = dict(item_path= FileUploadField)
	form_excluded_columns = ('realname',)

	def on_model_change(self, form, model, is_created):

		obj_file_storage = form.data.get('item_path')
		obj_filename = obj_file_storage.filename
		file_base_path = self.form_args.get('item_path').get('base_path')
		import os
		model.item_path = os.path.join(file_base_path, obj_filename)
		model.realname = obj_filename


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
		from ..models import ItemFile
		obj = ItemFile.query.filter_by(id=file_id).first()

		path_file_to_download = obj.item_path
		return send_file(path_file_to_download, attachment_filename=obj.realname, as_attachment=True)

