import pymysql
from .response import JsonResponse
from .permissions import IsSuperUser
from .exception import ValidationException

pymysql.install_as_MySQLdb()
