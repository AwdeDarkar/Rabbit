"""
api functions
====================================================================================================

A RESTful interface with the predictions system.

----------------------------------------------------------------------------------------------------

**Created**
    10.30.18
**Updated**
    12.18.18 by Darkar
**Author**
    Darkar
**Copyright**
    This code is Free and Open Source for any purpose; it is provided as-is without warranty.
"""
from __future__ import absolute_import

from enum import Enum
from datetime import datetime

from ..database.interfaces import PredictionInterface #pylint: disable=import-error

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

def select_list(db_conn, criteria={}): #pylint: disable=dangerous-default-value
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

    if "id_in" in criteria:
        ids = criteria["id_in"]
        filters.append(lambda p: p in ids)

    def f(prob):
        """ Check all of the filters """
        for filt in filters:
            if not filt(prob): return False
        return True

    return PredictionInterface.create_all(db_conn, test=f)

def create_predictions(db_conn, new_predictions):
    """ Create a list of predictions in ``db_conn`` defined by ``new_predictions`` """
    cursor = db_conn.cursor()
    for n_pred in new_predictions:
        pred = PredictionInterface(cursor=cursor)
        pred.name = n_pred["name"]
        pred.description = n_pred["description"]
        pred.created = datetime.now()
        for event in n_pred["events"]:
            pred.probabilities[event] = n_pred["events"][event]

        if not pred.save(): return False

    return True


def resolve_predictions(db_conn, res_predictions):
    """ Resolve the predictions with the given ids """
    ids = res_predictions.keys()
    preds = select_list(db_conn, criteria={"id_in" : ids})
    for pred in preds:
        pred.resolve(res_predictions[pred.get_id()])
        pred.save()
