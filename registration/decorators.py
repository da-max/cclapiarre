import json
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

from application.models import Application


def login_required(func):
    def wrapper(root, info, *args, **kwargs):
        if info.context.user.is_anonymous:
            raise PermissionDenied('We must be logged to access this data.')
        return func(root, info, *args, **kwargs)
    return wrapper


# Thanks to
# https://medium.com/@anish.shrestha/relay-graphene-django-and-permissions-b1b2b96daf20 for exemple.
def permissions_required(perm):
    def decorator(func):
        def wrapper(root, info, **kwargs):
            user = info.context.user
            if isinstance(perm, str):
                perms = (perm, )
            else:
                perms = perm

            if user.has_perms(perms):
                return func(root, info, **kwargs)

            raise PermissionDenied("Permission Denied")

        return wrapper
    return decorator


def application_permissions_required(group_type="admins"):
    """ 
    Params : perm table or string
    Description : This decorator is used to check if the user has 
    permission under the form Admin/Member <application_name>.
    """
    def decorator(func):
        def wrapper(root, info, application__name, *args, **kwargs):
            user = info.context.user
            try:
                app = Application.objects.get(name=application__name)
            except Application.DoesNotExist:
                raise Application.DoesNotExist("Application not found.")

            if group_type == "members":
                try:
                    assert user.is_superuser or app.admins.get(username=user.username) or app.members.get(
                        username=user.username)
                except AssertionError:
                    raise PermissionDenied("Permission Denied")

            else:
                try:
                    assert user.is_superuser or app.admins.get(
                        username=user.username)

                except AssertionError:
                    raise PermissionDenied("Permission Denied")

            return func(root, info, application__name, *args, **kwargs)

        return wrapper
    return decorator
