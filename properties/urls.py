from django.urls import path
from . import views

urlpatterns = [

    path('', views.property_list, name='property_list'),

    path('get-specs/', views.get_category_specifications, name='get_specs'),

    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),

    path('agent/add/', views.agent_add_property, name='agent_add_property'),

    path('<slug:slug>/', views.property_detail, name='property_detail'),
    path("agent/property/edit/<int:pk>/",views.agent_edit_property,name="agent_edit_property"),
    path("agent/property/<int:pk>/",views.agent_property_detail,name="agent_property_detail"),
    path("agent/property/delete/<int:pk>/",views.agent_delete_property,name="agent_delete_property"),
    path("agent/booking/update/<int:booking_id>/<str:status>/",views.agent_update_booking,name="agent_update_booking")

]