from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from vacations.models import Role, User, Country, Vacation
from datetime import date, timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate database with initial data from init_db.sql'

    def handle(self, *args, **options):
        self.stdout.write('Populating database with initial data...')

        # Create roles
        admin_role, created = Role.objects.get_or_create(role_name='admin')
        user_role, created = Role.objects.get_or_create(role_name='user')
        
        if created:
            self.stdout.write('Created roles')

        # Create users
        admin_user, created = User.objects.get_or_create(
            email='admin@example.com',
            defaults={
                'first_name': 'Admin',
                'last_name': 'User',
                'role': admin_role,
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('adminpass')
            admin_user.save()
            self.stdout.write(f'Created admin user: {admin_user.email}')
        
        regular_user, created = User.objects.get_or_create(
            email='user@example.com',
            defaults={
                'first_name': 'Regular',
                'last_name': 'User',
                'role': user_role
            }
        )
        if created:
            regular_user.set_password('userpass')
            regular_user.save()
            self.stdout.write(f'Created regular user: {regular_user.email}')
        
        self.stdout.write('Created users')

        # Create countries
        countries_data = [
            'Israel', 'Spain', 'Italy', 'France', 'Germany',
            'Japan', 'Brazil', 'Argentina', 'United States', 
            'Australia', 'Colombia'
        ]
        
        countries = {}
        for country_name in countries_data:
            country, created = Country.objects.get_or_create(country_name=country_name)
            countries[country_name] = country
        
        self.stdout.write('Created countries')

        # Create vacations with future dates
        today = timezone.now().date()
        base_start = today + timedelta(days=30)  # Start 30 days from now
        
        vacations_data = [
            {
                'country': 'Israel',
                'description': 'Explore the vibrant city of Tel Aviv with its beautiful beaches, bustling markets, and rich history. Experience the perfect blend of ancient traditions and modern innovation.',
                'start_date': base_start + timedelta(days=0),
                'end_date': base_start + timedelta(days=9),
                'price': 1500,
                'image_file': 'telaviv.jpg'
            },
            {
                'country': 'Spain',
                'description': 'Discover the heart of Spain in Madrid with its world-class museums, royal palaces, and incredible cuisine. Immerse yourself in the Spanish culture and lifestyle.',
                'start_date': base_start + timedelta(days=15),
                'end_date': base_start + timedelta(days=25),
                'price': 1200,
                'image_file': 'madrid.jpg'
            },
            {
                'country': 'Italy',
                'description': 'You can create a dream vacation of famous artistic wonders and historic gems punctuated by top-notch dining in fabulous restaurants with a spirited vacation package.',
                'start_date': base_start + timedelta(days=30),
                'end_date': base_start + timedelta(days=39),
                'price': 1800,
                'image_file': 'rome.jpg'
            },
            {
                'country': 'France',
                'description': 'Experience the romance and elegance of Paris, the City of Light. Visit iconic landmarks, enjoy world-class cuisine, and immerse yourself in French culture.',
                'start_date': base_start + timedelta(days=45),
                'end_date': base_start + timedelta(days=51),
                'price': 2000,
                'image_file': 'paris.jpg'
            },
            {
                'country': 'Germany',
                'description': 'Explore Berlin, a city rich in history and culture. From historical sites to vibrant nightlife, Berlin offers something for every traveler.',
                'start_date': base_start + timedelta(days=60),
                'end_date': base_start + timedelta(days=67),
                'price': 1400,
                'image_file': 'berlin.jpg'
            },
            {
                'country': 'Japan',
                'description': 'Discover the fascinating blend of traditional and modern Japan in Tokyo. Experience ancient temples, cutting-edge technology, and incredible cuisine.',
                'start_date': base_start + timedelta(days=75),
                'end_date': base_start + timedelta(days=88),
                'price': 2500,
                'image_file': 'tokyo.jpg'
            },
            {
                'country': 'Brazil',
                'description': 'Experience the energy and beauty of Rio de Janeiro with its stunning beaches, vibrant culture, and iconic landmarks like Christ the Redeemer.',
                'start_date': base_start + timedelta(days=90),
                'end_date': base_start + timedelta(days=98),
                'price': 2200,
                'image_file': 'rio.jpg'
            },
            {
                'country': 'Argentina',
                'description': 'Explore the passionate city of Buenos Aires with its European architecture, tango culture, and excellent cuisine. A perfect blend of culture and excitement.',
                'start_date': base_start + timedelta(days=105),
                'end_date': base_start + timedelta(days=112),
                'price': 1900,
                'image_file': 'buenosaires.jpg'
            },
            {
                'country': 'United States',
                'description': 'Experience the energy of New York City, the city that never sleeps. From Broadway shows to world-class museums and diverse neighborhoods.',
                'start_date': base_start + timedelta(days=120),
                'end_date': base_start + timedelta(days=130),
                'price': 1600,
                'image_file': 'nyc.jpg'
            },
            {
                'country': 'Australia',
                'description': 'Discover Sydney with its iconic Opera House, beautiful harbor, and laid-back Australian culture. Perfect for adventure seekers and culture enthusiasts.',
                'start_date': base_start + timedelta(days=135),
                'end_date': base_start + timedelta(days=145),
                'price': 2300,
                'image_file': 'sydney.jpg'
            },
            {
                'country': 'Colombia',
                'description': 'Explore the vibrant city of Medellin, known for its perfect climate, innovative urban development, and warm Colombian hospitality.',
                'start_date': base_start + timedelta(days=150),
                'end_date': base_start + timedelta(days=157),
                'price': 2100,
                'image_file': 'medellin.jpg'
            },
            {
                'country': 'United States',
                'description': 'Experience the glamour and sunshine of Los Angeles with its beautiful beaches, Hollywood attractions, and diverse culture.',
                'start_date': base_start + timedelta(days=165),
                'end_date': base_start + timedelta(days=175),
                'price': 1800,
                'image_file': 'losangeles.jpg'
            }
        ]

        for vacation_data in vacations_data:
            country = countries[vacation_data['country']]
            vacation, created = Vacation.objects.get_or_create(
                country=country,
                start_date=vacation_data['start_date'],
                defaults={
                    'description': vacation_data['description'],
                    'end_date': vacation_data['end_date'],
                    'price': vacation_data['price'],
                    'image_file': vacation_data['image_file']
                }
            )

        self.stdout.write('Created vacations')
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with initial data!')
        )