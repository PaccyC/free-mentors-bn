import graphene
from users.schema import UserQuery, UserMutation
from mentorship_sessions.schema import SessionQuery, SessionMutation


class Query(UserQuery, SessionQuery, graphene.ObjectType):
    pass


class Mutation(UserMutation, SessionMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
