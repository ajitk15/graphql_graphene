## Getting Started

Follow these steps to set up your environment and run the app.

## Prerequisites

Make sure you have Python 3.8+ installed on your system.

## Installation

#### Create a virtual environment:

python -m venv env

#### Activate the virtual environment:

On Windows:

.\env\Scripts\activate

On macOS/Linux:

source env/bin/activate

## Install dependencies:

- pip install graphene==3.2.2
- pip install fastapi==0.95.1
- pip install starlette-graphene3==0.6.0
- pip install uvicorn==0.21.1
- pip install SQLAlchemy==2.0.11
- pip install psycopg==3.1.8

#### Save dependencies to a requirements file:

pip freeze > requirements.txt

## Running the Application

Start the application using Uvicorn:

uvicorn main:app --reload

## Open your browser and navigate to:

GraphQL Playground: http://127.0.0.1:8000/graphql

## Project Structure

The typical structure of this project:

graphql_graphene/
- ├── main.py         # Entry point of the application
- ├── models.py       # SQLAlchemy models
- ├── schema.py       # GraphQL schema using Graphene
- ├── resolvers.py    # Query/Mutation resolvers
- └── requirements.txt

## Additional Information

Graphene Documentation: https://docs.graphene-python.org/

FastAPI Documentation: https://fastapi.tiangolo.com/

SQLAlchemy Documentation: https://docs.sqlalchemy.org/

Feel free to clone, modify, and expand this project for your needs. Contributions are welcome!

