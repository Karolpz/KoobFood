from django.urls import path

from . import views

app_name = 'restaurant'

urlpatterns = [
    path('', views.RestaurantListView.as_view(), name='restaurants_list'),
    path('manager/', views.RestaurantListManagerView.as_view(), name='restaurant_manager_list'),
    path('<int:pk>/', views.RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('manager/<int:pk>/', views.RestaurantManagerDetailView.as_view(), name='restaurant_manager_detail'),
    path('create/', views.RestaurantCeateView.as_view(), name='restaurant_create'),
    path('<int:pk>/update/', views.RestaurantUpdateView.as_view(), name='restaurant_update'),
    path('<int:pk>/delete/', views.RestaurantDeleteView.as_view(), name='restaurant_delete'),
    path('<int:restaurant_id>/tables/create/', views.RestaurantTableCreateView.as_view(), name='restaurant_table_create'),
    path('<int:pk>/tables/update/', views.RestaurantTableUpdateView.as_view(), name='restaurant_table_update'),
    path('<int:pk>/tables/delete/', views.RestaurantTableDeleteView.as_view(), name='restaurant_table_delete'),
]