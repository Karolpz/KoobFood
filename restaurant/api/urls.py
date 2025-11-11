from rest_framework_nested import routers
from .views import RestaurantViewSet, RestaurantTableViewSet
from django.urls import path, include


router = routers.SimpleRouter()
router.register(r'', RestaurantViewSet, basename='api_restaurant')

restaurants_router = routers.NestedSimpleRouter(router, r'', lookup='api_restaurant')
restaurants_router.register(r'tables', RestaurantTableViewSet, basename='api_restaurant_tables')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(restaurants_router.urls)),
]