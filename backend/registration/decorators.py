import json
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

from backend.application.models import Application


def check_application_permission_by_slug(perm='admin'):
    def decorator(func):
        def wrapper(root, info, *args, **kwargs):
            if info.context.user.is_superuser:
                return func(root, info, args, kwargs)

            try:
                if perm == 'member':
                    assert info.context.user.member_application.filter(
                        slug=kwargs['application__slug'])
                else:
                    assert info.context.user.admin_application.filter(
                        slug=kwargs['application__slug'])

            except AssertionError:
                raise PermissionDenied(
                    "You dont have permission to access to this resource.")

            return func(root, info, args, kwargs)

        return wrapper
    return decorator
