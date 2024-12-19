from graphene import ObjectType, List
from app.gql.types import EmployerObject, JobObject
from app.db.data import employers_data, jobs_data
from app.db.database import Session
from app.db.modeles import Employer, Job
from sqlalchemy.orm import joinedload


class Query(ObjectType):
    employers = List(EmployerObject)
    jobs = List(JobObject)

    @staticmethod
    def resolve_employers(root, info):
        return Session().query(Employer).all()
        return Session().query(Job).options(joinedload(Job.employer)).all()
    

    @staticmethod
    def resolve_jobs(root, info):
        return Session().query(Job).all()