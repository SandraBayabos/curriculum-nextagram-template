import os
import config
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from models.base_model import db

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

csrf = CSRFProtect()
app = Flask('NEXTAGRAM', root_path=web_dir)
csrf.init_app(app)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


# def object_list(template_name, qr, var_name='object_list', **kwargs):
#     kwargs.update(
#         page=int(request.args.get('page', 1)),
#         pages=qr.count() / 20 + 1)
#     kwargs[var_name] = qr.paginate(kwargs['page'])
#     return render_template(template_name, **kwargs)


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
