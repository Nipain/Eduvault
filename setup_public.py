import os
import django
from django.contrib.auth import get_user_model

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tenants.models import School, Domain

def setup_everything():
    User = get_user_model()
    
    try:
        # 1. Create the Public Tenant
        tenant, created = School.objects.get_or_create(
            schema_name='public', 
            defaults={'name': 'EduVault Main Site'}
        )
        if created:
            print("✅ Successfully created 'public' tenant.")
        else:
            print("ℹ️ 'public' tenant already exists.")

        # 2. Add your Render URL
        live_domain = 'eduvault-l2mi.onrender.com'
        domain, d_created = Domain.objects.get_or_create(
            domain=live_domain, 
            tenant=tenant, 
            defaults={'is_primary': True}
        )
        
        if d_created:
            print(f"✅ Successfully linked {live_domain} to public schema.")
        else:
            print(f"ℹ️ Domain {live_domain} is already linked.")

        # 3. Create Global Superuser (Public Schema)
        # Change these to your preferred credentials
        admin_email = "admin@eduvault.app"
        admin_password = "Whitetiger@47" 

        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                username=admin_email,
                email=admin_email,
                password=admin_password
            )
            print(f"✅ Superuser created: {admin_email}")
        else:
            print(f"ℹ️ Superuser {admin_email} already exists.")

    except Exception as e:
        print(f"❌ Error during setup: {e}")

if __name__ == "__main__":
    setup_everything()