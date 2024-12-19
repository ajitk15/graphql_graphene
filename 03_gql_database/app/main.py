from graphene import Schema
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from fastapi import FastAPI
from app.db.database import prepare_datebase, Session
from app.gql.queries import Query
from app.db.modeles import Employer, Job

# GQL Query
schema = Schema(query=Query)

app = FastAPI()
@app.on_event("startup")
def startup_event():
    prepare_datebase()

@app.get("/employers")
def get_employers():
    session = Session()
    employers = session.query(Employer).all()
    session.close()
    return employers


@app.get("/jobs")
def get_jobs():
    session = Session()
    jobs = session.query(Job).all()
    session.close()
    return jobs

app.mount("/graphql", GraphQLApp(
    schema=schema,
    on_get=make_graphiql_handler()
))

