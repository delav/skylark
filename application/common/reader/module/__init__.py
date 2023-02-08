from application.libkeyword.models import LibKeyword
from application.libkeyword.serializers import LibKeywordSerializers


class LibKeywordMap(object):

    def __init__(self, market=None):
        self.market = market
        self.keyword_id_map = {}
        self.name_alias_map = {}
        self.alias_name_map = {}
        self._init_keywords()

    def _init_keywords(self):
        keywords = LibKeyword.objects.all()
        [self._get(item) for item in keywords.iterator()]

    def _get(self, keyword):
        ser_item = LibKeywordSerializers(keyword).data
        self.keyword_id_map[keyword.id] = ser_item
        name = ser_item['name']
        alias = ser_item['ext_name']
        self.name_alias_map[name] = alias
        self.alias_name_map[alias] = name

    def get_id_map(self):
        return self.keyword_id_map

    def get_name_map(self):
        return self.name_alias_map

    def get_alias_map(self):
        return self.alias_name_map


# init lib keyword data
lib_keyword = LibKeywordMap()
keyword_map = lib_keyword.get_id_map()
name_map = lib_keyword.get_name_map()
alias_map = lib_keyword.get_alias_map()
