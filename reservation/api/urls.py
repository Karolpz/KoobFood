from django.urls import path, include
from rest_framework_nested import routers
from .views import ReservationViewSet
from restaurant.api.views import RestaurantViewSet

router = routers.SimpleRouter()
router.register(r'', RestaurantViewSet, basename='restaurant')

reservation_router = routers.NestedSimpleRouter(router, r'', lookup='restaurant')
reservation_router.register(r'reservation', ReservationViewSet, basename='reservation')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(reservation_router.urls)),
]