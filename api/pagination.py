""" This file contains all class for paginate. """
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class StandardLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 30