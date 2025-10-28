from django.urls import reverse_lazy
from .forms import RestaurantForm, RestaurantTableForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

from .models import Restaurant, Restaurant_Table

from rest_framework import generics, viewsets, permissions
from .serializers import RestaurantSerializer

# ------------------------RESTAURANT MANAGER--------------------------------

class RestaurantManagerMixin(LoginRequiredMixin, PermissionRequiredMixin):
    model = Restaurant

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(manager=self.request.user)
    
class RestaurantListManagerView(RestaurantManagerMixin, generic.ListView):
    template_name = 'restaurant/restaurant_manager_list.html'
    context_object_name = 'restaurant_list'
    permission_required = 'restaurant.view_restaurant'

class RestaurantManagerDetailView(RestaurantManagerMixin, generic.DetailView):
    template_name = 'restaurant/restaurant_manager_detail.html'
    context_object_name = 'restaurant_detail'
    permission_required = 'restaurant.view_restaurant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant_tables'] = self.object.tables.all()
        return context
    
class RestaurantCreateView( RestaurantManagerMixin, generic.CreateView):
    form_class = RestaurantForm
    template_name = 'restaurant/restaurant_create.html'
    permission_required = 'restaurant.add_restaurant'

    def form_valid(self, form):
        form.instance.manager = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('restaurant:restaurant_table_create', kwargs={'restaurant_id': self.object.pk})
    
class RestaurantUpdateView( RestaurantManagerMixin,generic.UpdateView):
    form_class = RestaurantForm
    template_name = 'restaurant/restaurant_update.html'
    permission_required = 'restaurant.change_restaurant'

    def get_success_url(self):
        return reverse_lazy('restaurant:restaurant_manager_detail', kwargs={'pk': self.object.pk})
    
class RestaurantDeleteView(RestaurantManagerMixin, generic.DeleteView):
    template_name = 'restaurant/restaurant_delete.html'
    success_url = reverse_lazy('restaurant:restaurant_manager_list')
    permission_required = 'restaurant.delete_restaurant'


# ------------------------RESTAURANTS CUSTOMER--------------------------------

class RestaurantListView(generic.ListView):
    model = Restaurant
    template_name = 'restaurant/restaurant_list.html'
    context_object_name = 'restaurant_list'
    paginate_by = 5
    
class RestaurantDetailView(generic.DetailView):
    model = Restaurant
    template_name = 'restaurant/restaurant_detail.html'
    context_object_name = 'restaurant_detail'

# ------------------------TABLES DU RESTAURANT--------------------------------

class RestaurantTableCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Restaurant_Table
    form_class = RestaurantTableForm
    template_name = 'restaurant_table/restaurant_table_create.html'
    success_url = reverse_lazy('restaurant:restaurant_manager_list')
    permission_required = 'restaurant.add_restaurant_table'

    def form_valid(self, form): 
        restaurant = Restaurant.objects.get(pk=self.kwargs['restaurant_id']) 
        if restaurant.manager != self.request.user: 
            return HttpResponseForbidden("Vous n'êtes pas autorisé à ajouter des tables à ce restaurant.") 
        form.instance.restaurant = restaurant 
        response = super().form_valid(form)

        if self.request.POST.get('action') == 'save':
            return redirect('restaurant:restaurant_table_create', restaurant_id=restaurant.pk)
        return response
    
class RestaurantTableUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Restaurant_Table
    form_class = RestaurantTableForm
    template_name = 'restaurant_table/restaurant_table_update.html'
    permission_required = 'restaurant.change_restaurant_table'

    def get_success_url(self):
        return reverse_lazy('restaurant:restaurant_manager_detail', kwargs={'pk': self.object.restaurant.pk})

    def get_queryset(self):
        return Restaurant_Table.objects.filter(restaurant__manager=self.request.user)
    
class RestaurantTableDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Restaurant_Table
    template_name = 'restaurant_table/restaurant_table_delete.html'
    success_url = reverse_lazy('restaurant:restaurant_list')
    permission_required = 'restaurant.delete_restaurant_table'

    def get_success_url(self):
        return reverse_lazy('restaurant:restaurant_manager_detail', kwargs={'pk': self.object.restaurant.pk})

    def get_queryset(self):
        return Restaurant_Table.objects.filter(restaurant__manager=self.request.user)
    
# ------------------------API VIEWS--------------------------------
class IsManagerOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.groups.filter(name='Manager').exists()

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.manager == request.user
        
class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsManagerOrReadOnlyPermission]
    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)

        
    
         

