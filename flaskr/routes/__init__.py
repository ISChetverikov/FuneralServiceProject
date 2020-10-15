from flask import Blueprint
routes = Blueprint('routes', __name__)

from .index import *
from .cars import *
from .workers import *
from .mortuaries import *
from .cemeteries import *
from .clients import *
from .funerals import *
from .reports import *

from .error500 import *
from .error404 import *