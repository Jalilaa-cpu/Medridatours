from django.contrib import admin
from .models import Vehicle, Testimonial


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['name', 'transmission', 'fuel_type', 'daily_price', 'year', 'featured', 'available']
    list_filter = ['transmission', 'fuel_type', 'featured', 'available', 'air_conditioning']
    search_fields = ['name']
    list_editable = ['featured', 'available', 'daily_price']
    ordering = ['-featured', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'image', 'year')
        }),
        ('Specifications', {
            'fields': ('transmission', 'fuel_type', 'air_conditioning')
        }),
        ('Pricing & Availability', {
            'fields': ('daily_price', 'featured', 'available')
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'rating', 'active', 'created_at']
    list_filter = ['rating', 'active', 'created_at']
    search_fields = ['name', 'location', 'content']
    list_editable = ['active']
    ordering = ['-created_at']
