from application.storage import LIB_KEYWORD_MAP
from application.storage import USER_KEYWORD_MAP


STATUSES = ['FAIL', 'PASS', 'SKIP', 'NOT RUN']


class _Keyword(object):
    def __init__(self, keyword_id, inputs, outputs):
        """
        keyword: entity dict
        """
        self._keyword_id = keyword_id
        self._inputs = inputs
        self._outputs = outputs
        self._keyword_name = ''
        self.__callback__()

    def __callback__(self):
        func_name = self._get_func_name()
        if not hasattr(self, func_name):
            return
        getattr(self, func_name)()

    def keyword_map(self):
        return {}

    def _get_func_name(self):
        name = self.keyword_map().get(self._keyword_id, {}).get('name')
        if not name:
            return self._default_keyword()
        self._keyword_name = name
        return f'_{name.lower().strip()}'

    def _default_keyword(self):
        """
        if found not keyword, use default keyword: LOG
        """
        self._keyword_name = 'LOG'
        self._outputs = ''
        self._inputs = f'This keyword invalid: {self._keyword_id}!'
        return None

    @property
    def keyword_name(self):
        return self._keyword_name

    @property
    def entity_input(self):
        return self._inputs

    @property
    def entity_output(self):
        return self._outputs


class LibKeywordManager(_Keyword):
    """
    handle special keyword, such as FOR, END IF..., function name is the keyword name.
    """
    def keyword_map(self):
        return LIB_KEYWORD_MAP

    def _end(self):
        """
        special keyword 'end' must be upper
        """
        self._keyword_name = 'END'

    def _for(self):
        """
        special keyword 'for' must be upper
        """
        self._keyword_name = 'FOR'

    def _if(self):
        """
        special keyword 'if' must be upper
        """
        self._keyword_name = 'IF'

    def _else_if(self):
        """
        special keyword 'else if' must be upper
        """
        self._keyword_name = 'ELSE IF'

    def _else(self):
        """
        special keyword 'else' must be upper
        """
        self._keyword_name = 'ELSE'

    def _try(self):
        """
        special keyword 'try' must be upper
        """
        self._keyword_name = 'TRY'

    def _except(self):
        """
        special keyword 'except' must be upper
        """
        self._keyword_name = 'EXCEPT'

    def _finally(self):
        """
        special keyword 'finally' must be upper
        """
        self._keyword_name = 'FINALLY'

    def _while(self):
        """
        special keyword 'while' must be upper
        """
        self._keyword_name = 'WHILE'

    def _continue(self):
        """
        special keyword 'continue' must be upper
        """
        self._keyword_name = 'CONTINUE'

    def _break(self):
        """
        special keyword 'break' must be upper
        """
        self._keyword_name = 'BREAK'

    def _return(self):
        """
        special keyword 'return' must be upper
        """
        self._keyword_name = 'RETURN'


class UserKeywordManager(_Keyword):
    """
    handle user keyword
    """

    def keyword_map(self):
        return USER_KEYWORD_MAP
