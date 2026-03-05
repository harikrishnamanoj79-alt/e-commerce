"""
URL configuration for estatepro project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Pages app
    path('', include('pages.urls')),

    # Properties app
    path('properties/', include('properties.urls')),

    # Accounts app
    path('accounts/', include('accounts.urls')),

    # Bookings app
    path('bookings/', include('bookings.urls')),
]