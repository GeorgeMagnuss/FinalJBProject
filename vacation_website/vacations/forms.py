from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, Role, Country, Vacation


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'})
    )
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'})
    )
    password1 = forms.CharField(
        min_length=4,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )
    password2 = forms.CharField(
        min_length=4,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        # Default to regular user role
        user_role, created = Role.objects.get_or_create(role_name='user')
        user.role = user_role
        
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email', 
            'class': 'form-control',
            'required': True
        })
    )
    password = forms.CharField(
        required=True,
        min_length=4,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password', 
            'class': 'form-control',
            'required': True
        })
    )


class VacationForm(forms.ModelForm):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        max_value=10000,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Vacation
        fields = ['country', 'description', 'start_date', 'end_date', 'price']
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if end_date <= start_date:
                raise ValidationError("End date must be after start date")
        
        return cleaned_data