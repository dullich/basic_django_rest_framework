 
from django.urls.conf import include, path
from rest_framework import routers
from .views import CityViewSet, CountryViewSet, OwnerViewSet, PropertyImageViewSet, PropertyTraceViewSet, PropertyViewSet, StateViewSet
#, UserSerializer

router = routers.DefaultRouter()
#outer.register(r"user", UserSerializer)
router.register(r"country", CountryViewSet)
router.register(r"state", StateViewSet)
router.register(r"city", CityViewSet)
router.register(r"owner", OwnerViewSet)
router.register(r"property", PropertyViewSet)
router.register(r"property-image", PropertyImageViewSet)
router.register(r"property-trace", PropertyTraceViewSet)

#define routes for realstateco_api app
urlpatterns = [
    path('', include(router.urls))
]