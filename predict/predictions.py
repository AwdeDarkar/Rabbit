"""
predictions
====================================================================================================

A RESTful interface with the predictions system.

----------------------------------------------------------------------------------------------------

**Created**
    10.30.18
**Updated**
    10.31.18 by Darkar
**Author**
    Darkar
**Copyright**
    This code is Free and Open Source for any purpose; it is provided as-is without warranty.
"""

from enum import Enum
from datetime import datetime

from ..database.interfaces import PredictionInterface

class RequestType(Enum):
    """ Different general forms an API request can take """

    SELECT_LIST = "select"
    """ Select and return a list of predictions matching certain criteria """

    CREATE_PREDICTIONS = "create"
    """ Insert a list of new predictions """

    RESOLVE_PREDICTIONS = "resolve"
    """ Resolve existing predictions """

def process_api_call(db_conn, request):
    """ Process a request to the api as POST JSON data """
    if request.method != "POST": return None

    data = request.form.to_dict(flat=False)
    rtype = data["type"]
    if rtype == RequestType.SELECT_LIST: return select_list(db_conn, data["criteria"])
    if rtype == RequestType.SELECT_LIST: return select_list(db_conn, data["predictions"])
    if rtype == RequestType.SELECT_LIST: return select_list(db_conn, data["resolutions"])
    return None

def select_list(db_conn, criteria):
    """ Select a list of predictions from ``db_conn`` matching ``criteria`` """
    filters = []

    if "interval" in criteria:
        mn = datetime.utcfromtimestamp(criteria["interval"]["min_timestamp"])
        mx = datetime.utcfromtimestamp(criteria["interval"]["max_timestamp"])
        filters.append(lambda p: p.created > mn and p.created < mx)

    if "resolved" in criteria:
        filters.append(lambda p: (p.resolved))

    if "unresolved" in criteria:
        filters.append(lambda p: not p.resolved)

    def f(prob):
        """ Check all of the filters """
        for filt in filters:
            if not filt(prob): return False
        return True

    return PredictionInterface.create_all(db_conn, test=f)

def create_predictions(db_conn, new_predictions):
    pass

def resolve_predictions(db, res_predictions):
    pass
