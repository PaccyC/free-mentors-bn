import graphene
from graphene_django import DjangoObjectType
from .models import MentorshipSession, Review
from users.models import User
from free_mentors_bn.utils.auth import get_user_from_info


class SessionType(DjangoObjectType):
    class Meta:
        model = MentorshipSession
        fields = ('id', 'mentee', 'mentor', 'questions', 'status', 'scheduled_at', 'created_at')


class ReviewType(DjangoObjectType):
    class Meta:
        model = Review
        fields = ('id', 'mentee', 'mentor', 'score', 'comment', 'is_hidden', 'created_at')


class CreateSession(graphene.Mutation):
    class Arguments:
        mentor_id = graphene.ID(required=True)
        questions = graphene.String(required=True)
        scheduled_at = graphene.DateTime(required=True)

    Output = SessionType

    def mutate(self, info, mentor_id, questions, scheduled_at):
        user = get_user_from_info(info)
        if not user:
            raise Exception("Not authenticated")
        try:
            mentor = User.objects.get(id=int(mentor_id), role='MENTOR')
        except (User.DoesNotExist, ValueError):
            raise Exception("Mentor not found")
        return MentorshipSession.objects.create(
            mentee=user,
            mentor=mentor,
            questions=questions,
            scheduled_at=scheduled_at,
        )


class AcceptSession(graphene.Mutation):
    class Arguments:
        session_id = graphene.ID(required=True)

    Output = SessionType

    def mutate(self, info, session_id):
        user = get_user_from_info(info)
        if not user or user.role != 'MENTOR':
            raise Exception("Mentor access required")
        try:
            session = MentorshipSession.objects.get(id=int(session_id), mentor=user)
        except (MentorshipSession.DoesNotExist, ValueError):
            raise Exception("Session not found")
        if session.status != 'PENDING':
            raise Exception("Session is not pending")
        session.status = 'ACCEPTED'
        session.save()
        return session


class DeclineSession(graphene.Mutation):
    class Arguments:
        session_id = graphene.ID(required=True)

    Output = SessionType

    def mutate(self, info, session_id):
        user = get_user_from_info(info)
        if not user or user.role != 'MENTOR':
            raise Exception("Mentor access required")
        try:
            session = MentorshipSession.objects.get(id=int(session_id), mentor=user)
        except (MentorshipSession.DoesNotExist, ValueError):
            raise Exception("Session not found")
        if session.status != 'PENDING':
            raise Exception("Session is not pending")
        session.status = 'DECLINED'
        session.save()
        return session


class ReviewMentor(graphene.Mutation):
    class Arguments:
        mentor_id = graphene.ID(required=True)
        score = graphene.Int(required=True)
        comment = graphene.String(required=True)

    Output = ReviewType

    def mutate(self, info, mentor_id, score, comment):
        user = get_user_from_info(info)
        if not user:
            raise Exception("Not authenticated")
        try:
            mentor = User.objects.get(id=int(mentor_id), role='MENTOR')
        except (User.DoesNotExist, ValueError):
            raise Exception("Mentor not found")
        if not (1 <= score <= 5):
            raise Exception("Score must be between 1 and 5")
        return Review.objects.create(mentee=user, mentor=mentor, score=score, comment=comment)


class HideReview(graphene.Mutation):
    class Arguments:
        review_id = graphene.ID(required=True)

    Output = ReviewType

    def mutate(self, info, review_id):
        user = get_user_from_info(info)
        if not user or user.role != 'ADMIN':
            raise Exception("Admin access required")
        try:
            review = Review.objects.get(id=int(review_id))
        except (Review.DoesNotExist, ValueError):
            raise Exception("Review not found")
        review.is_hidden = True
        review.save()
        return review


class SessionMutation(graphene.ObjectType):
    create_session = CreateSession.Field()
    accept_session = AcceptSession.Field()
    decline_session = DeclineSession.Field()
    review_mentor = ReviewMentor.Field()
    hide_review = HideReview.Field()


class SessionQuery(graphene.ObjectType):
    my_sessions = graphene.List(SessionType)
    mentor_sessions = graphene.List(SessionType)
    mentor_reviews = graphene.List(ReviewType, mentor_id=graphene.ID(required=True))
    all_reviews = graphene.List(ReviewType)

    def resolve_my_sessions(self, info):
        user = get_user_from_info(info)
        if not user:
            raise Exception("Not authenticated")
        return MentorshipSession.objects.filter(mentee=user)

    def resolve_mentor_sessions(self, info):
        user = get_user_from_info(info)
        if not user or user.role != 'MENTOR':
            raise Exception("Mentor access required")
        return MentorshipSession.objects.filter(mentor=user)

    def resolve_mentor_reviews(self, info, mentor_id):
        try:
            # Djongo BooleanField filter is buggy — filter is_hidden in Python
            reviews = Review.objects.filter(mentor_id=int(mentor_id))
            return [r for r in reviews if not r.is_hidden]
        except (ValueError, Exception):
            return []

    def resolve_all_reviews(self, info):
        user = get_user_from_info(info)
        if not user or user.role != 'ADMIN':
            raise Exception("Admin access required")
        return Review.objects.all()
