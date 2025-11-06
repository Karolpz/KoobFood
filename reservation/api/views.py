from .serializers import ReservationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from koobfood.api.permissions import IsOwnerOrManagerReadOnlyPermission
from ..models import Reservation
from restaurant.models import Restaurant
from rest_framework.response import Response

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrManagerReadOnlyPermission]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Reservation.objects.filter(restaurant__manager=user)
        return Reservation.objects.filter(customuser=user)
    
    def perform_create(self, serializer):
        restaurant_id=self.kwargs.get('restaurant_pk')
        serializer.save(customuser=self.request.user, restaurant_id=restaurant_id)
