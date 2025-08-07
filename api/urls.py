from django.urls import path
from . import views

urlpatterns =[
    path('products/', views.ProductList.as_view()),
    path('products/info/', views.product_info),
    path('products/<int:product_id>/', views.ProductDetail.as_view()),
    path('orders/', views.OrderList.as_view()),
]