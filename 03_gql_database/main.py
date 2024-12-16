from graphene import Schema, ObjectType, String, Field, Int, List, Mutation
from starlette_graphene3 import GraphQLApp, make_graphiql_handler, make_playground_handler
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String as saString, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


DB_URL = "postgresql+psycopg://postgres:EbrLoLGrcHXMWmWiGSgygsmpnjmYHEBg@autorack.proxy.rlwy.net:32523/railway"
engine = create_engine(DB_URL)
conn = engine.connect()

Base = declarative_base()

class Employer(Base):
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True)
    name = Column(saString)
    contact_email = Column(saString)
    industry = Column(saString)
    jobs = relationship("Job", back_populates="employer")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(saString)
    description = Column(saString)
    employer_id = Column(Integer, ForeignKey("employers.id"))
    employer = relationship("Employer", back_populates="jobs")

Session = sessionmaker(bind=engine)

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


def prepare_datebase():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session()

    for employer in employers_data:
        emp = Employer(**employer)
        session.add(emp)

    for job in jobs_data:
        session.add(Job(**job))

    session.commit()
    session.close()
    

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
@app.on_event("startup")
def startup_event():
    prepare_datebase()

app.mount("/graphql", GraphQLApp(
    schema=schema,
    on_get=make_graphiql_handler()
))

app.mount("/graphqlp", GraphQLApp(
    schema=schema,
    on_get=make_playground_handler()
))