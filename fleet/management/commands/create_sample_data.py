from django.core.management.base import BaseCommand
from fleet.models import Vehicle, Testimonial


class Command(BaseCommand):
    help = 'Create sample data for the Medridatours website'

    def handle(self, *args, **options):
        # Create sample vehicles
        vehicles_data = [
            {
                'name': 'Renault Clio',
                'transmission': 'manual',
                'air_conditioning': True,
                'fuel_type': 'gasoline',
                'daily_price': 250.00,
                'year': 2022,
                'featured': True,
                'available': True,
            },
            {
                'name': 'Peugeot 208',
                'transmission': 'manual',
                'air_conditioning': True,
                'fuel_type': 'gasoline',
                'daily_price': 280.00,
                'year': 2023,
                'featured': True,
                'available': True,
            },
            {
                'name': 'Dacia Sandero',
                'transmission': 'manual',
                'air_conditioning': True,
                'fuel_type': 'gasoline',
                'daily_price': 220.00,
                'year': 2021,
                'featured': False,
                'available': True,
            },
            {
                'name': 'Hyundai i10',
                'transmission': 'manual',
                'air_conditioning': True,
                'fuel_type': 'gasoline',
                'daily_price': 200.00,
                'year': 2022,
                'featured': False,
                'available': True,
            },
            {
                'name': 'Toyota Yaris',
                'transmission': 'automatic',
                'air_conditioning': True,
                'fuel_type': 'hybrid',
                'daily_price': 350.00,
                'year': 2023,
                'featured': True,
                'available': True,
            },
            {
                'name': 'Volkswagen Polo',
                'transmission': 'manual',
                'air_conditioning': True,
                'fuel_type': 'gasoline',
                'daily_price': 270.00,
                'year': 2022,
                'featured': False,
                'available': True,
            },
            {
                'name': 'Fiat 500',
                'transmission': 'manual',
                'air_conditioning': True,
                'fuel_type': 'gasoline',
                'daily_price': 240.00,
                'year': 2021,
                'featured': True,
                'available': True,
            },
            {
                'name': 'Nissan Micra',
                'transmission': 'automatic',
                'air_conditioning': True,
                'fuel_type': 'gasoline',
                'daily_price': 300.00,
                'year': 2023,
                'featured': False,
                'available': True,
            },
        ]

        for vehicle_data in vehicles_data:
            vehicle, created = Vehicle.objects.get_or_create(
                name=vehicle_data['name'],
                defaults=vehicle_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created vehicle: {vehicle.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Vehicle already exists: {vehicle.name}')
                )

        # Create sample testimonials
        testimonials_data = [
            {
                'name': 'Sarah Johnson',
                'location': 'Londres, UK',
                'content': 'Service excellent ! La voiture était parfaite et la livraison à l\'aéroport très pratique. Je recommande vivement Medridatours pour votre séjour à Essaouira.',
                'rating': 5,
                'active': True,
            },
            {
                'name': 'Mohammed Al-Rashid',
                'location': 'Dubaï, UAE',
                'content': 'Très satisfait de mon expérience avec Medridatours. La réservation via WhatsApp est simple et l\'équipe est très professionnelle.',
                'rating': 5,
                'active': True,
            },
            {
                'name': 'Marie Dubois',
                'location': 'Paris, France',
                'content': 'Parfait pour explorer Essaouira ! Voiture propre, pas de caution demandée et support client au top. Merci Medridatours !',
                'rating': 5,
                'active': True,
            },
            {
                'name': 'Carlos Rodriguez',
                'location': 'Madrid, Espagne',
                'content': 'Excellent service, prix raisonnables et voitures en parfait état. Je reviendrai certainement lors de mon prochain voyage.',
                'rating': 4,
                'active': True,
            },
            {
                'name': 'Emma Wilson',
                'location': 'New York, USA',
                'content': 'Amazing experience! The car was perfect for exploring the beautiful city of Essaouira. Great customer service and very convenient.',
                'rating': 5,
                'active': True,
            },
        ]

        for testimonial_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                name=testimonial_data['name'],
                defaults=testimonial_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created testimonial: {testimonial.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Testimonial already exists: {testimonial.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Sample data created successfully!')
        )
