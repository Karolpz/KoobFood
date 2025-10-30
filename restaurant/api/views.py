from rest_framework import viewsets
from .serializers import RestaurantSerializer, RestaurantTableSerializer
from koobfood.api.permissions import IsManagerOrReadOnlyPermission, IsManagerPermission
from ..models import Restaurant, Restaurant_Table
from rest_framework.exceptions import PermissionDenied

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsManagerOrReadOnlyPermission]
    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)

class RestaurantTableViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantTableSerializer
    permission_classes = [IsManagerPermission]

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_pk')
        return Restaurant_Table.objects.filter(
            restaurant_id=restaurant_id,
            restaurant__manager=self.request.user
        )
    def perform_create(self, serializer):
        restaurant_id = self.kwargs.get('restaurant_pk')
        restaurant = Restaurant.objects.get(id=restaurant_id)
        if restaurant.manager != self.request.user:
            raise PermissionDenied("You do not have permission to add tables to this restaurant.")
        serializer.save(restaurant=restaurant)
