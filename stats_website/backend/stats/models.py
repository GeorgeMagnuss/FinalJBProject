from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class Role(models.Model):
    """
    Role model for user permissions - points to shared vacation database table.
    
    This is an unmanaged model that provides read-only access to the roles table
    created and managed by the main vacation website application.
    """
    """Role model for user permissions - points to shared vacation database table"""
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
        managed = False


class VacationUser(models.Model):
    """
    Vacation user model for accessing shared vacation database table.
    
    This is an unmanaged model that provides read-only access to the users table
    created and managed by the main vacation website application.
    """
    """Vacation user model for accessing shared vacation database table"""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    role = models.ForeignKey(
        Role, 
        on_delete=models.CASCADE,
        related_name='users',
        db_column='role_id'
    )
    password = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_admin(self) -> bool:
        return self.role.role_name == 'admin'
    
    class Meta:
        db_table = 'users'
        managed = False


class Country(models.Model):
    """
    Country model for vacation destinations - points to shared vacation database table.
    
    This is an unmanaged model that provides read-only access to the countries table
    created and managed by the main vacation website application.
    """
    """Country model for vacation destinations - points to shared vacation database table"""
    country_name = models.CharField(max_length=100, unique=True)
    
    def __str__(self) -> str:
        return self.country_name
    
    class Meta:
        db_table = 'countries'
        verbose_name_plural = 'countries'
        managed = False


class Vacation(models.Model):
    """
    Vacation package model - points to shared vacation database table.
    
    This is an unmanaged model that provides read-only access to the vacations table
    created and managed by the main vacation website application.
    """
    """Vacation package model - points to shared vacation database table"""
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
        managed = False


class Like(models.Model):
    """
    Like relationship between users and vacations - points to shared vacation database table.
    
    This is an unmanaged model that provides read-only access to the likes table
    created and managed by the main vacation website application.
    """
    """Like relationship between users and vacations - points to shared vacation database table"""
    user = models.ForeignKey(
        VacationUser, 
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
        managed = False
