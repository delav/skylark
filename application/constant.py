
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
    DISABLED = 3
    READY = 9


# build status
class BuildStatus:
    PENDING = -1
    RUNNING = 0
    FINISH = 1
    SUCCESS = 2
    FAILED = 3


class KeywordCategory:
    ORDINARY = 0
    RESERVED = 1
    DEPENDENCE = 2
    CUSTOMIZED = 3
    PLATFORM = 9


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


class NoticeMode:
    WECOM = 1
    DING_TALK = 2
    lARK = 3
