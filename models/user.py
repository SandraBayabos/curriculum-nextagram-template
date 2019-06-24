from models.base_model import BaseModel
from flask import url_for
from flask_login import LoginManager, UserMixin
import peewee as pw
import re
from playhouse.hybrid import hybrid_property
from config import AWS_LINK


class User(BaseModel, UserMixin):

    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(null=False)
    user_profile_image = pw.CharField(null=True, default=None)
    private = pw.BooleanField(default=False)

    def validate(self):
        duplicate_user = User.get_or_none(
            User.username == self.username)

        if duplicate_user:
            self.errors.append('Name taken')

        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_email:
            self.errors.append('An account with that email already exists')

    @classmethod
    def validate_password(self, password):
        valid_password = True
        while valid_password:
            if (len(password) < 6 or len(password) > 12):
                break
            elif not re.search("[a-z]", password):
                break
            elif not re.search("[0-9]", password):
                break
            elif not re.search("[A-Z]", password):
                break
            elif not re.search("[$#@]", password):
                break
            elif re.search("\s", password):
                break
            else:
                valid_password = False
                break

        return not valid_password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @hybrid_property
    def profile_image_url(self):
        # to return image url
        if self.user_profile_image:
            return f"{AWS_LINK}/{self.user_profile_image}"
        else:
            return url_for('static', filename="images/profile.jpg")

    # to set a user to private or public
    @hybrid_property
    def is_private(self):
        return True if self.private else False
