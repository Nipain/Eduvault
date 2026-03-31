from django.shortcuts import render, redirect
from tenants.models import School, Domain
from accounts.models import User
from billing.models import Subscription, Plan
from .forms import SchoolSignupForm

from django_tenants.utils import schema_context
from datetime import timedelta
from django.utils import timezone
from django.db import transaction


def signup(request):

    if request.method == "POST":
        form = SchoolSignupForm(request.POST)

        if form.is_valid():

            raw_host = request.get_host()
            clean_host = raw_host.split(':')[0]
            school_name = form.cleaned_data["school_name"]
            subdomain = form.cleaned_data["subdomain"].lower().replace(" ", "")
            email = form.cleaned_data["admin_email"]
            password = form.cleaned_data["password"]
            plan = form.cleaned_data["plan"]

            # ✅ Check duplicate BEFORE proceeding
            if School.objects.filter(schema_name=subdomain).exists():
                form.add_error("subdomain", "Subdomain already taken")
                return render(request, "public/signup.html", {"form": form})

            try:
                # ✅ TRANSACTION START
                with transaction.atomic():

                    # 1️⃣ Create tenant
                    tenant = School(
                        schema_name=subdomain,
                        name=school_name
                    )
                    tenant.save()

                    # 2️⃣ Create domain
                    domain = Domain(
                        domain=f"{subdomain}.{clean_host}",
                        tenant=tenant,
                        is_primary=True
                    )
                    domain.save()

                    # 3️⃣ Switch to tenant schema
                    with schema_context(subdomain):

                        User.objects.create_user(
                            username=email,
                            email=email,
                            password=password,
                            role="admin",
                            is_staff=True
                        )


                    # 4️⃣ Create subscription (public schema)
                    Subscription.objects.create(
                        school=tenant,
                        plan=plan,
                        end_date=timezone.now() + timedelta(days=plan.duration_days)
                    )

                # This combines your new school name with the current website address
                return redirect(f"{request.scheme}://{subdomain}.{raw_host}/login/")

            except Exception as e:
                form.add_error(None, f"Something went wrong: {str(e)}")

    else:
        form = SchoolSignupForm()

    return render(request, "public/signup.html", {"form": form})


def login_redirect(request):

    subdomain = request.GET.get("subdomain")

    if subdomain:
        subdomain = subdomain.lower().replace(" ", "")
        return redirect(f"http://{subdomain}.localhost:8000/login/")

    return redirect("/")


def home(request):

    return render(request,"public/home.html")


def pricing(request):

    plans = Plan.objects.all()

    return render(request,"public/pricing.html",{"plans":plans})