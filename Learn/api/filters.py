import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'price': ['exact', 'lt', 'gt', 'range'],
            'name': ['exact', 'icontains'], #icontains: tìm kiếm không phân biệt hoa thường, chứa chuỗi con
        }
        # url có dạng: /api/products/?price__gt=100&name__icontains=laptop