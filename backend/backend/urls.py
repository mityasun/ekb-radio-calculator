from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import custom_admin_login

urlpatterns = [
    path('admin/login/', custom_admin_login, name='admin_login'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

handler404 = 'backend.views.view_404'
handler429 = 'backend.views.view_429'

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
