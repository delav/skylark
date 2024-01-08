from application.status import ModuleType
from application.setupteardown.models import SetupTeardown
from application.setupteardown.serializers import SetupTeardownSerializers
from application.variable.models import Variable
from application.variable.serializers import VariableSerializers
from application.tag.models import Tag, ModuleTag
from application.caseentity.models import CaseEntity
from application.constant import EXTRA_VARIABLE_KEY, EXTRA_FIXTURE_KEY, EXTRA_TAG_KEY, EXTRA_ENTITY_KEY


def get_model_extra_data(module_id, module_type):
    variable_list, fixture_dict, tag_list = [], {}, []
    if module_type != ModuleType.CASE:
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
            fixture_dict = SetupTeardownSerializers(setup_teardown.first()).data
    tag_queryset = ModuleTag.objects.filter(
        module_id=module_id,
        module_type=module_type
    )
    if tag_queryset.exists():
        for item in tag_queryset.iterator():
            tag_info = {
                'id': item.id,
                'tag_id': item.tag_id,
            }
            tag_list.append(tag_info)
    extra_data_result = {
        EXTRA_VARIABLE_KEY: variable_list,
        EXTRA_FIXTURE_KEY: fixture_dict,
        EXTRA_TAG_KEY: tag_list
    }
    return extra_data_result


def get_model_simple_extra_data(module_id, module_type, include_entity=False):
    variable_list, fixture_dict, tag_list = [], {}, []
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
        'input_args', 'output_args', 'keyword_id', 'keyword_type'
    )
    if module_type != ModuleType.CASE:
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
    module_tags = ModuleTag.objects.filter(
        module_id=module_id,
        module_type=module_type
    )
    tag_queryset = Tag.objects.filter(
        id__in=[m.tag_id for m in module_tags]
    ).values(*tag_simple_fields)
    if setup_teardown.exists():
        fixture_dict = setup_teardown.first()
    if tag_queryset.exists():
        tag_list = list(tag_queryset)
    extra_data_result = {
        EXTRA_VARIABLE_KEY: variable_list,
        EXTRA_FIXTURE_KEY: fixture_dict,
        EXTRA_TAG_KEY: tag_list
    }
    if include_entity:
        entity_queryset = CaseEntity.objects.filter(
            test_case_id=module_id
        ).order_by('order').values(*entity_simple_fields)
        extra_data_result[EXTRA_ENTITY_KEY] = list(entity_queryset)
    return extra_data_result

