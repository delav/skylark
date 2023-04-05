from rest_framework import serializers
from application.projectversion.models import ProjectVersion


class ProjectVersionSerializers(serializers.ModelSerializer):

    content = serializers.CharField(read_only=True)
    sources = serializers.CharField(read_only=True)
    project_id = serializers.IntegerField()
    create_by = serializers.CharField(read_only=True)
    update_by = serializers.CharField(read_only=True)

    class Meta:
        model = ProjectVersion
        fields = (
            'id', 'project_id', 'branch', 'version', 'content',
            'sources', 'remark', 'create_at', 'update_at', 'create_by', 'update_by'
        )

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST':
            attrs['create_by'] = request.user.email
        attrs['update_by'] = request.user.email
        return attrs
