from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
import json
from .models import Role, User, Country, Vacation, Like


class StatsAPITestCase(TestCase):
    """Test cases for Statistics API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create roles
        self.admin_role = Role.objects.create(role_name='admin')
        self.user_role = Role.objects.create(role_name='user')
        
        # Create admin user
        self.admin_user = User.objects.create_user(
            email='admin@test.com',
            password='admin123',
            first_name='Admin',
            last_name='Test',
            role=self.admin_role
        )
        
        # Create regular user
        self.regular_user = User.objects.create_user(
            email='user@test.com',
            password='user123',
            first_name='User',
            last_name='Test',
            role=self.user_role
        )
        
        # Create countries
        self.country1 = Country.objects.create(country_name='Italy')
        self.country2 = Country.objects.create(country_name='Spain')
        
        # Create vacations with different timing
        today = timezone.now().date()
        
        # Past vacation
        self.past_vacation = Vacation.objects.create(
            country=self.country1,
            description='Past Rome vacation',
            start_date=today - timedelta(days=20),
            end_date=today - timedelta(days=10),
            price=1500,
            image_file='rome.jpg'
        )
        
        # Ongoing vacation
        self.ongoing_vacation = Vacation.objects.create(
            country=self.country2,
            description='Ongoing Madrid vacation',
            start_date=today - timedelta(days=5),
            end_date=today + timedelta(days=5),
            price=1200,
            image_file='madrid.jpg'
        )
        
        # Future vacation
        self.future_vacation = Vacation.objects.create(
            country=self.country1,
            description='Future Florence vacation',
            start_date=today + timedelta(days=10),
            end_date=today + timedelta(days=20),
            price=1800,
            image_file='florence.jpg'
        )
        
        # Create likes
        Like.objects.create(user=self.regular_user, vacation=self.past_vacation)
        Like.objects.create(user=self.admin_user, vacation=self.ongoing_vacation)

    def test_login_success_admin(self):
        """Test successful admin login"""
        response = self.client.post(
            reverse('login'),
            data=json.dumps({'email': 'admin@test.com', 'password': 'admin123'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_login_fail_regular_user(self):
        """Test that regular users cannot login to stats"""
        response = self.client.post(
            reverse('login'),
            data=json.dumps({'email': 'user@test.com', 'password': 'user123'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content)
        self.assertFalse(data['success'])

    def test_login_fail_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(
            reverse('login'),
            data=json.dumps({'email': 'admin@test.com', 'password': 'wrong'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)

    def test_vacation_stats_authenticated(self):
        """Test vacation stats endpoint with authenticated admin"""
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('vacation_stats'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['pastVacations'], 1)
        self.assertEqual(data['ongoingVacations'], 1)
        self.assertEqual(data['futureVacations'], 1)

    def test_vacation_stats_unauthenticated(self):
        """Test vacation stats endpoint without authentication"""
        response = self.client.get(reverse('vacation_stats'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_vacation_stats_non_admin(self):
        """Test vacation stats endpoint with non-admin user"""
        self.client.force_login(self.regular_user)
        response = self.client.get(reverse('vacation_stats'))
        self.assertEqual(response.status_code, 403)

    def test_total_users(self):
        """Test total users endpoint"""
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('total_users'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['totalUsers'], 2)

    def test_total_likes(self):
        """Test total likes endpoint"""
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('total_likes'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['totalLikes'], 2)

    def test_likes_distribution(self):
        """Test likes distribution endpoint"""
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('likes_distribution'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 3)  # 3 vacations
        
        # Check distribution structure
        for item in data:
            self.assertIn('destination', item)
            self.assertIn('likes', item)

    def test_logout(self):
        """Test logout endpoint"""
        self.client.force_login(self.admin_user)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
