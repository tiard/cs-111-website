from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('cs111.django.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('accounts/profile/', include('django_ssh.urls', namespace='ssh')),
]
