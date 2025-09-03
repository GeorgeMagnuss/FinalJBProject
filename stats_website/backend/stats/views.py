from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Count
import json
from .models import User, Vacation, Like


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    """Login endpoint for admin users only"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user and user.is_admin:
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Login successful'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid credentials or not admin'}, status=401)
            
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    """Logout endpoint"""
    logout(request)
    return JsonResponse({'success': True, 'message': 'Logout successful'})


def vacation_stats(request):
    """Get vacation statistics - past, ongoing, future"""
    if not request.user.is_authenticated or not request.user.is_admin:
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


def total_users(request):
    """Get total number of users in the system"""
    if not request.user.is_authenticated or not request.user.is_admin:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    total = User.objects.count()
    return JsonResponse({'totalUsers': total})


def total_likes(request):
    """Get total number of likes in the system"""
    if not request.user.is_authenticated or not request.user.is_admin:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    total = Like.objects.count()
    return JsonResponse({'totalLikes': total})


def likes_distribution(request):
    """Get likes distribution by vacation destination"""
    if not request.user.is_authenticated or not request.user.is_admin:
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
