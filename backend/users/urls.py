from django.urls import path, include
from django.contrib.auth.views import LogoutView


from . import views

app_name = 'users'
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', views.LogIn.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/', include('users.api.urls')),
]