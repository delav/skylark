from rest_framework import serializers
from application.product.models import Product


class ProductSerializers(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
