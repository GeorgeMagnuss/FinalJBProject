from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()


class EmailBackend(ModelBackend):
    """Custom authentication backend using email instead of username - matches vacation website"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
            
        if username is None or password is None:
            return None
        
        try:
            user = User.objects.get(email=username)
            
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            else:
                return None
                
        except User.DoesNotExist:
            # Run default password hasher to mitigate timing attacks
            User().set_password(password)
            return None
        except Exception:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user if self.user_can_authenticate(user) else None
        except User.DoesNotExist:
            return None