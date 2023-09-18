from django.shortcuts import redirect
from django.urls import reverse
from managment.views import logout_view 


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not request.user.is_authenticated and request.path_info not in [reverse('login'), reverse('register')]:
            return redirect('login')
        return self.get_response(request)
    
    
# AUTO LOGOUT AFTER SESSION EXPIERY

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:
            if request.session.get_expiry_age() <= 0:
                print(request.session.get_expiry_age())
                logout_view(request)  # Log out the user if the session has expired
        response = self.get_response(request)
        return response
