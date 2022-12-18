from rest_framework import serializers
from application.builder.models import Builder


class BuilderSerializers(serializers.ModelSerializer):
    
    start_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    end_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    build_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Builder
        fields = '__all__'
