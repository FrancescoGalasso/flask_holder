from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class BaseModel(db.Model):
    # This is an abstract class: SQLAlchemy will not create a table for that model!
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    creation_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modification_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @property
    def get_str_time(self):
        return self.creation_time.strftime('%B %d %Y - %H:%M:%S')

    @property
    def object_to_dict(self):

        data = {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

        for k in data.keys():
            if isinstance(data[k], datetime):
                data[k] = data[k].strftime('%B %d %Y - %H:%M:%S')

        return data


class NameModel(BaseModel):
    __abstract__ = True
    name = db.Column(db.String(120), index=True, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class User(UserMixin, NameModel):
    __tablename__ = 'users'

    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

class Role(NameModel):
    __tablename__ = 'roles'

    users = db.relationship('User', backref='role')
    create = db.Column(db.Text)
    read = db.Column(db.Text)
    update = db.Column(db.Text)
    delete = db.Column(db.Text)


class MachineIdentity(BaseModel):
    __tablename__ = 'machine_identities'
    serial_number = db.Column(db.Integer, index=True, unique=True)
    model = db.Column(db.String(64), index=True)
    platform = db.Column(db.String)
    releases = db.Column(db.String)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


def has_permission(table_name, current_user, action):
    print('table_name: {}'.format(table_name))
    print('current_user name: {}'.format(current_user.name))

    # print('create role tablenames: {}'.format(current_user.role.action))
    if hasattr(current_user.role, action):
        _tablenames = getattr(current_user.role, action)
        print('_tablenames: {}'.format(_tablenames))
        has_action = False
        if _tablenames and table_name in _tablenames:
            has_action = True
        
        return True if has_action else False

