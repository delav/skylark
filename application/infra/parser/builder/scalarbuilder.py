from application.infra.parser.builder import BaseBuilder


class ScalarBuilder(BaseBuilder):
    """
    suite scalar
    """

    def __init__(self):
        super(ScalarBuilder, self).__init__()

    def _splice_key_value(self, key, value):
        """
        splice key and value to string
        :param key: scalar name
        :param value: scalar value
        :return: string
        """
        return key + self.small_sep + value + self.linefeed

    def get_from_queryset(self, queryset):
        """
        get suite scalar from suite queryset
        :return: string
        """
        scalar_content = ''
        if not queryset.exists():
            return ''
        for obj in queryset.iterator():
            scalar_content += self._splice_key_value(obj.name, obj.value)
        return scalar_content
