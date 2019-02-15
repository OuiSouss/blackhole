"""
Redefine a JSONEncoder
Because Mongo uses BSON which is not serializable for datetime and ObjectID
"""
from datetime import datetime, date
import isodate as iso
from bson import ObjectId
from flask.json import JSONEncoder
from werkzeug.routing import BaseConverter


class MongoJSONEncoder(JSONEncoder):
    """
    Extends JsonEncoder
    :return: new JsonEncoder with datetime and ObjectID encoded
    """
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return iso.datetime_isoformat(o)
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


class ObjectIdConverter(BaseConverter):
    """
    Convert ObjectID
    """
    def to_python(self, value):
        return ObjectId(value)

    def to_url(self, value):
        return str(value)
