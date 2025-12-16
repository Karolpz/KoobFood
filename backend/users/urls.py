from django.urls import path, include


from . import views

app_name = 'users'
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', views.LogIn.as_view(), name='login'),
    path('logout/', views.LoggerLogoutView.as_view(), name='logout'),
    path('api/', include('users.api.urls')),
]