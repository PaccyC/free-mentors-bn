import graphene
from users.schema import UserQuery, Signup, Login, ChangeUserToMentor, CreateAdmin
from mentorship_sessions.schema import (
    SessionQuery, CreateSession, AcceptSession,
    DeclineSession, ReviewMentor, HideReview,
)


class Query(UserQuery, SessionQuery, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    signup = Signup.Field()
    login = Login.Field()
    change_user_to_mentor = ChangeUserToMentor.Field()
    create_admin = CreateAdmin.Field()
    create_session = CreateSession.Field()
    accept_session = AcceptSession.Field()
    decline_session = DeclineSession.Field()
    review_mentor = ReviewMentor.Field()
    hide_review = HideReview.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
