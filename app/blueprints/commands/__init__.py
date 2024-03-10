from flask import Blueprint
import click

bp = Blueprint('command', __name__, url_prefix='/command')
from app.models import User

@bp.cli.command('mod_user')
@click.argument('name')
def mod_user(name):
    user = User.query.filter_by(username = name).first()
    if user:
        try: 
            user.admin = True
            user.commit()
        except: 
            print("An unforeseen error has occured. User %s's permissions could not be updated." % name)
            return
        print("user: %s has been given admin permissions." % name)
    else:
        print("Error: User %s could not be located within the tables. Please check for mispellings.")

    