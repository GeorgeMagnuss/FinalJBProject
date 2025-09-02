from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
    print(f"🔍 LOGIN VIEW: Received {request.method} request")
    print(f"   Content-Type: {request.content_type}")
    print(f"   Request body: {request.body}")
    
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        print(f"📧 Parsed email: {email}")
        print(f"🔑 Parsed password: {'*' * len(password) if password else None}")
        
        user = authenticate(request, username=email, password=password)
        print(f"🔐 authenticate() returned: {user}")
        
        if user:
            print(f"✅ User found: {user.email}")
            print(f"   Is admin: {user.is_admin}")
            print(f"   Is active: {user.is_active}")
            print(f"   Is staff: {user.is_staff}")
            
            if user.is_admin:
                print("✅ User is admin - logging in")
                login(request, user)
                return JsonResponse({'success': True, 'message': 'Login successful'})
            else:
                print("❌ User is not admin")
                return JsonResponse({'success': False, 'message': 'Not an admin user'}, status=401)
        else:
            print("❌ authenticate() returned None")
            return JsonResponse({'success': False, 'message': 'Invalid credentials or not admin'}, status=401)
            
    except Exception as e:
        print(f"❌ Exception in login_view: {e}")
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    """Logout endpoint"""
    logout(request)
    return JsonResponse({'success': True, 'message': 'Logout successful'})


@login_required
def vacation_stats(request):
    """Get vacation statistics - past, ongoing, future"""
    if not request.user.is_admin:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
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


@login_required
def total_users(request):
    """Get total number of users in the system"""
    if not request.user.is_admin:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    total = User.objects.count()
    return JsonResponse({'totalUsers': total})


@login_required
def total_likes(request):
    """Get total number of likes in the system"""
    if not request.user.is_admin:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    total = Like.objects.count()
    return JsonResponse({'totalLikes': total})


@login_required
def likes_distribution(request):
    """Get likes distribution by vacation destination"""
    if not request.user.is_admin:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
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
