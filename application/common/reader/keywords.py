from application.libkeyword.models import LibKeyword
from application.libkeyword.serializers import LibKeywordSerializers

manage_names = {
    "end": "END",
    "for_list": "FOR",
    "for_dict": "FOR",
}


class LibKeywordMap(object):

    def __init__(self):
        self.keyword_map = {}
        self.key_to_alias = {}
        self.alias_to_key = {}

    def change_to_dict(self):
        keywords = LibKeyword.objects.all()
        # names_list = manage_names.keys()
        for item in keywords.iterator():
            self.keyword_map[item.id] = LibKeywordSerializers(item).data
            # name = item["name"]
            # if name in names_list:
            #     key = manage_names[name]
            # else:
            #     key = self.format_keyword(name)
            # value = item["alias"]
            # self.key_to_alias[key] = value
            # self.alias_to_key[value] = key
        return self.keyword_map

    @staticmethod
    def format_keyword(strings):
        str_list = strings.split('_')
        new_str_list = [s.capitalize() for s in str_list]
        result = ' '.join(new_str_list)
        return result

    def get_key_alias(self):
        return self.key_to_alias

    def get_alias_key(self):
        return self.alias_to_key
