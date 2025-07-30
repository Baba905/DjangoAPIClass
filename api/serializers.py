from rest_framework import serializers
from .models import Product,Order,OrderItem

# Using Meta class permit to match type of each attributs of the serialized class

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'stock',
        ]

    def validate_price(self,price):
        
        if price <= 0:
            raise serializers.ValidationError("Price can't be a negative value")
        return price 