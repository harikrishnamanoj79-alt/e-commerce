from django.contrib import admin
from .models import VisitBooking


@admin.register(VisitBooking)
class VisitBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'property', 'visit_date', 'status', 'created_at')
    list_filter = ('status', 'visit_date')
    search_fields = ('name', 'email', 'phone')