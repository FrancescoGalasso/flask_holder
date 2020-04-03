import click

from app import db
from app.models import User, Role
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
		admin_role = Role(name='admin')
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
