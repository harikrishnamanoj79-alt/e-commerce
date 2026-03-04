from django.urls import path
from . import views

urlpatterns = [

    path('', views.property_list, name='property_list'),

    path('get-specs/', views.get_category_specifications, name='get_specs'),

    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),

    path('agent/add/', views.agent_add_property, name='agent_add_property'),

    path('<slug:slug>/', views.property_detail, name='property_detail'),

]