from application.setupteardown.models import SetupTeardown
from application.setupteardown.serializers import SetupTeardownSerializers
from application.variable.models import Variable
from application.variable.serializers import VariableSerializers


def get_model_extra_data(module_id, module_type):
    variable_queryset = Variable.objects.filter(
        module_id=module_id,
        module_type=module_type
    )
    setup_teardown = SetupTeardown.objects.filter(
        module_id=module_id,
        module_type=module_type
    )
    variable_list, fixture = [], {}
    if variable_queryset.exists():
        variable_list = VariableSerializers(variable_queryset, many=True).data
    if setup_teardown.exists():
        fixture = SetupTeardownSerializers(setup_teardown.first()).data
    extra_data_result = {
        'variables': variable_list,
        'fixtures': fixture
    }
    return extra_data_result
