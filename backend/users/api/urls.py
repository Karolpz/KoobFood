from .views import SignUpAPIView, get_my_profile
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path


urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='api_signup'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('me/', get_my_profile, name='api_get_my_profile'),  
]
