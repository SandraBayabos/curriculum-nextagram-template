from models.base_model import BaseModel
from models.user import User
from models.image import Image


class Donation(BaseModel):
    user = pw.ForeignKeyField(User, backref='posts')
    image = pw.ForeignKeyField(Image, backref='images')
    amount = pw.DecimalField(null=True)
