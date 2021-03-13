import json
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.http import Http404
from django.db.models import Q

from backend.stats.models import PageAccess


class CheckAccess:
    """ Middleware for check if the page display has not an access as False. """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        try:
            # Get PageAccess object with same url to request, start_date before now, and with False access.
            page = PageAccess.objects.get(Q(url=request.build_absolute_uri()) & Q(start_date__lt=timezone.now()) & Q(access=False))

        # url fields has unique attribute at True,so I don’t check if get return one of more values (with except).
        except ObjectDoesNotExist:
            pass
        else:
            if page.raise_exception:
                raise Http404((page.title, page.content))
            else:
                request.page = dict()
                request.page['access'] = False
                request.page['title'] = page.title
                request.page['content'] = page.content
        
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
