from django.shortcuts import redirect
from django_tenants.utils import get_tenant

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # ✅ Allow these paths + any path starting with /static/
        allowed_paths = [
            "/",
            "/login/",
            "/logout/",
            "/signup/",
            "/pricing/",
            "/admin/",
            "/login-redirect/",
        ]

        # Check if the path is in our list OR is a static file request
        if path in allowed_paths or path.startswith("/static/") or any(path.startswith(p) for p in allowed_paths if p != "/"):
            return self.get_response(request)

        if not request.user.is_authenticated:
            return redirect("/login/")

        return self.get_response(request)


# class LoginRequiredMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         path = request.path

#         # ✅ Allow these paths without login
#         allowed_paths = [
#             "/login/",
#             "/logout/",
#             "/admin/",   # ✅ IMPORTANT
#         ]

#         # Allow admin sub-paths also
#         if any(path.startswith(p) for p in allowed_paths):
#             return self.get_response(request)

#         # If not logged in → redirect
#         if not request.user.is_authenticated:
#             return redirect("/login/")

#         return self.get_response(request)