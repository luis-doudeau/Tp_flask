from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap5(app)
import os
def mkpath(p):
    """
    renvoie repertoire courant
    """
    return os.path.normpath(
            os.path.join(
                os.path.dirname(__file__),p)
            )

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///' + mkpath('../books.db'))
app. config ['SECRET_KEY'] = "069b85f6-3d1a-4c89-8d17-83e9b577da10"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)
login_manager = LoginManager (app)
login_manager.login_view = 'login'

