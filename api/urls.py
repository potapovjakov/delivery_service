from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (CargoDetailViewSet, CargoViewSet, LocationDetailViewSet,
                       LocationViewSet, TruckDetailViewSet, TruckViewSet)

app_name = 'api'

router = SimpleRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(
        'cargos/',
        CargoViewSet.as_view(),
        name='cargos'
    ),
    path(
        'cargos/<int:pk>/',
        CargoDetailViewSet.as_view(),
        name='cargo_detail'
    ),
    path(
        'locations/',
        LocationViewSet.as_view(),
        name='locations'
    ),
    path(
        'locations/<str:pk>/',
        LocationDetailViewSet.as_view(),
        name='location_detail'
    ),
    path(
        'trucks/',
        TruckViewSet.as_view(),
        name='trucks'
    ),
    path(
        'trucks/<str:pk>/',
        TruckDetailViewSet.as_view(),
        name='trucks_detail'
    ),
]
