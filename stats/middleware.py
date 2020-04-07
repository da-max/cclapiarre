import json
from django.core.exceptions import ObjectDoesNotExist
from stats.models import PageAccess



class CheckAccess:
    """ Middleware for check if the page display has not an access as False. """
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



class Version:
    """ Middleware for take number version in frontent/package.json. """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    
    def __call__(self, request):
        
                
        try:
            file = open('frontend/package.json')
            with (file) as package:
                package = json.load(package)
            
            version = package['version']

        except:
            version = '0.0.1'
        
        request.version = version
        
        response = self.get_response(request)
        
        return response