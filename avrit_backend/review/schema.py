from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import graphene
from graphene_permissions.mixins import AuthNode, AuthMutation
from graphene_permissions.permissions import AllowStaff, AllowAny
from review.models import Post
import graphql_jwt

class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        filter_fields = {
            'title': ['exact', 'icontains'],
            'type_of_submission': ['exact', 'icontains'],
            'course_name': ['exact', 'icontains'],
            'subject': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
        }
        interfaces = (relay.Node,)

class QueryPost(ObjectType):
    post = relay.Node.Field(PostNode)
    all_post = DjangoFilterConnectionField(PostNode)

class MutationJWT(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()