from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    # User Management
    path('accounts/', include('allauth.urls')),
    # Local apps
    path('app/', include('chatapp.urls')),
    path('api/', include('api.urls'))
]
