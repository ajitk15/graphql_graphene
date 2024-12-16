from graphene import Schema, ObjectType, String, Field, Int, List, Mutation

users_data = [
        {"id": 1, "name":"John", "age":34},
        {"id": 2, "name":"Kumar", "age":24},
        {"id": 3, "name":"Mohan", "age":44}
]

class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()

class CreateUser(Mutation):
    class Arguments:
        name = String()
        age = Int()
    
    user = Field(UserType)

    def mutate(self, info, name, age):
        user = {"id": len(users_data) + 1, "name": name, "age": age}
        users_data.append(user)
        return CreateUser(user=user)

class UpdateUser(Mutation):
    class Arguments:
        user_id = Int(required=True)
        name = String()
        age = Int()

    user = Field(UserType)

    def mutate(self, info, user_id, name=None, age=None):
        user = None
        for u in users_data:
            if u["id"] == user_id:
                user = u
                break

        if not user:
            return None
        
        if name is not None:
            user["name"] = name

        if age is not None:
            user["age"] = age

        return UpdateUser(user=user)

class DeleteUser(Mutation):
    class Arguments:
        user_id = Int(required=True)

    user = Field(UserType)

    def mutate(self, info, user_id):
        user = None
        for idx, u in enumerate(users_data):
            if u["id"] == user_id:
                user = u
                del users_data[idx]

        if not user:
            return None
        
        return DeleteUser(user=user)

class Query(ObjectType):
    users = List(UserType)
    user = Field(UserType, user_id=Int())
    users_by_min_age = List(UserType, min_age=Int())

    def resolve_users(self, info):
        return users_data
        
    def resolve_user(self, info, user_id):
        matched_user = [user for user in users_data if user["id"] == user_id]
        return matched_user[0] if matched_user else None
    
    def resolve_users_by_min_age(self, info, min_age):
        return [user for user in users_data if user["age"] >=  min_age]

    
class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

schema = Schema(query=Query, mutation=Mutation)



query_users = '''
query {
  users {
    id
    name
    age
  }
}
'''

create_user = '''
mutation {
 createUser(name: "Ajit", age: 33){
 user{
  name
  age
 }
 }
}
'''

update_user = '''
mutation {
 updateUser(userId: 4, name: "Ajit kumar", age: 33){
 user{
  id
  name
  age
 }
 }
}
'''

delete_user = '''
mutation{
 deleteUser(userId: 4){
  user{
  id
  name
  age
  }
 }
}
'''


if __name__ == "__main__":
    result = schema.execute(query_users)
    print(result)
    print("\n================================")
    result = schema.execute(create_user)
    print(result)
    print("\n================================")
    result = schema.execute(query_users)
    print(result)
    print("\n================================")
    result = schema.execute(update_user)
    print(result)
    print("\n================================")
    result = schema.execute(query_users)
    print(result)
    print("\n================================")
    result = schema.execute(delete_user)
    print(result)
    print("\n================================")
    result = schema.execute(query_users)
    print(result)
    print("\n================================")