from graphene import Schema, ObjectType, String, Field, Int, List, Mutation
from starlette_graphene3 import GraphQLApp, make_graphiql_handler, make_playground_handler
from fastapi import FastAPI

employers_data = [
    {"id": 1, "name": "MetaTechA", "contact_email": "contact@company-a.com", "industry": "Tech"},
    {"id": 2, "name": "MoneySoftB", "contact_email": "contact@company-b.com", "industry": "Finance"},
]

jobs_data = [
    {"id": 1, "title": "Software Engineer", "description": "Develop web applications", "employer_id": 1},
    {"id": 2, "title": "Data Analyst", "description": "Analyze data and create reports", "employer_id": 1},
    {"id": 3, "title": "Accountant", "description": "Manage financial records", "employer_id": 2},
    {"id": 4, "title": "Manager", "description": "Manage people who manage records", "employer_id": 2},
]

class EmployerObject(ObjectType):
    id = Int()
    name =  String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)

    @staticmethod
    def resolve_jobs(root, info):
        return [job for job in jobs_data if job["employer_id"] == root["id"]]

class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)

    @staticmethod
    def resolve_employer(root, info):
        return next((employer for employer in employers_data if employer["id"] == root["employer_id"]))

class Query(ObjectType):
    employers = List(EmployerObject)
    jobs = List(JobObject)

    @staticmethod
    def resolve_employers(root, info):
        return employers_data

    @staticmethod
    def resolve_jobs(root, info):
        return jobs_data
    
class Mutation(ObjectType):
    pass

schema = Schema(query=Query)
app = FastAPI()
app.mount("/graphql", GraphQLApp(
    schema=schema,
    on_get=make_graphiql_handler()
))

app.mount("/graphqlp", GraphQLApp(
    schema=schema,
    on_get=make_playground_handler()
))