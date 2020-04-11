from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.inspection import inspect  # pylint: disable=import-error


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

    if hasattr(current_user.role, action):
        _tablenames = getattr(current_user.role, action)
        has_action = False
        if _tablenames and table_name in _tablenames:
            has_action = True
        
        # print('table_name: {} | action: {} | has permission: {}'.format(table_name, action, has_action))
        return True if has_action else False


class ItemFile(NameModel):
    __tablename__ = 'item_files'
    # data = db.Column(db.LargeBinary) # blob type into sqlite
    realname = db.Column(db.String(80), nullable=False)
    item_path = db.Column(db.String(240), nullable=False)
    description = db.Column(db.String(240))
    platform_id = db.Column(db.Integer, db.ForeignKey('item_files_platforms.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('item_files_types.id'))

    @property
    def str_time(self):
        return self.creation_time.strftime('%B %d %Y')

class ItemFilePlatform(NameModel):
    __tablename__ = 'item_files_platforms'
    description = db.Column(db.String(240))
    item_file = db.relationship('ItemFile', backref='platform')


class ItemFileType(NameModel):
    __tablename__ = 'item_files_types'
    description = db.Column(db.String(240))
    item_type = db.relationship('ItemFile', backref='type')

