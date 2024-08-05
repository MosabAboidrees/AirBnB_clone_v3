#!/usr/bin/python3
"""Flask Blueprint"""

from flask import Blueprint
<<<<<<< HEAD
=======
from api.v1.views.index import *
from api.v1.views.states import *
>>>>>>> refs/remotes/origin/master

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


from api.v1.views.index import *
