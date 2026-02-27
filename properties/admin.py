from django.contrib import admin
from .models import Property, Category
from django.utils.html import format_html


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'preview')
    prepopulated_fields = {"slug": ("name",)}

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="40" style="object-fit:cover;" />', obj.image.url)
        return "-"


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'location', 'category', 'is_available')
    list_filter = ('category', 'is_available')
    prepopulated_fields = {"slug": ("title",)}