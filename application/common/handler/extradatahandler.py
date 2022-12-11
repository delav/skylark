from application.setupteardown.models import SetupTeardown
from application.setupteardown.serializers import SetupTeardownSerializers
from application.variable.models import Variable
from application.variable.serializers import VariableSerializers


def get_model_extra_data(module_id, module_type):
    variable_queryset = Variable.objects.filter(
        module_id=module_id,
        module_type=module_type
    )
    setup_teardown_queryset = SetupTeardown.objects.filter(
        module_id=module_id,
        module_type=module_type
    )
    extra_data_result = {
        'variable': VariableSerializers(variable_queryset, many=True).data,
        'fixture': SetupTeardownSerializers(setup_teardown_queryset, many=True).data
    }
    return extra_data_result
