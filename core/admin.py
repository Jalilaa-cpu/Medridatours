from django.contrib import admin
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'vehicle_rented', 'location', 'active', 'created_at']
    list_filter = ['rating', 'active', 'created_at', 'vehicle_rented']
    search_fields = ['name', 'content', 'location', 'vehicle_rented']
    list_editable = ['active']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informations client', {
            'fields': ('name', 'email', 'location', 'vehicle_rented')
        }),
        ('Témoignage', {
            'fields': ('rating', 'content')
        }),
        ('Publication', {
            'fields': ('active',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request)
    
    actions = ['make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        queryset.update(active=True)
        self.message_user(request, f"{queryset.count()} témoignages ont été publiés.")
    make_active.short_description = "Publier les témoignages sélectionnés"
    
    def make_inactive(self, request, queryset):
        queryset.update(active=False)
        self.message_user(request, f"{queryset.count()} témoignages ont été masqués.")
    make_inactive.short_description = "Masquer les témoignages sélectionnés"
