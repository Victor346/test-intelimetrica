import psycopg2
from psycopg2 import pool
import os

# This class is used to create a database connection pool and provide with connections to other modules
connection_url = os.environ['DATABASE_URL']

try:
    # For the time being the maximum amount of connection in the pool will be set to 5 but it can be augmented
    # as required
    postgres_pool = psycopg2.pool.SimpleConnectionPool(1, 5, connection_url)
    if postgres_pool:
        print("Connection pool created successfully")

except (Exception, psycopg2.DatabaseError) as error:
    print("Error while connecting to PostgreSQL", error)


def get_db_connection():
    print("Connection lended")
    return postgres_pool.getconn()


def release_db_connection(connection):
    postgres_pool.putconn(connection)
    print("Connection released")
