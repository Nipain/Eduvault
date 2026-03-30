from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .decorators import role_required

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect("/dashboard/")

        else:
            return render(request, "accounts/login.html", {"error": "Invalid credentials"})

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("/login/")

def dashboard(request):

    if not request.user.is_authenticated:
        return redirect("/login/")

    role = request.user.role

    if role == "admin":
        return redirect("/admin-dashboard/")

    elif role == "teacher":
        return redirect("/teacher-dashboard/")

    elif role == "parent":
        return redirect("/parent-dashboard/")

    elif role == "accountant":
        return redirect("/accountant-dashboard/")

    return redirect("/login/")

@role_required(["admin"])
def admin_dashboard(request):
    return render(request, "dashboard/admin.html")

@role_required(["teacher"])
def teacher_dashboard(request):
    return render(request, "dashboard/teacher.html")

@role_required(["parent"])
def parent_dashboard(request):
    return render(request, "dashboard/parent.html")

@role_required(["accountant"])
def accountant_dashboard(request):
    return render(request, "dashboard/accountant.html")