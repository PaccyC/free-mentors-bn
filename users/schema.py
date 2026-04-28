import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from free_mentors_bn.utils.auth import create_token, get_user_from_info


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'bio', 'address', 'occupation', 'expertise', 'role')


class AuthPayload(graphene.ObjectType):
    token = graphene.String()
    user = graphene.Field(UserType)


class Signup(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        bio = graphene.String(default_value='')
        address = graphene.String(default_value='')
        occupation = graphene.String(default_value='')
        expertise = graphene.String(default_value='')

    Output = AuthPayload
    

    def mutate(self, info, first_name, last_name, email, password,
               bio='', address='', occupation='', expertise=''):
        if User.objects.filter(email=email).exists():
            raise Exception("Email already in use")
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password),
            bio=bio,
            address=address,
            occupation=occupation,
            expertise=expertise,
        )
        return AuthPayload(token=create_token(user), user=user)


class Login(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    Output = AuthPayload

    def mutate(self, info, email, password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise Exception("Invalid credentials")
        if not check_password(password, user.password):
            raise Exception("Invalid credentials")
        return AuthPayload(token=create_token(user), user=user)


class ChangeUserToMentor(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)

    Output = UserType

    def mutate(self, info, user_id):
        current_user = get_user_from_info(info)
        if not current_user or current_user.role != 'ADMIN':
            raise Exception("Admin access required")
        try:
            user = User.objects.get(id=int(user_id))
        except (User.DoesNotExist, ValueError):
            raise Exception("User not found")
        user.role = 'MENTOR'
        user.save()
        return user


class CreateAdmin(graphene.Mutation):
    class Arguments:
        admin_creation_key = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        bio = graphene.String(default_value='')
        address = graphene.String(default_value='')
        occupation = graphene.String(default_value='')
        expertise = graphene.String(default_value='')

    Output = UserType

    def mutate(self, info, admin_creation_key, first_name, last_name, email, password,
               bio='', address='', occupation='', expertise=''):
        from django.conf import settings
        expected = settings.ADMIN_CREATION_KEY
        if not expected or admin_creation_key != expected:
            raise Exception("Invalid admin creation key")
        if User.objects.filter(email=email).exists():
            raise Exception("Email already in use")
        return User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password),
            bio=bio,
            address=address,
            occupation=occupation,
            expertise=expertise,
            role='ADMIN',
        )


class UserMutation(graphene.ObjectType):
    signup = Signup.Field()
    login = Login.Field()
    change_user_to_mentor = ChangeUserToMentor.Field()
    create_admin = CreateAdmin.Field()


class UserQuery(graphene.ObjectType):
    mentors = graphene.List(UserType)
    mentor = graphene.Field(UserType, id=graphene.ID(required=True))
    me = graphene.Field(UserType)
    all_users = graphene.List(UserType)

    def resolve_mentors(self, info):
        return User.objects.filter(role='MENTOR')

    def resolve_mentor(self, info, id):
        try:
            return User.objects.get(id=int(id), role='MENTOR')
        except (User.DoesNotExist, ValueError):
            raise Exception("Mentor not found")

    def resolve_me(self, info):
        user = get_user_from_info(info)
        if not user:
            raise Exception("Not authenticated")
        return user

    def resolve_all_users(self, info):
        current_user = get_user_from_info(info)
        if not current_user or current_user.role != 'ADMIN':
            raise Exception("Admin access required")
        return User.objects.all()
