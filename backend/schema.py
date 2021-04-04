import graphql_jwt
from graphene import ObjectType, Schema

from backend.application.schema import Query as application_query, Mutation as application_mutation
from backend.article.schema import Query as article_query, Mutation as article_mutation
from backend.carousel.schema import Query as carousel_query, Mutation as carousel_mutation
from backend.citrus.schema import Query as citrus_query, Mutation as citrus_mutation
from backend.coffee.schema import Query as coffee_query, Mutation as coffee_mutation
from backend.event.schema import Query as event_query
from backend.registration.schema import Query as registration_query, Mutation as registration_mutation


class Query(application_query, article_query, carousel_query, citrus_query, coffee_query, event_query,
            registration_query, ObjectType):
    pass


class Mutation(application_mutation, article_mutation, carousel_mutation, citrus_mutation, coffee_mutation, registration_mutation, ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = Schema(query=Query, mutation=Mutation)
