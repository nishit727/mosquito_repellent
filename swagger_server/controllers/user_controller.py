import connexion
import six
import base64

from database import Database
from swagger_server.models.user import User  # noqa: E501
from swagger_server import util

db = Database()

def create_user(user):  # noqa: E501
    """Create user

     # noqa: E501

    :param user: Created user object
    :type user: dict | bytes

    :rtype: None
    """
    try:
        username = user["username"]
        password = user["password"]
        if db.add_user(username, password):
            return "Successfully added user"
    except Exception as e:
        return None

def get_token():  # noqa: E501
    """Create a token

    This can only be done by a verified user. # noqa: E501

    :rtype: str
    """
    try:
        auth = connexion.request.headers["Authorization"]
        auth = str(auth).split(" ")[1]
        dc = str(base64.b64decode(auth))
        dc = dc[dc.find("\'") + 1:dc.rfind("\'")]
        username = dc.split(":")[0]
        password = dc.split(":")[1]
        if db.verify_user(username, password):
            token = db.generate_token(username)
            return token
    except Exception as e:
        print(e)
    return None
