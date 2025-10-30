from rest_framework_nested import routers
from .views import RestaurantViewSet, RestaurantTableViewSet
from django.urls import path, include


router = routers.SimpleRouter()
router.register(r'', RestaurantViewSet, basename='restaurant')

restaurants_router = routers.NestedSimpleRouter(router, r'', lookup='restaurant')
restaurants_router.register(r'tables', RestaurantTableViewSet, basename='restaurant-tables')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(restaurants_router.urls)),
]