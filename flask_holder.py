import os
import click
from cli import register_cli
from app import create_app, db
from app.models import (User, 
					  	Role, 
					  	MachineIdentity,
					  	ItemFile,
					  	ItemFilePlatform,
					  	ItemFileType)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
register_cli(app)

@app.shell_context_processor
def make_shell_context():
	return dict(db=db,
				User=User,
				Role=Role,
				MachineIdentity=MachineIdentity,
				ItemFile=ItemFile,
				ItemFilePlatform=ItemFilePlatform,
				ItemFileType=ItemFileType)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)
