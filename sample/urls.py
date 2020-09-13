from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from hero.views import HeroViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'heroes', HeroViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
