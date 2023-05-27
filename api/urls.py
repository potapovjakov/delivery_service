from django.urls import include, path
from api.views import TruckViewSet, CargoViewSet
from rest_framework.routers import DefaultRouter


app_name = 'api'

router = DefaultRouter()
router.register(r'trucks', TruckViewSet)
router.register(r'cargos', CargoViewSet)


urlpatterns = [
    path('', include(router.urls))
]
