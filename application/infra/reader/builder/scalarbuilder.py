from application.infra.reader.builder.basebuilder import BaseBuilder
from application.variable.models import Variable


class ScalarBuilder(BaseBuilder):
    """
    suite scalar
    """
    def __init__(self, module_id, module_type):
        self.module_id = module_id
        self.module_type = module_type

    def _splice_key_value(self, key, value):
        """
        splice key and value to string
        :param key: scalar name
        :param value: scalar value
        :return: string
        """
        return key + self.small_sep + value + self.linefeed

    def variable_info(self):
        """
        get suite scalar by moduleId and moduleType
        :return: string
        """
        scalar_content = ''
        queryset = Variable.objects.filter(
            module_id=self.module_id,
            module_type=self.module_type
        )
        if not queryset.exists():
            return ''
        for obj in queryset.iterator():
            scalar_content += self._splice_key_value(obj.name, obj.value)
        return scalar_content
