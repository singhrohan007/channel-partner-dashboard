
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from dashboard.views import admin_login_view, admin_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('admin-login/', admin_login_view, name='admin_login'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),

]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)