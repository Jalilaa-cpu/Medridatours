from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Testimonial

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'email', 'location', 'content', 'rating', 'vehicle_rented']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': _('Votre nom complet'),
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': _('votre@email.com (optionnel)')
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': _('Votre ville/pays (ex: Casablanca, France)')
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': _('Partagez votre expérience avec Medridatours...'),
                'rows': 4,
                'required': True
            }),
            'rating': forms.Select(
                choices=[(i, f"{i} étoile{'s' if i > 1 else ''}") for i in range(1, 6)],
                attrs={
                    'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                    'required': True
                }
            ),
            'vehicle_rented': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': _('Véhicule que vous avez loué (optionnel)')
            }),
        }
        labels = {
            'name': _('Nom complet'),
            'email': _('Email'),
            'location': _('Ville/Pays'),
            'content': _('Votre commentaire'),
            'rating': _('Votre note'),
            'vehicle_rented': _('Véhicule loué'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make rating field display stars
        self.fields['rating'].widget = forms.Select(
            choices=[
                (5, '⭐⭐⭐⭐⭐ Excellent'),
                (4, '⭐⭐⭐⭐☆ Très bien'),
                (3, '⭐⭐⭐☆☆ Bien'),
                (2, '⭐⭐☆☆☆ Correct'),
                (1, '⭐☆☆☆☆ À améliorer'),
            ],
            attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'required': True
            }
        )