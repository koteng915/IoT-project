from rest_framework import renderers
from rest_framework import routers
from django.urls import include, path
from .views import DmsViewSet

router= routers.DefaultRouter()
router.register(r'dms', DmsViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]