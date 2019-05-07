from models.base_model import BaseModel
from flask_login import LoginManager, UserMixin
import peewee as pw
import re


class Image(BaseModel):

    user = pw.ForeignKeyField(User, backref='images')
