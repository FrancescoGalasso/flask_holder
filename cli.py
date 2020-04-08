import click

from app import db
from app.models import User, Role, MachineIdentity, ItemFile, ItemFilePlatform, ItemFileType
from werkzeug.security import generate_password_hash


def register_cli(app):

	@app.cli.command()
	def test():
		"""Run the unit tests."""
		import unittest
		tests = unittest.TestLoader().discover('tests')
		unittest.TextTestRunner(verbosity=2).run(tests)

	@app.cli.command()
	def generate_db():
		"""Generate db and create default <Admin> User"""
		
		# for safety drop all tables
		db.drop_all()
		# create tables
		db.create_all()
		# create Admin Role
		_table_names = db.engine.table_names()
		table_names = ','.join(_table_names)
		admin_role = Role(name='admin',
						  create=table_names,
						  read=table_names,
						  update=table_names,
						  delete=table_names)
		# create admin user
		admin_user = User(name='admin', password_hash=generate_password_hash('admin'),
					email='admin@example.com', role=admin_role)

		try:
			db.session.add(admin_role)
			db.session.add(admin_user)
			db.session.commit()
			click.echo('User "{0}" with Role "{1}" Added.'.format(admin_user.name, admin_user.role))
		except Exception as e:
			# log.error("Fail to add new user: %s Error: %s" % (username, e))
			click.echo('ERROR: {}'.format(e))
			db.session.rollback()

	@app.cli.command()
	def generate_sample_roles():
		"""Generate sample roles (tech_administrator & user)"""

		tech_administrator_role = Role(name='tech_administrator')
		user_role = Role(name='user')

		roles_list = [tech_administrator_role, user_role]

		try:
			for _role in roles_list:
				db.session.add(_role)
				click.echo('Role "{0}" Added.'.format(_role.name))

			db.session.commit()
		except Exception as e:
			# log.error("Fail to add new user: %s Error: %s" % (username, e))
			click.echo('ERROR: {}'.format(e))
			db.session.rollback()

	@app.cli.command('create-user')
	@click.argument('username')
	@click.argument('password')
	@click.argument('role_name')
	def create_user(username, password, role_name):
	    _user= User()
	    _role = Role.query.filter_by(name=role_name).first()
	    _user.name = username
	    _user.set_password(password)
	    _user.role = _role

	    try:
	        db.session.add(_user)
	        db.session.commit()
	        click.echo('User {0} Added.'.format(username))
	    except Exception as e:
	        # log.error("Fail to add new user: %s Error: %s" % (username, e))
	        click.echo("Fail to add new user: %s Error: %s" % (username, e))
	        db.session.rollback()

	@app.cli.command()
	def generate_sample_files():
		"""Generate sample ItemFile, ItemFilePlatform and ItemFileType by deleting existing ones"""

		try:
			db.session.query(ItemFile).delete()
			db.session.query(ItemFilePlatform).delete()
			db.session.query(ItemFileType).delete()
			db.session.commit()
			click.echo('Deleted all ItemFile')
		except Exception as e:
			# log.error("Fail to add new user: %s Error: %s" % (username, e))
			click.echo('ERROR: {}'.format(e))
			db.session.rollback()

		platform_win32 = ItemFilePlatform(name='win32', description='Windows 32 bit')
		platform_win64 = ItemFilePlatform(name='win64', description='Windows 64 bit')

		type_manual = ItemFileType(name='doc', description='Manual')
		type_program = ItemFileType(name='prog', description='Program')

		file_data_1 = "This is a test file 1 !!!".encode()	#bytes
		file_data_2 = "This is a test file 2 !!!".encode()	#bytes
		file_data_3 = "This is a test file tries to be a program !!!".encode()	#bytes

		item_file_1 = ItemFile(name='test_file_1.txt',
								data=file_data_1,
								description='This is a test file to download',
								type=type_manual)

		item_file_2 = ItemFile(name='test_file_2.txt',
								data=file_data_2,
								description='This is an another test file to download',
								type=type_manual)

		item_file_3 = ItemFile(name='test_file_3.txt',
								data=file_data_3,
								description='This is a fake program file to download',
								platform=platform_win64,
								type=type_program)

		item_file_4 = ItemFile(name='test_file_4.txt',
								data=file_data_3,
								description='This is a fake program file to download',
								platform=platform_win32,
								type=type_program)

		item_files = [item_file_2, item_file_1, item_file_3]

		try:
			for item in item_files:
				db.session.add(item)
				click.echo('Item "{0}" Added.'.format(item.name))

			db.session.commit()
		except Exception as e:
			# log.error("Fail to add new user: %s Error: %s" % (username, e))
			click.echo('ERROR: {}'.format(e))
			db.session.rollback()

