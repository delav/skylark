# user customize keyword group
CUSTOMIZE_KEYWORD_GROUP = 99


# module data category
class ModuleCategory:
    TESTCASE = 0
    KEYWORD = 1
    RESOURCE = 2
    FILE = 3


# module data type
class ModuleType:
    PROJECT = 0
    DIR = 1
    SUITE = 2
    CASE = 3


# variable value type
class ValueType:
    STRING = 0
    NUMBER = 1
    LIST = 2
    DICT = 3


# model data status
class ModuleStatus:
    NORMAL = 0
    DISCARDED = 1
    DELETED = 2


class KeywordType:
    LIB = 1
    USER = 2


class ParamMode:
    NAN = 0
    SINGLE = 1
    MULTI = 2
    LIST = 3
    DICT = 4


class FileSaveMode:
    DB = 1
    FILE = 2
