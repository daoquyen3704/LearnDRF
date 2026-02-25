from django.shortcuts import render
from django.db.models import Max
from api.serializers import OrderSerializer, ProductInfoSerializer, ProductSerializer
from api.models import Product, Order
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import generics

class ProductListAPIView(generics.ListAPIView):
    # queryset = Product.objects.all()
    # Cú pháp: model.objects.filter( field__lookup = value )
    # queryset = Product.objects.filter(stock__gt=0)
    # => SQL : SELECT * FROM product WHERE stock > 0;
    queryset = Product.objects.exclude(stock__gt=0)
     # => SQL : SELECT * FROM product WHERE stock <= 0;
    serializer_class = ProductSerializer

# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializers = ProductSerializer(products, many=True)
#     return Response({
#         'data': serializers.data
#     })

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #Muốn dùng product_id thay vì pk thì thêm lookup_url_kwarg
    lookup_url_kwarg = 'product_id'

# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializers = ProductSerializer(product)
#     return Response({
#         'data': serializers.data
#     })

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product') #tránh N+1 query, lấy luôn sp liên quan đến order
    serializer_class = OrderSerializer

# @api_view(['GET'])
# def order_list(request):
#     orders = Order.objects.prefetch_related('items__product')
#     serializers = OrderSerializer(orders, many=True)
#     return Response({
#         'data': serializers.data
#     })

class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product') #tránh N+1 query, lấy luôn sp liên quan đến order
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)
    
@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializers = ProductInfoSerializer({
        'products': products,
        'count': len(products),
        'max_price': products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response({
        'data': serializers.data
    })



