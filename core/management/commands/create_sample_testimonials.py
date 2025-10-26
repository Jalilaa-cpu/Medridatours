from django.core.management.base import BaseCommand
from core.models import Testimonial

class Command(BaseCommand):
    help = 'Create sample testimonials for testing'

    def handle(self, *args, **options):
        # Sample testimonials in French
        testimonials_data = [
            {
                'name': 'Ahmed Bennani',
                'location': 'Casablanca, Maroc',
                'content': 'Excellent service ! J\'ai loué une Dacia Logan pour 3 jours à Essaouira. Véhicule propre, climatisation parfaite, et livraison à l\'aéroport très ponctuelle. L\'équipe Medridatours est très professionnelle. Je recommande vivement !',
                'rating': 5,
                'vehicle_rented': 'Dacia Logan',
                'active': True
            },
            {
                'name': 'Sophie Martin',
                'location': 'Lyon, France',
                'content': 'Parfait pour découvrir Essaouira et ses environs ! Le Hyundai Tucson était spacieux et confortable. Service avec caution très transparent, pas de surprises. Communication via WhatsApp très pratique. Merci Medridatours !',
                'rating': 5,
                'vehicle_rented': 'Hyundai Tucson',
                'active': True
            },
            {
                'name': 'Youssef Alami',
                'location': 'Marrakech, Maroc',
                'content': 'Super expérience ! Véhicule en excellent état, prix raisonnable avec la caution. L\'équipe a été très réactive sur WhatsApp pour toutes mes questions. La Dacia Duster était parfaite pour mes excursions.',
                'rating': 4,
                'vehicle_rented': 'Dacia Duster',
                'active': True
            },
            {
                'name': 'Maria Garcia',
                'location': 'Madrid, Espagne',
                'content': 'Très satisfaite de mon séjour à Essaouira grâce à Medridatours ! Service professionnel, voiture impeccable (Kia Sportage), et tarifs honnêtes. Je reviendrai certainement lors de mon prochain voyage au Maroc.',
                'rating': 5,
                'vehicle_rented': 'Kia Sportage',
                'active': True
            },
            {
                'name': 'Omar Benali',
                'location': 'Essaouira, Maroc',
                'content': 'Agence locale de confiance ! J\'ai loué plusieurs fois chez Medridatours, toujours satisfait. Véhicules bien entretenus, service avec caution sans problème. Les propriétaires sont très accueillants.',
                'rating': 5,
                'vehicle_rented': 'Dacia Lodgy',
                'active': True
            },
            {
                'name': 'Jennifer Smith',
                'location': 'London, UK',
                'content': 'Great car rental experience in Essaouira! Clean vehicle, easy WhatsApp communication, and fair deposit policy. The team was very helpful with directions and local recommendations. Highly recommended!',
                'rating': 4,
                'vehicle_rented': 'Renault Clio 5',
                'active': True
            }
        ]

        # Create testimonials
        created_count = 0
        for data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                name=data['name'],
                content=data['content'],
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created testimonial: {testimonial.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Testimonial already exists: {testimonial.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new testimonials!')
        )