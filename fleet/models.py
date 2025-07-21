from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from urllib.parse import quote


class Vehicle(models.Model):
    TRANSMISSION_CHOICES = [
        ('manual', _('Manual')),
        ('automatic', _('Automatic')),
    ]
    
    FUEL_CHOICES = [
        ('gasoline', _('Gasoline')),
        ('diesel', _('Diesel')),
        ('hybrid', _('Hybrid')),
        ('electric', _('Electric')),
    ]
    
    name = models.CharField(_('Vehicle Name'), max_length=200)
    image = models.ImageField(_('Image'), upload_to='vehicles/')
    transmission = models.CharField(_('Transmission'), max_length=20, choices=TRANSMISSION_CHOICES)
    air_conditioning = models.BooleanField(_('Air Conditioning'), default=True)
    fuel_type = models.CharField(_('Fuel Type'), max_length=20, choices=FUEL_CHOICES)
    daily_price = models.DecimalField(_('Daily Price (MAD)'), max_digits=8, decimal_places=2)
    year = models.IntegerField(_('Year'))
    featured = models.BooleanField(_('Featured'), default=False)
    available = models.BooleanField(_('Available'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Vehicle')
        verbose_name_plural = _('Vehicles')
        ordering = ['-featured', 'name']
    
    def __str__(self):
        return self.name
    
    def whatsapp_link(self):
        """Generate WhatsApp booking link with pre-filled message"""
        base_url = f"https://wa.me/212629473725"
        message = f"Bonjour Medridatours, je souhaite réserver la {self.name} du [Date début] au [Date fin]."
        return f"{base_url}?text={quote(message)}"
    
    def get_transmission_display_french(self):
        """Get French display for transmission"""
        if self.transmission == 'manual':
            return 'Manuelle'
        elif self.transmission == 'automatic':
            return 'Automatique'
        return self.get_transmission_display()
    
    def get_fuel_display_french(self):
        """Get French display for fuel type"""
        fuel_map = {
            'gasoline': 'Essence',
            'diesel': 'Diesel',
            'hybrid': 'Hybride',
            'electric': 'Électrique'
        }
        return fuel_map.get(self.fuel_type, self.get_fuel_type_display())


class Testimonial(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    location = models.CharField(_('Location'), max_length=100)
    content = models.TextField(_('Content'))
    rating = models.IntegerField(_('Rating'), default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _('Testimonial')
        verbose_name_plural = _('Testimonials')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.rating}/5"
