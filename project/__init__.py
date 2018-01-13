# IMPORTS
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_login import current_user, login_required
from flask_mail import Mail
import os


# CONFIG
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

from project.models import User, Items


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


# BLUEPRINTS
from project.users.views import users_blueprint
from project.items.views import items_blueprint
from project.seminars.views import seminars_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(items_blueprint)
app.register_blueprint(seminars_blueprint)


# ROUTES
@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

	
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    """Render homepage"""

    all_user_items = Items.query.filter_by(user_id=current_user.id)
    return render_template('home.html', items=all_user_items)


# ERROR PAGES
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


@app.errorhandler(410)
def page_not_found(e):
    return render_template('410.html'), 410
