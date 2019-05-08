from models.base_model import BaseModel
from models.user import User
from flask_login import LoginManager, UserMixin
import peewee as pw
import re


class Image(BaseModel):

    user = pw.ForeignKeyField(User, backref='images')
    image = pw.CharField(null=True, default=None)
