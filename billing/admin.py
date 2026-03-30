from django.contrib import admin
from .models import Plan

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):

    def has_module_permission(self, request):
        # ✅ Only show in public schema
        return request.tenant.schema_name == "public"