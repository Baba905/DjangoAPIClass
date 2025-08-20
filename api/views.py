from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer,ProductInfoSerializer
from api.models import Product, Order, OrderItem, User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
""""Function base view """

## Function base view for product class
# @api_view(['GET'])
# def product_list(request):
#     products= Product.objects.all()
#     serializer = ProductSerializer(products,many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def product_details(request,pk):
#     product= get_object_or_404(Product,pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)


# @api_view(['GET'])
# def order_list(request):
#     orders= Order.objects.prefetch_related('items', 'items__product')
#     serializer = OrderSerializer(orders,many=True)
#     return Response(serializer.data)


@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        "products":products,
        "count": len(products),
        "max_price": products.aggregate(max_price=Max('price'))['max_price']
    })
    print(products.aggregate(max_price=Max('price')))
    return Response(serializer.data)



""""Class base view"""
# https://www.django-rest-framework.org/api-guide/generic-views/#generic-views
# Class base view for product

class ProductList(generics.ListAPIView):
    #queryset = Product.objects.all()
    queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

class OrderList(generics.ListAPIView):
    queryset= Order.objects.prefetch_related('items', 'items__product')
    serializer_class = OrderSerializer


# Get the order from a specific user 
# https://www.django-rest-framework.org/api-guide/generic-views/#methods
class UserOrderList(generics.ListAPIView):
    queryset= Order.objects.prefetch_related('items', 'items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset= super().get_queryset()
        return queryset.filter(user = self.request.user)
