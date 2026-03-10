from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('agent/dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/categories/', views.admin_categories, name='admin_categories'),
    path('admin-dashboard/agents/', views.admin_agents, name='admin_agents'),
    path('agent/<str:username>/', views.agent_detail, name='agent_detail'),
    path('admin-dashboard/remove-agent/<int:user_id>/', views.remove_agent_role, name='remove_agent_role'),
    path('admin-dashboard/delete-agent/<int:user_id>/', views.delete_agent, name='delete_agent'),
    path('admin-dashboard/properties/', views.admin_properties, name='admin_properties'),
    path('admin-dashboard/spec-fields/', views.admin_spec_fields, name='admin_spec_fields'),
    path('admin-dashboard/spec-fields/delete/<int:pk>/', views.admin_delete_spec_field, name='admin_delete_spec_field'),
    path('admin-dashboard/property-specs/', views.admin_property_specs, name='admin_property_specs'),
    path('admin-dashboard/property-specs/add/', views.admin_add_property_spec, name='admin_add_property_spec'),
    path('admin-dashboard/add-property/', views.admin_add_property, name='admin_add_property'),
    path('admin-dashboard/edit-property/<int:pk>/', views.admin_edit_property, name='admin_edit_property'),
    path('admin-dashboard/delete-property/<int:pk>/',views.admin_delete_property,name='admin_delete_property'),
    path('profile/', views.profile_view, name='profile'),
    path('admin-dashboard/property/<int:pk>/',views.admin_property_detail,name='admin_property_detail'),
    path("delete-property-image/<int:image_id>/",views.admin_delete_property_image,name="admin_delete_property_image"),
    path("set-featured-image/<int:image_id>/",views.admin_set_featured_image,name="admin_set_featured_image"),
    path('admin-dashboard/users/', views.admin_users, name='admin_users'),
    path('admin-dashboard/contact-messages/', views.admin_contact_messages, name='admin_contact_messages'),
    path('admin-dashboard/change-role/<int:user_id>/', views.change_user_role, name='change_user_role')
    
    
]