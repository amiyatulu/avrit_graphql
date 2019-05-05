import graphene
import review.schema
import users.schema

class Query(users.schema.Query, review.schema.QueryPost, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation, review.schema.MutationJWT, graphene.ObjectType,):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
