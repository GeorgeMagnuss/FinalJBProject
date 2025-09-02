import logging
from django.http import HttpResponse


class SuppressWellKnownMiddleware:
    """
    Middleware to suppress Chrome DevTools .well-known requests
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Suppress Chrome DevTools requests silently
        if request.path.startswith('/.well-known/'):
            return HttpResponse(status=404)
        
        response = self.get_response(request)
        return response