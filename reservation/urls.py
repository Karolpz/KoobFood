from django.urls import path

from . import views

app_name = 'reservation'    
urlpatterns = [
    path('<restaurant_id>/create/', views.ReservationCreateView.as_view(), name='reservation_create'),
    path ('<restaurant_id>/<reservation_id>', views.ReservationSuccessView.as_view(), name='reservation_success'),
    path('<restaurant_id>/signup_or_login/', views.signup_or_login, name='signup_or_login'),
    path('<restaurant_id>/manager/list/', views.ReservationManagerListView.as_view(), name='reservation_manager_list'),
    path('manager/<int:pk>/', views.ReservationManagerDetailView.as_view(), name='reservation_manager_detail'),
    ]