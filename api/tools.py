try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        raise ImportError
import datetime
from bson.objectid import ObjectId
from bson.timestamp import Timestamp
from werkzeug import Response
 
class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, Timestamp):
            return obj.time;
        return json.JSONEncoder.default(self, obj)
 
def jsonify(*args, **kwargs):
    """ jsonify with support for MongoDB ObjectId
    """
    return Response(json.dumps(dict(*args, **kwargs), cls=MongoJsonEncoder), mimetype='application/json')