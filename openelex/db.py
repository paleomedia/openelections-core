from openelex.config import settings
from mongoengine import connect

def init_db(name='openelex'):
    return None
    #connect(name, **settings.MONGO[name])[name]
