from django.shortcuts import render
from django.db.models import Max
from api.serializers import OrderSerializer, ProductInfoSerializer, ProductSerializer
from api.models import Product, Order
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import (IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny)
from rest_framework.views import APIView
from api.filters import InStockFilterBackend, ProductFilter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
class ProductListAPIView(generics.ListAPIView):
    # queryset = Product.objects.all()
    # Cú pháp: model.objects.filter( field__lookup = value )
    queryset = Product.objects.filter(stock__gt=0)
    # => SQL : SELECT * FROM product WHERE stock > 0;
    # queryset = Product.objects.exclude(stock__gt=0)
     # => SQL : SELECT * FROM product WHERE stock <= 0;
    serializer_class = ProductSerializer

# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializers = ProductSerializer(products, many=True)
#     return Response({
#         'data': serializers.data
#     })

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, 
                       filters.SearchFilter, 
                       filters.OrderingFilter,
                       InStockFilterBackend]
    filterset_class = ProductFilter #dùng filterset riêng, có thể định nghĩa logic lọc phức tạp hơn
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name']

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()

    serializer_class = ProductSerializer
    #Muốn dùng product_id thay vì pk thì thêm lookup_url_kwarg
    # lookup_url_kwarg = 'product_id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product') #tránh N+1 query, lấy luôn sp liên quan đến order
    serializer_class = OrderSerializer



class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product') #tránh N+1 query, lấy luôn sp liên quan đến order
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated] #chỉ cho phép user đã đăng nhập truy cập

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializers = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response({
            'data': serializers.data
        })
    




