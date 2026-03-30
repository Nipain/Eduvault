from django.shortcuts import redirect
from django_tenants.utils import get_tenant


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # ✅ Allow these paths without login
        allowed_paths = [
            "/login/",
            "/logout/",
            "/admin/",   # ✅ IMPORTANT
        ]

        # Allow admin sub-paths also
        if any(path.startswith(p) for p in allowed_paths):
            return self.get_response(request)

        # If not logged in → redirect
        if not request.user.is_authenticated:
            return redirect("/login/")

        return self.get_response(request)