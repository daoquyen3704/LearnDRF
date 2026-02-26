from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'stock',
        )
    
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Giá phải lớn hơn 0"
            )
        return value

class OrderItemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(read_only=True) --> trả ra toàn bộ ttin của sp
    product_name = serializers.CharField(source='product.name', read_only=True)
    # chỉ trả ra tên sp
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ('order', 'product', 'quantity', 'product_name', 'product_price')
    
    
class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(item.item_subtotal for item in order_items)
    class Meta:
        model = Order
        fields = ( 'order_id', 'created_at', 'user', 'status', 'items', 'total_price')

#khi nào dùng Serializer, khi nào dùng ModelSerializer?
#ModelSerializer: tự động tạo field dựa trên model, tiết kiệm thời gian, phù hợp với các trường hợp đơn giản, không cần logic phức tạp Django biết model.
#Serializer: linh hoạt hơn, cho phép bạn định nghĩa field tùy chỉnh,
# validation phức tạp, hoặc khi bạn muốn serialize dữ liệu không liên quan đến model nào đó. 
# Dùng khi bạn cần kiểm soát hoàn toàn cách dữ liệu được serialize/deserialized.
class ProductInfoSerializer(serializers.Serializer):
    # get all products, count of products, max price
    products = ProductSerializer(many=True, read_only=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()