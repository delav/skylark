import pymysql
from application.infra.response.jsonresponse import JsonResponse
from application.infra.permission.issuper import IsSuperUser
from application.infra.exception.validator import ValidationException

pymysql.install_as_MySQLdb()
