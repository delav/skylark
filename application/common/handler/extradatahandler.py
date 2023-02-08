from application.setupteardown.models import SetupTeardown
from application.setupteardown.serializers import SetupTeardownSerializers
from application.variable.models import Variable
from application.variable.serializers import VariableSerializers
from application.tag.models import Tag
from application.tag.serializers import TagSerializers


def get_model_extra_data(module_id, module_type):
    variable_queryset = Variable.objects.filter(
        module_id=module_id,
        module_type=module_type
    )
    setup_teardown = SetupTeardown.objects.filter(
        module_id=module_id,
        module_type=module_type
    )
    tag_queryset = Tag.objects.filter(
        module_id=module_id,
        module_type=module_type
    )
    variable_list, fixture, tag = [], {}, []
    if variable_queryset.exists():
        variable_list = VariableSerializers(variable_queryset, many=True).data
    if setup_teardown.exists():
        fixture = SetupTeardownSerializers(setup_teardown.first()).data
    if tag_queryset.exists():
        tag = TagSerializers(tag_queryset, many=True).data
    extra_data_result = {
        'variables': variable_list,
        'fixtures': fixture,
        'tags': tag
    }
    return extra_data_result
