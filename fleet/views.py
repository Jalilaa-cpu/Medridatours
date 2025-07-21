from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Vehicle


def fleet_list(request):
    """Display all available vehicles with filtering options"""
    # Provide static car list for display
    cars = [
        {
            'img': 'dacia_logan.png',
            'name': 'Dacia Logan',
            'transmission': 'Automatique',
            'type': 'Sedan – Coffre 528 L',
            'fuel': 'Essence / Diesel',
            'price': '30 € / Jour',
        },
        {
            'img': 'dacia-duster.png',
            'name': 'Dacia Duster',
            'transmission': 'Manuelle',
            'type': 'SUV Compact – Coffre 445 L',
            'fuel': 'Diesel / Essence',
            'price': '40 € / Jour',
        },
        {
            'img': 'hyundai_tukson.png',
            'name': 'Hyundai Tucson',
            'transmission': 'Automatique',
            'type': 'SUV Familial – Coffre 620 L',
            'fuel': 'Hybride / Essence',
            'price': '82 € / Jour',
        },
        {
            'img': 'dacia_lodgy.png',
            'name': 'Dacia Lodgy',
            'transmission': 'Automatique',
            'type': '7 Places – Coffre modulable',
            'fuel': 'Diesel / Essence',
            'price': '45 € / Jour',
        },
        {
            'img': 'Fiat 500.png',
            'name': 'FIAT 500',
            'transmission': 'Automatique',
            'type': 'Citadine compacte',
            'fuel': 'Essence / Hybride',
            'price': '30 € / Jour',
        },
        {
            'img': 'renault_clio 5.jpg',
            'name': 'Renault Clio 5',
            'transmission': 'Manuelle',
            'type': 'Polyvalente – Coffre 391 L',
            'fuel': 'Diesel / Essence',
            'price': '30 € / Jour',
        },
        {
            'img': 'peugot_208.png',
            'name': 'Peugeot 208',
            'transmission': 'Manuelle',
            'type': 'Citadine – Coffre 311 L',
            'fuel': 'Essence / Diesel',
            'price': '30 € / Jour',
        },
        {
            'img': 'dacia_dokker.jpg',
            'name': 'Dacia Dokker',
            'transmission': 'Manuelle',
            'type': 'Utilitaire / Familiale – Grand coffre',
            'fuel': 'Diesel',
            'price': '30 € / Jour',
        },
        {
            'img': 'Hyundai-i10.jpg',
            'name': 'Hyundai i10',
            'transmission': 'Automatique',
            'type': 'Mini Citadine – Coffre 252 L',
            'fuel': 'Essence',
            'price': '30 € / Jour',
        },
        {
            'img': 'Kia-Sportage.jpeg',
            'name': 'Kia Sportage',
            'transmission': 'Automatique',
            'type': 'SUV Confort – Coffre 591 L',
            'fuel': 'Essence / Hybride',
            'price': '90 € / Jour',
        },
        {
            'img': 'Jeep-Renegade.png',
            'name': 'Jeep Renegade',
            'transmission': 'Manuelle',
            'type': 'SUV Aventure – Coffre 351 L',
            'fuel': 'Essence / Diesel',
            'price': '55 € / Jour',
        },
    ]
    # Provide filter context for template compatibility
    transmission = request.GET.get('transmission')
    fuel_type = request.GET.get('fuel_type')
    ac = request.GET.get('ac')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search = request.GET.get('search')
    context = {
        'cars': cars,
        'transmission_choices': Vehicle.TRANSMISSION_CHOICES,
        'fuel_choices': Vehicle.FUEL_CHOICES,
        'current_filters': {
            'transmission': transmission,
            'fuel_type': fuel_type,
            'ac': ac,
            'min_price': min_price,
            'max_price': max_price,
            'search': search,
        }
    }
    return render(request, 'fleet/fleet_list.html', context)


def vehicle_detail(request, vehicle_id):
    """Display detailed view of a specific vehicle"""
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, available=True)
    
    # Get related vehicles (same transmission or fuel type)
    related_vehicles = Vehicle.objects.filter(
        available=True
    ).exclude(id=vehicle.id).filter(
        Q(transmission=vehicle.transmission) | 
        Q(fuel_type=vehicle.fuel_type)
    )[:3]
    
    context = {
        'vehicle': vehicle,
        'related_vehicles': related_vehicles,
    }
    
    return render(request, 'fleet/vehicle_detail.html', context)


