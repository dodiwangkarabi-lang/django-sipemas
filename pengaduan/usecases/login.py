
# models
from django.contrib.auth.models import User

# login
from django.contrib.auth import (
    login, authenticate, logout
)

class Logout:
    def __init__(self):
        pass
    
    def execute(self, request):
        logout(request)


class Login:
    def __init__(self):
        pass
    
    def execute(self, **kwargs):
        """
        Kwargs:
            request (request): django request
            username (str): _description_
            password (str): _description_
            
        Returns:
            Object | None \n
                kalau berhasil login maka return user \n
                kalau gagal login maka return None
        """
        username = kwargs['username']
        password = kwargs['password']
        
        user = authenticate(
            kwargs['request'],
            username=username, password=password
        )
        
        if user is not None:
            login(kwargs['request'], user)
            return user
        
        return None
            
        
        
        