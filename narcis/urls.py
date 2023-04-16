
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('base.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
]
