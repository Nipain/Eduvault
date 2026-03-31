from django.shortcuts import redirect
from django_tenants.utils import get_tenant

# class LoginRequiredMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         path = request.path

#         # ✅ Allow these paths + any path starting with /static/
#         allowed_paths = [
#             "/",
#             "/login/",
#             "/logout/",
#             "/signup/",
#             "/pricing/",
#             "/admin/",
#             "/login-redirect/",
#         ]

#         # Check if the path is in our list OR is a static file request
#         if path in allowed_paths or path.startswith("/static/") or any(path.startswith(p) for p in allowed_paths if p != "/"):
#             return self.get_response(request)

#         if not request.user.is_authenticated:
#             return redirect("/login/")

#         return self.get_response(request)

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        tenant = get_tenant(request) # <--- ADD THIS: Identify the school
        print(f"DEBUG: Tenant is {tenant.schema_name}, Path is {path}")

        # ✅ Allow these paths for everyone
        allowed_paths = [
            "/login/",
            "/logout/",
            "/signup/",
            "/pricing/",
            "/admin/",
        ]

        # 1. Always allow Static Files
        if path.startswith("/static/"):
            return self.get_response(request)

        # 2. Allow the Homepage ONLY on the Public site
        if path == "/" and tenant.schema_name == 'public':
            return self.get_response(request)

        # 3. Check if current path is allowed
        if any(path.startswith(p) for p in allowed_paths):
            return self.get_response(request)

        # 4. If not logged in, redirect to the login page of the CURRENT school
        if not request.user.is_authenticated:
            # This will keep the user on school1.localhost:8000/login/
            return redirect("/login/") 

        return self.get_response(request)