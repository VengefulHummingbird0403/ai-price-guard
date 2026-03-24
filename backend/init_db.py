import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

# Connect to default 'postgres' db to create 'price_guard'
try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="password", # Default local dev fallback
        host="localhost",
        port="5432"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'price_guard'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute("CREATE DATABASE price_guard")
        print("Database price_guard created.")
    else:
        print("Database price_guard already exists.")
    cursor.close()
    conn.close()
except psycopg2.OperationalError as e:
    # If connection fails due to auth, let's try password="postgres"
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres", 
            host="localhost",
            port="5432"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'price_guard'")
        exists = cursor.fetchone()
        if not exists:
             cursor.execute("CREATE DATABASE price_guard")
             print("Database price_guard created.")
        else:
             print("Database price_guard already exists.")
        cursor.close()
        conn.close()
    except Exception as e2:
        print(f"Error connecting to Postgres. Is it running locally? ({e2})")
except Exception as e:
    print(f"Error: {e}")
