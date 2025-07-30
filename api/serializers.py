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
    
class OrderItemSerializer(serializers.ModelSerializer):
    # We get all attributs of Product class
    ## product = ProductSerializer()
    # Use the below approch if you some attributs not all
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(max_digits=10,decimal_places=2,source='product.price')
    class Meta:
        model = OrderItem
        fields =[
            "product_name",
            "product_price",
            "quantity",
            "item_subtotal",
        ]
    
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True, read_only= True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)
    
    class Meta:
        model = Order
        fields = [
            "order_id",
            "user",
            "created_at",
            "status",
            "items",
            "total_price"
        ]

