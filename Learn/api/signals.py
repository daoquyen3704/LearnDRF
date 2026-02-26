from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product

#khi xóa hoặc thêm mới sản phẩm, sẽ xóa cache của danh sách sản phẩm 
#để đảm bảo dữ liệu luôn mới nhất khi truy cập lại.
@receiver([post_save, post_delete], sender=Product)
def clear_product_cache(sender, instance, **kwargs):
    cache.delete_pattern('product_list*')

