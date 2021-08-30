import base64
import time

import connexion
import six

from database import Database
from swagger_server.models.daterange import Daterange  # noqa: E501
from swagger_server.models.mosquito import Mosquito  # noqa: E501
from swagger_server import util

db = Database()

def add_mosqutio(mosquito):  # noqa: E501
    """Add a detected mosquito

    This can only be done by a verified user. # noqa: E501

    :param mosquito: Created user object
    :type mosquito: dict | bytes

    :rtype: None
    """
    auth = connexion.request.headers["Authorization"]
    if db.verify_token(auth):
        device_id = mosquito["device_id"]
        specie = mosquito["specie"]
        if db.add_mosquito(time.time(), device_id, specie):
            return "successfully added mosquito"
    return 'do some magic!'


def get_mosqutio(daterange=None):  # noqa: E501
    """Get detected mosqutio data in given time frame

     # noqa: E501

    :param daterange: 
    :type daterange: dict | bytes

    :rtype: None
    """
    auth = connexion.request.headers["Authorization"]
    if db.verify_token(auth):
        start_date = None
        end_date = None
        if daterange is not None:
            if "start_date" in daterange.keys():
                start_date = daterange["start_date"]
            if "end_date" in daterange.keys():
                end_date = daterange["end_date"]
        rows = db.get_mosquito_by_date_range(start_date, end_date)
        data = []
        for row in rows:
            date = row[0]
            device_id = row[1]
            specie = row[2]
            data.append({"timestamp":int(date), "device_id":device_id, "specie":specie})

        return data
