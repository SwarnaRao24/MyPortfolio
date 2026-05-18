from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),       # <-- Fixed: Added the 's' to urls
    path('', include('portfolio.urls')),   # <-- Fixed: Changed the slash '/' to a dot '.'
]