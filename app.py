import os
import config
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from models.base_model import db
# import urllib.parse

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

csrf = CSRFProtect()
app = Flask('NEXTAGRAM', root_path=web_dir)
csrf.init_app(app)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


# @app.template_filter('clean_querystring')
# def clean_querystring(request_args, *keys_to_remove, **new_values):
#     # We'll use this template filter in the pagination include. This filter
#     # will take the current URL and allow us to preserve the arguments in the
#     # querystring while replacing any that we need to overwrite. For instance
#     # if your URL is /?q=search+query&page=2 and we want to preserve the search
#     # term but make a link to page 3, this filter will allow us to do that.
#     querystring = dict((key, value) for key, value in request_args.items())
#     for key in keys_to_remove:
#         querystring.pop(key, None)
#     querystring.update(new_values)
#     return urllib.parse.urlencode(querystring)


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
