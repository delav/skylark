from application.constant import MODULE_TYPE_META
from application.setupteardown.models import SetupTeardown
from application.setupteardown.serializers import SetupTeardownSerializers
from application.variable.models import Variable
from application.variable.serializers import VariableSerializers
from application.tag.models import Tag
from application.tag.serializers import TagSerializers
from application.caseentity.models import CaseEntity
from application.caseentity.serializers import CaseEntitySerializers
from infra.constant.constants import VARIABLE_KEY, FIXTURE_KEY, TAG_KEY, ENTITY_KEY


def get_model_extra_data(module_id, module_type, include_entity=False):
    variable_list, fixture, tag = [], {}, []
    if module_type != MODULE_TYPE_META.get('TestCase'):
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
        if setup_teardown.exists():
            fixture = SetupTeardownSerializers(setup_teardown.first()).data
    tag_queryset = Tag.objects.filter(
        module_id=module_id,
        module_type=module_type
    )
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
        extra_data_result.update({ENTITY_KEY: entities.data})
    return extra_data_result


def get_model_simple_extra_data(module_id, module_type, include_entity=False):
    variable_list, fixture, tag = [], {}, []
    variable_simple_fields = (
        'name', 'value'
    )
    setup_teardown_simple_fields = (
        'suite_setup', 'suite_teardown', 'test_setup', 'test_teardown'
    )
    tag_simple_fields = (
        'name',
    )
    entity_simple_fields = (
        'input_args', 'output_args', 'keyword_id'
    )
    if module_type != MODULE_TYPE_META.get('TestCase'):
        variable_queryset = Variable.objects.filter(
            module_id=module_id,
            module_type=module_type
        ).values(*variable_simple_fields)
        if variable_queryset.exists():
            variable_list = list(variable_queryset)
    setup_teardown = SetupTeardown.objects.filter(
        module_id=module_id,
        module_type=module_type
    ).values(*setup_teardown_simple_fields)
    tag_queryset = Tag.objects.filter(
        module_id=module_id,
        module_type=module_type
    ).values(*tag_simple_fields)
    if setup_teardown.exists():
        fixture = setup_teardown.first()
    if tag_queryset.exists():
        tag = list(tag_queryset)
    extra_data_result = {
        VARIABLE_KEY: variable_list,
        FIXTURE_KEY: fixture,
        TAG_KEY: tag
    }
    if include_entity:
        entity_queryset = CaseEntity.objects.filter(
            test_case_id=module_id
        ).order_by('seq_number').values(*entity_simple_fields)
        extra_data_result[ENTITY_KEY] = list(entity_queryset)
    return extra_data_result

