from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker
from app.db.modeles import Base, Employer, Job
from app.db.data import employers_data, jobs_data
from app.settings.config import DB_URL

engine = create_engine(DB_URL)
conn = engine.connect()
Session = sessionmaker(bind=engine)

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