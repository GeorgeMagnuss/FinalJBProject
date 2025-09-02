from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()


class EmailBackend(ModelBackend):
    """Custom authentication backend using email instead of username - matches vacation website"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(f"🔍 EmailBackend.authenticate() called")
        print(f"   username: {username}")
        print(f"   password: {'*' * len(password) if password else None}")
        print(f"   kwargs: {kwargs}")
        
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
            print(f"   username from kwargs: {username}")
            
        if username is None or password is None:
            print("❌ Username or password is None, returning None")
            return None
        
        try:
            print(f"🔍 Looking for user with email: {username}")
            user = User.objects.get(email=username)
            print(f"✅ Found user: {user.email}")
            print(f"   User details: {user.first_name} {user.last_name}")
            print(f"   Is active: {user.is_active}")
            print(f"   Is staff: {user.is_staff}")
            print(f"   Is admin: {user.is_admin}")
            
            password_check = user.check_password(password)
            print(f"🔑 Password check result: {password_check}")
            
            can_authenticate = self.user_can_authenticate(user)
            print(f"🔐 user_can_authenticate result: {can_authenticate}")
            
            if password_check and can_authenticate:
                print("✅ Authentication successful, returning user")
                return user
            else:
                print("❌ Authentication failed - password or user_can_authenticate check failed")
                return None
                
        except User.DoesNotExist:
            print(f"❌ User with email {username} does not exist")
            # Run default password hasher to mitigate timing attacks
            User().set_password(password)
            return None
        except Exception as e:
            print(f"❌ Exception during authentication: {e}")
            return None
            
        print("❌ Reached end of method without returning user")
        return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user if self.user_can_authenticate(user) else None
        except User.DoesNotExist:
            return None