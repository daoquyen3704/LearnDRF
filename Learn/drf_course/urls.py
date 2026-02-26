from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('silk/', include('silk.urls', namespace='silk')),
]

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += [
    # --- SWAGGER CONFIG ---
    # 1. File schema (dạng YAML/JSON) tải về máy
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # 2. Giao diện Swagger UI (Dùng cái này nhiều nhất)
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'),
	     name='swagger-ui'),
    
    # 3. Giao diện Redoc (Giao diện thay thế, nhìn đẹp
    # hơn nhưng không test được)
    path('redoc/', 
	    SpectacularRedocView.as_view(url_name='schema'), 
	    name='redoc'),
]



