from models.base_model import BaseModel
from models.user import User
from flask_login import LoginManager, UserMixin
from playhouse.hybrid import hybrid_property
import peewee as pw
import re
from config import AWS_LINK


class Image(BaseModel):

    user = pw.ForeignKeyField(User, backref='images')
    image = pw.CharField(null=True, default=None)

    @hybrid_property
    def users_image_url(self):
        return f"{AWS_LINK}/{self.image}"
