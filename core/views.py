from django.shortcuts import render
from fleet.models import Vehicle, Testimonial
from django.conf import settings


def home(request):
    """Homepage view with featured vehicles and testimonials"""
    featured_vehicles = Vehicle.objects.filter(featured=True, available=True)[:4]
    testimonials = Testimonial.objects.filter(active=True)[:3]
    
    context = {
        'featured_vehicles': featured_vehicles,
        'testimonials': testimonials,
        'whatsapp_number': settings.WHATSAPP_NUMBER,
    }
    
    return render(request, 'core/home.html', context)


def contact(request):
    """Contact page view"""
    context = {
        'whatsapp_number': settings.WHATSAPP_NUMBER,
    }
    
    return render(request, 'core/contact.html', context)


def about(request):
    """About page view"""
    context = {
        'whatsapp_number': settings.WHATSAPP_NUMBER,
    }
    
    return render(request, 'core/about.html', context)
