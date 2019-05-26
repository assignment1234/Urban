from urban.models import StoreManager
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
django.setup()

from.models import StoreManager
from django.core.exceptions import PermissionDenied


def check_login_store(func):
    def inner1(request):
        store_manager =  StoreManager.objects.filter(user=request.user)
        if store_manager.count()==0:
            raise PermissionDenied
        else:
            return func(request)

    return inner1