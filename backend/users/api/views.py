from rest_framework import generics
from ..models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class SignUpAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_profile(request):
    return Response({
        'username': request.user.username,
        'email': request.user.email,
        'id': request.user.id
    })