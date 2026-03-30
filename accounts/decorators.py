from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Check if user is authenticated and has the correct role
            if not request.user.is_authenticated or request.user.role not in allowed_roles:
                # Optional: Add a message so the user knows why they were redirected
                messages.error(request, "You do not have permission to access this page. Please login with an authorized account.")
                
                # Redirect to the login page
                return redirect('login') 

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator