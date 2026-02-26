from rest_framework.filters import BaseFilterBackend
import django_filters
from .models import Product, Order


class InStockFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)
class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'price': ['exact', 'lt', 'gt', 'range'],
            'name': ['exact', 'icontains'], #icontains: tìm kiếm không phân biệt hoa thường, chứa chuỗi con
        }
        # url có dạng: /api/products/?price__gt=100&name__icontains=laptop

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'created_at': ['exact', 'lt', 'gt'],
        }