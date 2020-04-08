import json
from django.core.exceptions import ObjectDoesNotExist
from stats.models import PageAccess
from django.utils import timezone
from django.http import Http404


class CheckAccess:
    """ Middleware for check if the page display has not an access as False. """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        try:
            page = PageAccess.objects.get(url=request.build_absolute_uri())

        # url fields has unique attribute at True,so I don’t check if get return one of more values (with except).
        except ObjectDoesNotExist:
            pass

        else:
            if page.start_date > timezone.now():
                request.page_access = True

            elif page.raise_exception:
                raise Http404(page.content)
            else:
                request.page_access = bool(page.access)
                request.page_title = page.title
                request.page_content = page.content
        finally:
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
