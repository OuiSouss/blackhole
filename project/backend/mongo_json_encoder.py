"""
mongo_json_encoder.py
===================
Redefine a JSONEncoder
Because Mongo uses BSON which is not serializable for datetime and ObjectID
"""
from datetime import datetime, date
import isodate as iso
from bson import ObjectId
from flask import json
from werkzeug.routing import BaseConverter


class MongoJSONEncoder(json.JSONEncoder):
    """
    MongoJSONEncoder Extends json.JSONEncoder

    :param json: JSON
    :type json: Object
    :return: JSON
    :rtype: Object
    """
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return iso.datetime_isoformat(o)
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class ObjectIdConverter(BaseConverter):
    """
    ObjectIdConverter Converter

    Convert ObjectID to string and str to ObjectID

    :param BaseConverter: werzeug BaseConverter
    :type BaseConverter: map
    """
    def to_python(self, value):
        return ObjectId(value)

    def to_url(self, value):
        return str(value)
