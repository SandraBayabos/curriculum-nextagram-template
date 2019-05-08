from models.userimage import Image
from instagram_web.blueprints.images.helpers import upload_file_to_s3, allowed_file
from flask import Blueprint, Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager
from werkzeug import secure_filename

userimages_blueprint = Blueprint(
    'userimages', __name__, template_folder='templates')


@userimages_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('userimages/new.html')
