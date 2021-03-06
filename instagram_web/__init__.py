from app import app
from flask import Flask, render_template
from flask_login import current_user
from playhouse.flask_utils import object_list, get_object_or_404
from flask_login import LoginManager
from models.user import User
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from instagram_web.util.google_oauth import oauth
from instagram_web.blueprints.follows.views import follows_blueprint

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(follows_blueprint, url_prefix="/follows")

#FLASK LOGIN FUNCTION#
login_manager = LoginManager()
login_manager.init_app(app)

# GOOGLE OAUTH
oauth.init_app(app)


#user_loader used to reload the user object from the user ID stored in the session#


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

# error handlers


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/")
def home():
    # users = User.select(User.id == current_user.id)
    return render_template('home.html')

    # return object_list
    # ('home.html',
    #  users)
