from typing import Dict, Any, List
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Count
import json
from .models import VacationUser, Vacation, Like


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request: HttpRequest) -> JsonResponse:
    """
    Authenticate admin users for statistics dashboard access.
    
    Args:
        request: HTTP request containing email and password in JSON body
        
    Returns:
        JsonResponse: Success/failure status with authentication result
    """
    """Login endpoint for admin users only"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        # Check if user exists in vacation database and is admin
        try:
            vacation_user = VacationUser.objects.get(email=email)
            # Check if user is admin through role
            is_admin = vacation_user.is_admin
            
            if is_admin:
                # For simplicity, accept hardcoded admin credentials
                if email == 'admin@vacation.com' and password == 'admin123':
                    request.session['authenticated'] = True
                    request.session['user_email'] = email
                    return JsonResponse({'success': True, 'message': 'Login successful'})
        except VacationUser.DoesNotExist:
            pass
            
        return JsonResponse({'success': False, 'message': 'Invalid credentials or not admin'}, status=401)
            
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request: HttpRequest) -> JsonResponse:
    """
    Logout current authenticated user by clearing session data.
    
    Args:
        request: HTTP request object
        
    Returns:
        JsonResponse: Success confirmation message
    """
    """Logout endpoint"""
    request.session.flush()
    return JsonResponse({'success': True, 'message': 'Logout successful'})


def vacation_stats(request: HttpRequest) -> JsonResponse:
    """
    Get vacation statistics categorized by past, ongoing, and future dates.
    
    Args:
        request: HTTP request object (must be authenticated)
        
    Returns:
        JsonResponse: Object containing pastVacations, ongoingVacations, futureVacations counts
    """
    """Get vacation statistics - past, ongoing, future"""
    if not request.session.get('authenticated'):
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    today = timezone.now().date()
    
    past_vacations = Vacation.objects.filter(end_date__lt=today).count()
    ongoing_vacations = Vacation.objects.filter(
        start_date__lte=today, 
        end_date__gte=today
    ).count()
    future_vacations = Vacation.objects.filter(start_date__gt=today).count()
    
    return JsonResponse({
        'pastVacations': past_vacations,
        'ongoingVacations': ongoing_vacations,
        'futureVacations': future_vacations
    })


def total_users(request: HttpRequest) -> JsonResponse:
    """
    Get total number of registered users in the system.
    
    Args:
        request: HTTP request object (must be authenticated)
        
    Returns:
        JsonResponse: Object containing totalUsers count
    """
    """Get total number of users in the system"""
    if not request.session.get('authenticated'):
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    total = VacationUser.objects.count()
    return JsonResponse({'totalUsers': total})


def total_likes(request: HttpRequest) -> JsonResponse:
    """
    Get total number of likes across all vacation packages.
    
    Args:
        request: HTTP request object (must be authenticated)
        
    Returns:
        JsonResponse: Object containing totalLikes count
    """
    """Get total number of likes in the system"""
    if not request.session.get('authenticated'):
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    total = Like.objects.count()
    return JsonResponse({'totalLikes': total})


def likes_distribution(request: HttpRequest) -> JsonResponse:
    """
    Get distribution of likes by vacation destination country.
    
    Args:
        request: HTTP request object (must be authenticated)
        
    Returns:
        JsonResponse: Array of objects with destination and likes count
    """
    """Get likes distribution by vacation destination"""
    if not request.session.get('authenticated'):
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    distribution = (Vacation.objects
                   .annotate(likes_count=Count('likes'))
                   .values('country__country_name', 'likes_count')
                   .order_by('-likes_count'))
    
    result = [
        {
            'destination': item['country__country_name'],
            'likes': item['likes_count']
        }
        for item in distribution
    ]
    
    return JsonResponse(result, safe=False)
