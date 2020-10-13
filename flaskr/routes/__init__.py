from flask import Blueprint
routes = Blueprint('routes', __name__)

from .index import *
from .cars import *
from .error500 import *
from .error404 import *