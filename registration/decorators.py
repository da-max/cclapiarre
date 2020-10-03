from django.core.exceptions import PermissionDenied


def login_required(func):
    def wrapper(root, info, *args):
        if info.context.user.is_anonymous:
            raise PermissionDenied('We must be logged to access this data.')
        return func(root, info, *args)
    return wrapper
