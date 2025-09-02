from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from .models import User, Vacation, Like, Role, Country
from .forms import UserRegistrationForm, UserLoginForm, VacationForm


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful!')
            login(request, user, backend='vacations.backends.EmailBackend')
            return redirect('vacation_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'vacations/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('vacation_list')
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserLoginForm()
    
    return render(request, 'vacations/login.html', {'form': form})


def login_simple_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('vacation_list')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserLoginForm()
    
    return render(request, 'vacations/login_simple.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def vacation_list_view(request):
    vacations = Vacation.objects.all().order_by('start_date')
    
    # Check if user liked each vacation
    for vacation in vacations:
        vacation.user_liked = vacation.is_liked_by_user(request.user)
    
    context = {
        'vacations': vacations,
        'is_admin': request.user.is_admin
    }
    
    if request.user.is_admin:
        return render(request, 'vacations/admin_vacation_list.html', context)
    else:
        return render(request, 'vacations/vacation_list.html', context)


@login_required
def add_vacation_view(request):
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('vacation_list')
    
    if request.method == 'POST':
        form = VacationForm(request.POST, request.FILES)
        if form.is_valid():
            vacation = form.save(commit=False)
            
            # Handle image upload
            if 'image' in request.FILES:
                image = request.FILES['image']
                filename = f"vacation_images/{image.name}"
                path = default_storage.save(filename, ContentFile(image.read()))
                vacation.image_file = os.path.basename(path)
            else:
                vacation.image_file = 'default.jpg'
            
            vacation.save()
            messages.success(request, 'Vacation added successfully!')
            return redirect('vacation_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = VacationForm()
    
    return render(request, 'vacations/add_vacation.html', {'form': form})


@login_required
def edit_vacation_view(request, vacation_id):
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('vacation_list')
    
    vacation = get_object_or_404(Vacation, id=vacation_id)
    
    if request.method == 'POST':
        form = VacationForm(request.POST, request.FILES, instance=vacation)
        if form.is_valid():
            vacation = form.save(commit=False)
            
            # Handle image upload
            if 'image' in request.FILES:
                image = request.FILES['image']
                filename = f"vacation_images/{image.name}"
                path = default_storage.save(filename, ContentFile(image.read()))
                vacation.image_file = os.path.basename(path)
            
            vacation.save()
            messages.success(request, 'Vacation updated successfully!')
            return redirect('vacation_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = VacationForm(instance=vacation)
    
    context = {
        'form': form,
        'vacation': vacation
    }
    return render(request, 'vacations/edit_vacation.html', context)


@login_required
@require_POST
def delete_vacation_view(request, vacation_id):
    if not request.user.is_admin:
        return JsonResponse({'success': False, 'error': 'Permission denied'})
    
    vacation = get_object_or_404(Vacation, id=vacation_id)
    vacation.delete()
    
    return JsonResponse({'success': True})


@login_required
@require_POST
def toggle_like_view(request, vacation_id):
    if request.user.is_admin:
        return JsonResponse({'success': False, 'error': 'Admins cannot like vacations'})
    
    vacation = get_object_or_404(Vacation, id=vacation_id)
    like, created = Like.objects.get_or_create(
        user=request.user,
        vacation=vacation
    )
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({
        'success': True,
        'liked': liked,
        'like_count': vacation.like_count
    })
