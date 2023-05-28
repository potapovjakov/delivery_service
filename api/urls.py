from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CargoDetailViewSet, CargoViewSet, LocationDetailViewSet,
                       TruckViewSet)

app_name = 'api'

router = DefaultRouter()
router.register(r'trucks', TruckViewSet, basename='trucks')

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
        'locations/<str:pk>/',
        LocationDetailViewSet.as_view(),
        name='location_detail'
    )
]
