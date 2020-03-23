from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('yutube-info/api/v1/videos/', include('youtube.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

