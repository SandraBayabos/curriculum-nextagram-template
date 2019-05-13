from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property

# idols and fans are both Users. Self-referencing table


class FollowerFollowing(BaseModel):
    # would automatically create follower_following
    fan = pw.ForeignKeyField(User, backref='idols', unique=True)
    idol = pw.ForeignKeyField(User, backref='fans', unique=True)
    approved = pw.BooleanField(default=False)

    @hybrid_property
    def is_approved(self):
        return True if self.approved else False
