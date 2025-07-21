from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create a superuser for the admin panel'

    def handle(self, *args, **options):
        User = get_user_model()
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@medridatours.com',
                password='admin123'
            )
            self.stdout.write(
                self.style.SUCCESS('Superuser created successfully!')
            )
            self.stdout.write(
                self.style.SUCCESS('Username: admin')
            )
            self.stdout.write(
                self.style.SUCCESS('Password: admin123')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Superuser already exists')
            )
