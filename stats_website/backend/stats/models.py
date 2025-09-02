from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class Role(models.Model):
    """Role model for user permissions"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    
    role_name = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        unique=True
    )
    
    def __str__(self) -> str:
        return self.role_name
    
    class Meta:
        db_table = 'roles'


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model using email as username"""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    role = models.ForeignKey(
        Role, 
        on_delete=models.CASCADE,
        related_name='users',
        db_column='role_id'
    )
    
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_admin(self) -> bool:
        return self.role.role_name == 'admin'
    
    class Meta:
        db_table = 'users'


class Country(models.Model):
    """Country model for vacation destinations"""
    country_name = models.CharField(max_length=100, unique=True)
    
    def __str__(self) -> str:
        return self.country_name
    
    class Meta:
        db_table = 'countries'
        verbose_name_plural = 'countries'


class Vacation(models.Model):
    """Vacation package model"""
    country = models.ForeignKey(
        Country, 
        on_delete=models.CASCADE,
        related_name='vacations'
    )
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10000)]
    )
    image_file = models.CharField(max_length=255)
    
    def clean(self):
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError("End date must be after start date")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def like_count(self) -> int:
        return self.likes.count()
    
    def is_liked_by_user(self, user) -> bool:
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False
    
    def __str__(self) -> str:
        return f"{self.country.country_name} - {self.description[:50]}"
    
    class Meta:
        db_table = 'vacations'
        ordering = ['start_date']


class Like(models.Model):
    """Like relationship between users and vacations"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='likes'
    )
    vacation = models.ForeignKey(
        Vacation, 
        on_delete=models.CASCADE,
        related_name='likes'
    )
    
    def __str__(self) -> str:
        return f"{self.user} likes {self.vacation.country.country_name}"
    
    class Meta:
        db_table = 'likes'
        unique_together = ['user', 'vacation']
