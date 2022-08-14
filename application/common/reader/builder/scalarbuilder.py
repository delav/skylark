from application.common.reader.builder.basebuilder import BaseBuilder
from application.variable.models import Variable


class ScalarBuilder(BaseBuilder):
    """
    suite scalar
    """
    def __init__(self, module_id, module_type):
        self.module_id = module_id
        self.module_type = module_type

    def _splice_key_value(self, key, value, vt):
        """
        splice key and value to string
        :param key: scalar name
        :param value: scalar value
        :return: string
        """
        # list or dict
        if vt == 1 or vt == 2:
            value_list = value.split(self.special_sep)
            value_text = self.small_sep.join(value_list)
        else:
            value_text = value
        return key + self.large_sep + value_text + self.linefeed

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
        for item in queryset.iterator():
            scalar_content += self._splice_key_value(
                item.name, item.value, item.value_type
            )
        return scalar_content
