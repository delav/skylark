from application.storage import LIB_ALIAS_MAP


class FixtureManager(object):
    multi_combine_key = 'AND'
    arg_separator = '|'

    def __init__(self, fixture_list):
        self.fixtures = fixture_list
        self._new_fixtures = []

    def replace_fixture_names(self):
        for item in self.fixtures:
            self._new_fixtures.append(self._handler_fixture(item))

    def _handler_fixture(self, fixture_str):
        if fixture_str == '':
            return fixture_str
        new_fixture_str = ''
        keyword_list = []
        if self.multi_combine_key in fixture_str:
            keyword_list = fixture_str.split(self.multi_combine_key)
        for item in keyword_list:
            keyword_str_list = item.split(self.arg_separator)
            keyword_name = keyword_str_list[0].strip()
            if keyword_name in LIB_ALIAS_MAP:
                keyword_str_list[0] = LIB_ALIAS_MAP[keyword_name]
            new_fixture_str += self.arg_separator.join(keyword_str_list)
        return new_fixture_str

    def get_new_fixtures(self):
        return self._new_fixtures
