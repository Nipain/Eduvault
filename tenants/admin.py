from django.contrib import admin
from django.shortcuts import redirect

class TenantAdminSite(admin.AdminSite):
    def has_permission(self, request):
        # 1. Standard permission check
        is_allowed = super().has_permission(request)
        if not is_allowed:
            return False

        # 2. Schema check: If it's the public schema, only global superusers allowed
        if request.tenant.schema_name == 'public':
            return request.user.is_superuser and request.user.school is None

        # 3. Tenant check: User must be assigned to THIS school OR be a global superuser
        return request.user.is_superuser or request.user.school == request.tenant

tenant_admin_site = TenantAdminSite(name='tenant_admin')