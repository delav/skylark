
# module data category
class ModuleCategory:
    TESTCASE = 0
    KEYWORD = 1
    VARIABLE = 2
    FILE = 3


# module data type
class ModuleType:
    PROJECT = 0
    DIR = 1
    SUITE = 2
    CASE = 3


# variable value type
class ValueType:
    NONE = 0
    STRING = 1
    NUMBER = 2
    LIST = 3
    DICT = 4


# model data status
class ModuleStatus:
    NORMAL = 0
    DISCARDED = 1
    DELETED = 2
    DISABLED = 4


class KeywordType:
    LIB = 1
    USER = 2


class KeywordGroupType:
    LIB = 0
    USER = 1
    PRO = 2


class ParamMode:
    NONE = 0
    SINGLE = 1
    MULTI = 2
    LIST = 3
    DICT = 4


class FileSaveMode:
    DB = 1
    FILE = 2


class NoticeSwitch:
    WECOM = 1
    DING_TALK = 2
    lARK = 3
