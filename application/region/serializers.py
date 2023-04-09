from rest_framework import serializers
from application.region.models import Region


class RegionSerializers(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = '__all__'
