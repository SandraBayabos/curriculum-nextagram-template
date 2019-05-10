from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property

# idols and fans are both Users. Self-referencing table


class FollowerFollowing(BaseModel):
    idol = pw.ForeignKeyField(User, backref='fans')
    fan = pw.ForeignKeyField(User, backref='idols')
