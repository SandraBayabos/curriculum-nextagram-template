from instagram_web.blueprints.images.helpers import upload_file_to_s3, allowed_file
import os
from app import app
from flask import Blueprint, Flask, render_template, request, redirect, flash, url_for
from flask_login import current_user, login_required
from models.user import User, hybrid_property
from models.image import Image
from werkzeug import secure_filename
from config import S3_BUCKET


images_blueprint = Blueprint('images',
                             __name__,
                             template_folder='templates')


@images_blueprint.route('/profile_picture', methods=['GET'])
@login_required
def profile_picture():
    return render_template('images/profile_picture.html')


@images_blueprint.route('/', methods=["POST"])
def upload_file():

    if "user_profile_picture" not in request.files:
        flash('No user_file key in request.files')
        return redirect('/')

    file = request.files["user_profile_picture"]

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, S3_BUCKET)

        #save image to the database#
        update_user_image = User.update(
            user_profile_image=file.filename
        ).where(User.id == current_user.id)

        # return str(file.filename)#

        if update_user_image.execute():

            flash('Successfully changed your profile picture!')
            # return redirect(url_for('home'))
            return render_template('images/profile_picture.html')
        else:
            flash(
                'An error occurred. Try again.')
            return render_template('images/profile_picture.html')
    else:
        return redirect('/')


@images_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('images/new.html')


@images_blueprint.route('/new_user_image', methods=['POST'])
def upload_image():

    # to upload to Amazon

    if "image" not in request.files:
        flash('No user_key in request.files')
        return redirect('/')

    file = request.files["image"]

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, S3_BUCKET)

    # to save to Image database

        upload_image = Image(
            image=file.filename,
            user_id=current_user.id
        )

        if upload_image.save():
            flash('Successfully uploaded a photo!')
            return render_template('images/new.html')
        else:
            flash('An error occurred. Try again')
            return render_template('images/new.html')
    else:
        return redirect('/')
