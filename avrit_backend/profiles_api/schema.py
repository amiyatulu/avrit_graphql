from django.contrib.auth import get_user_model
from graphene import relay, ObjectType
from graphene_django.filter import DjangoFilterConnectionField
import django_filters
import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from profiles_api.models import ProfileImage, ProfileDetails
from graphql_jwt.decorators import login_required
from graphql_relay.node.node import from_global_id
from graphql_jwt.decorators import staff_member_required


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        exclude_fields = ('password')

class ProfileImageType(DjangoObjectType):
    class Meta:
        model = ProfileImage
        filter_fields = ['user__name']
        interfaces = (relay.Node, )

class ProfileDetailsNode(DjangoObjectType):
    class Meta:
        model = ProfileDetails
        filter_fields = ['user__name'] 
        exclude_fields = ('arrange', 'created_at', 'updated_at')
        interfaces = (relay.Node, )

class ProfilePubFilter(django_filters.FilterSet):
    class Meta:
        model = ProfileDetails
        fields = ['user__name'] 
    @property
    def qs(self):
        return super(ProfilePubFilter, self).qs.filter(allow_public_view='Y')




class Query(ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    me = graphene.Field(UserType)
    profile = graphene.Field(ProfileDetailsNode)
    pub_all_profile = DjangoFilterConnectionField(ProfileDetailsNode, filterset_class=ProfilePubFilter)
    pub_profile = graphene.Field(ProfileDetailsNode, id=graphene.ID(required=True))
    @staff_member_required
    def resolve_all_users(self, info, **kwargs):
        usermodel = get_user_model()
        return usermodel.objects.all()
    
    @staff_member_required
    def resolve_user(self, info, id):
        return get_user_model().objects.get(id=id)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user
    def resolve_profile(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return ProfileDetails.objects.get(user=user)
    def resolve_pub_profile(self, info, id):
        profile_id = from_global_id(id)[1]
        profiledetailsobj = ProfileDetails.objects.get(pk=profile_id) 
        if(profiledetailsobj.allow_public_view != 'Y'):
            raise Exception("Viewing Profile Not Allowed")
        return profiledetailsobj
    

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        name = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, name, password, email):
        user = get_user_model()(
            name=name,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class CreateProfileImage(graphene.Mutation):
    profile_image = graphene.Field(ProfileImageType)

    @classmethod
    @login_required
    def mutate(cls, root, info):
        user = info.context.user
        files = info.context.FILES['imageFile']
        imgobj = ProfileImage(user=user, image=files)
        imgobj.save()
        return CreateProfileImage(profile_image=imgobj)

class CreateProfileDetails(relay.ClientIDMutation):
    profile_details = graphene.Field(ProfileDetailsNode)
    class Input:
        address = graphene.String(required=True)
        research_interest = graphene.String(required=True)
        education = graphene.String()
        experience = graphene.String()
        publications = graphene.String()
    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        user = info.context.user
        address = input.get('address')
        research_interest = input.get('research_interest')
        education = input.get('education')
        experience = input.get('experience')
        publications = input.get('publications')    
        profile_details_obj = ProfileDetails(user=user, 
                                            address=address, 
                                            research_interest=research_interest, 
                                            education=education,
                                            experience=experience,
                                            publications=publications,
                                            )
        profile_details_obj.save()
        return CreateProfileDetails(profile_details=profile_details_obj)

class UpdateProfileDetails(relay.ClientIDMutation):
    profile_details = graphene.Field(ProfileDetailsNode)

    class Input:
        profile_id = graphene.ID(required=True)
        address = graphene.String(required=True)
        research_interest = graphene.String(required=True)
        education = graphene.String()
        experience = graphene.String()
        publications = graphene.String()
    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        user = info.context.user
        profile_qid = input.get('profile_id')
        profile_id = from_global_id(profile_qid)[1]
        profile_obj = ProfileDetails.objects.get(user_id=profile_id)
        if profile_obj.user != user:
            raise Exception('Not permitted to update this profile.')
        address = input.get('address')
        research_interest = input.get('research_interest')
        education = input.get('education')
        experience = input.get('experience')
        publications = input.get('publications')
        if address:
            profile_obj.address = address
        if research_interest:
            profile_obj.research_interest = research_interest
        if education:
            profile_obj.education = education
        else:
            profile_obj.education = ""
        if experience:
            profile_obj.experience = experience
        else:
            profile_obj.experience = ""
        if publications:
            profile_obj.publications = publications
        else:
            profile_obj.publications = ""
        profile_obj.save()

        return UpdateProfileDetails(profile_details=profile_obj)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_profile_image = CreateProfileImage.Field()
    create_profile_details = CreateProfileDetails.Field()
    update_profile_details = UpdateProfileDetails.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()