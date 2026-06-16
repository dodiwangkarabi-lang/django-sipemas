# login services
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout

def login_user(request, username, password):
    user = authenticate(
        request=request, username=username, password=password
    )
    if not user:
        return None
    
    login(request, user)
    
    return user

def logout_user(request):
    logout(request)
