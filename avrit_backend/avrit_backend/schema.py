import graphene
import review.schema
import profiles_api.schema

class Query(profiles_api.schema.Query, review.schema.QueryPost, graphene.ObjectType):
    pass

class Mutation(profiles_api.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
