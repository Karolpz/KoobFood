from rest_framework import viewsets, generics
from .serializers import RestaurantSerializer, RestaurantTableSerializer
from koobfood.api.permissions import IsManagerOrReadOnlyPermission, IsManagerPermission
from ..models import Restaurant, Restaurant_Table
from rest_framework.response import Response
from rest_framework.decorators import action

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsManagerOrReadOnlyPermission]
    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)
    
    @action(detail=False, methods=['get'] , permission_classes=[IsManagerPermission])
    def my_restaurants(self, request):
        user = request.user
        restaurants = Restaurant.objects.filter(manager=user)
        serializer = self.get_serializer(restaurants, many=True)
        return Response(serializer.data)

class RestaurantTableViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantTableSerializer
    permission_classes = [IsManagerPermission]

    def get_queryset(self):
        restaurant_id = self.kwargs.get('api_restaurant_pk')
        return Restaurant_Table.objects.filter(
            restaurant_id=restaurant_id,
            restaurant__manager=self.request.user
        )
    def perform_create(self, serializer):
        restaurant_id = self.kwargs.get('api_restaurant_pk')
        restaurant = Restaurant.objects.get(id=restaurant_id)
        serializer.save(restaurant=restaurant)
