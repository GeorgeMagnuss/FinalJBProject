from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, timedelta
from .models import Role, Country, Vacation, Like

User = get_user_model()


class ModelTestCase(TestCase):
    
    def setUp(self):
        self.admin_role = Role.objects.create(role_name='admin')
        self.user_role = Role.objects.create(role_name='user')
        
        self.admin_user = User.objects.create_user(
            email='admin@test.com',
            password='testpass123',
            first_name='Admin',
            last_name='Test',
            role=self.admin_role
        )
        
        self.regular_user = User.objects.create_user(
            email='user@test.com',
            password='testpass123',
            first_name='User',
            last_name='Test',
            role=self.user_role
        )
        
        self.country = Country.objects.create(country_name='Test Country')
        
        self.vacation = Vacation.objects.create(
            country=self.country,
            description='Test vacation description',
            start_date=date.today() + timedelta(days=30),
            end_date=date.today() + timedelta(days=40),
            price=1000.00,
            image_file='test.jpg'
        )
    
    def test_user_model(self):
        self.assertEqual(str(self.admin_user), 'Admin Test')
        self.assertTrue(self.admin_user.is_admin)
        self.assertFalse(self.regular_user.is_admin)
    
    def test_vacation_model(self):
        self.assertEqual(str(self.vacation), 'Test Country - Test vacation description')
        self.assertEqual(self.vacation.like_count, 0)
        self.assertFalse(self.vacation.is_liked_by_user(self.regular_user))
    
    def test_like_functionality(self):
        # User likes vacation
        like = Like.objects.create(user=self.regular_user, vacation=self.vacation)
        self.assertEqual(self.vacation.like_count, 1)
        self.assertTrue(self.vacation.is_liked_by_user(self.regular_user))
        
        # User unlikes vacation
        like.delete()
        self.assertEqual(self.vacation.like_count, 0)
        self.assertFalse(self.vacation.is_liked_by_user(self.regular_user))


class ViewTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        
        self.admin_role = Role.objects.create(role_name='admin')
        self.user_role = Role.objects.create(role_name='user')
        
        self.admin_user = User.objects.create_user(
            email='admin@test.com',
            password='testpass123',
            first_name='Admin',
            last_name='Test',
            role=self.admin_role
        )
        
        self.regular_user = User.objects.create_user(
            email='user@test.com',
            password='testpass123',
            first_name='User',
            last_name='Test',
            role=self.user_role
        )
        
        self.country = Country.objects.create(country_name='Test Country')
    
    def test_login_view(self):
        # Test GET request
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
        # Test valid login
        response = self.client.post(reverse('login'), {
            'email': 'user@test.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
    
    def test_register_view(self):
        # Test GET request
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        
        # Test valid registration
        response = self.client.post(reverse('register'), {
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@test.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(email='newuser@test.com').exists())
    
    def test_vacation_list_requires_login(self):
        response = self.client.get(reverse('vacation_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_vacation_list_authenticated(self):
        self.client.login(email='user@test.com', password='testpass123')
        response = self.client.get(reverse('vacation_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_add_vacation_access(self):
        # Regular user should be denied
        self.client.login(email='user@test.com', password='testpass123')
        response = self.client.get(reverse('add_vacation'))
        self.assertEqual(response.status_code, 302)  # Redirect due to permission denied
        
        # Admin should have access
        self.client.login(email='admin@test.com', password='testpass123')
        response = self.client.get(reverse('add_vacation'))
        self.assertEqual(response.status_code, 200)
    
    def test_like_toggle_functionality(self):
        vacation = Vacation.objects.create(
            country=self.country,
            description='Test vacation',
            start_date=date.today() + timedelta(days=30),
            end_date=date.today() + timedelta(days=40),
            price=1000.00,
            image_file='test.jpg'
        )
        
        self.client.login(email='user@test.com', password='testpass123')
        
        # Like vacation
        response = self.client.post(reverse('toggle_like', args=[vacation.id]))
        self.assertEqual(response.status_code, 200)
        
        # Verify like exists
        self.assertTrue(Like.objects.filter(user=self.regular_user, vacation=vacation).exists())


class FormTestCase(TestCase):
    
    def setUp(self):
        self.admin_role = Role.objects.create(role_name='admin')
        self.user_role = Role.objects.create(role_name='user')
        self.country = Country.objects.create(country_name='Test Country')
    
    def test_user_registration_form_valid(self):
        from .forms import UserRegistrationForm
        
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_user_registration_form_duplicate_email(self):
        from .forms import UserRegistrationForm
        
        # User already exists
        User.objects.create_user(
            email='existing@example.com',
            password='testpass123',
            first_name='Existing',
            last_name='User',
            role=self.user_role
        )
        
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'existing@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_vacation_form_valid(self):
        from .forms import VacationForm
        
        form_data = {
            'country': self.country.id,
            'description': 'Test vacation description',
            'start_date': date.today() + timedelta(days=30),
            'end_date': date.today() + timedelta(days=40),
            'price': 1000.00
        }
        form = VacationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_vacation_form_invalid_dates(self):
        from .forms import VacationForm
        
        form_data = {
            'country': self.country.id,
            'description': 'Test vacation description',
            'start_date': date.today() + timedelta(days=40),
            'end_date': date.today() + timedelta(days=30),  # End before start - should fail
            'price': 1000.00
        }
        form = VacationForm(data=form_data)
        self.assertFalse(form.is_valid())
