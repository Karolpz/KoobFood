from .serializers import ReservationSerializer
from rest_framework import viewsets
from koobfood.api.permissions import IsManagerOrReadOnlyPermission, IsManagerPermission
from ..models import Reservation
from rest_framework.response import Response

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsManagerOrReadOnlyPermission]

    def perform_create(self, serializer):
        serializer.save(customuser=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Reservation.objects.filter(restaurant__manager=user)
        return Reservation.objects.filter(customuser=user)