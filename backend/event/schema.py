import graphene
from graphene_django import DjangoObjectType

from backend.event.models import Event


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = ('date', 'title', 'descritpion')


class Query(graphene.ObjectType):
    """ Query for event app. They are only one query : all_events
    because only this is use by web site.
    """
    all_events = graphene.List(EventType)

    def resolve_all_events(self, info):
        return Event.objects.all()
