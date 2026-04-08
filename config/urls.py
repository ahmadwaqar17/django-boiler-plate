from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/dj-urls-panel/', include('dj_urls_panel.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include('config.api_urls')),
]
