from graphene import ObjectType, Schema

from article.schema import Query as article_query, Mutation as article_mutation
from carousel.schema import Query as carousel_query
from event.schema import Query as event_query
from registration.schema import Query as registration_query
from application.schema import Query as application_query


class Query(article_query, carousel_query, event_query,
            registration_query, application_query, ObjectType):
    pass


class Mutation(article_mutation, ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)
