from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import Testimonial
from .forms import TestimonialForm


def home(request):
    """Homepage view with testimonials and testimonial form"""
    testimonials = Testimonial.objects.filter(active=True)[:6]
    form = TestimonialForm()
    
    # Handle testimonial form submission
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.active = True  # Auto-activate testimonials
            testimonial.save()
            messages.success(request, 'Merci pour votre témoignage ! Il est maintenant publié sur notre site.')
            return redirect('core:home')
        else:
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
    
    context = {
        'testimonials': testimonials,
        'testimonial_form': form,
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


def transport(request):
    """Transport touristique page view"""
    context = {
        'whatsapp_number': settings.WHATSAPP_NUMBER,
    }
    
    return render(request, 'core/transport.html', context)


def testimonials(request):
    """Testimonials page view with form"""
    testimonials = Testimonial.objects.filter(active=True).order_by('-created_at')
    form = TestimonialForm()
    
    # Handle testimonial form submission
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.active = False  # Require admin approval
            testimonial.save()
            messages.success(request, 'Merci pour votre témoignage ! Il sera publié après validation.')
            return redirect('core:testimonials')
        else:
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
    
    context = {
        'testimonials': testimonials,
        'testimonial_form': form,
        'whatsapp_number': settings.WHATSAPP_NUMBER,
    }
    
    return render(request, 'core/testimonials.html', context)
