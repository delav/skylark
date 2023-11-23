from rest_framework import serializers
from application.executeparam.models import ExecuteParam


class ExecuteParamSerializers(serializers.ModelSerializer):

    class Meta:
        model = ExecuteParam
        fields = '__all__'
        read_only_fields = ('create_by', 'update_by')

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        request = self.context.get('request')
        user_email = request.user.email
        if request.method == 'POST':
            ret['create_by'] = user_email
        ret['update_by'] = user_email
        return ret
