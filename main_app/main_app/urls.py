from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # new
    path('', include('products.urls', namespace='products')),  # 2nd
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)