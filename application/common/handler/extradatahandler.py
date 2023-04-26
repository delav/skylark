from django.conf import settings
from application.setupteardown.models import SetupTeardown
from application.setupteardown.serializers import SetupTeardownSerializers
from application.variable.models import Variable
from application.variable.serializers import VariableSerializers
from application.tag.models import Tag
from application.tag.serializers import TagSerializers
from application.caseentity.models import CaseEntity
from application.caseentity.serializers import CaseEntitySerializers
from application.infra.constant.constants import VARIABLE_KEY, FIXTURE_KEY, TAG_KEY, ENTITY_KEY


def get_model_extra_data(module_id, module_type, include_entity=False):
    variable_list, fixture, tag = [], {}, []
    if module_type != settings.MODULE_TYPE_META.get('TestCase'):
        variable_queryset = Variable.objects.filter(
            module_id=module_id,
            module_type=module_type
        )
        if variable_queryset.exists():
            variable_list = VariableSerializers(variable_queryset, many=True).data
    setup_teardown = SetupTeardown.objects.filter(
        module_id=module_id,
        module_type=module_type
    )
    tag_queryset = Tag.objects.filter(
        module_id=module_id,
        module_type=module_type
    )
    if setup_teardown.exists():
        fixture = SetupTeardownSerializers(setup_teardown.first()).data
    if tag_queryset.exists():
        tag = TagSerializers(tag_queryset, many=True).data
    extra_data_result = {
        VARIABLE_KEY: variable_list,
        FIXTURE_KEY: fixture,
        TAG_KEY: tag
    }
    if include_entity:
        entity_queryset = CaseEntity.objects.filter(test_case_id=module_id).order_by('seq_number')
        entities = CaseEntitySerializers(entity_queryset, many=True)
        extra_data_result[ENTITY_KEY] = entities.data
    return extra_data_result
