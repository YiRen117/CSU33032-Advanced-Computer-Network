from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('Site/', include('Site.urls')),
    path('admin/', admin.site.urls),
    path('', include('Site.urls')),
]