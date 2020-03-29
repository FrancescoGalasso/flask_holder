from flask_admin.contrib.sqla import ModelView
from .. import db, admin
from ..models import User, Role, MachineIdentity


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(MachineIdentity, db.session))
