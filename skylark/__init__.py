import pymysql
from .celeryapp import app as celery_app

pymysql.version_info = (1, 4, 0, 'final', 0)
pymysql.install_as_MySQLdb()
__all__ = ('celery_app', )
