from graphene import ObjectType, Schema

from backend.article.schema import Query as article_query, Mutation as article_mutation
from backend.carousel.schema import Query as carousel_query
from backend.event.schema import Query as event_query
from backend.registration.schema import Query as registration_query, Mutation as registration_mutation
from backend.application.schema import Query as application_query, Mutation as application_mutation


class Query(article_query, carousel_query, event_query,
            registration_query, application_query, ObjectType):
    pass


class Mutation(article_mutation, application_mutation, registration_mutation, ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)
