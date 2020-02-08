from django.core.exceptions import ObjectDoesNotExist
from registration.models import PageAccess



class CheckAccess:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        
        try:
            page = PageAccess.objects.get(url=request.build_absolute_uri())

        except ObjectDoesNotExist:
            pass
        
        else:
            request.is_access = bool(page.access)
        
        response = self.get_response(request)
        return response  