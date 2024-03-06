import configparser
import psycopg2
from my_sql_queries import copy_table_queries, insert_table_queries

config = configparser.ConfigParser()
config.read('dwh.cfg')

ENDPOINT= config.get("CLUSTER","HOST")
DB_USER= config.get("CLUSTER","DB_USER")
DB_PASSWORD= config.get("CLUSTER","DB_PASSWORD")
DB_PORT= config.get("CLUSTER","DB_PORT")
DB_NAME= config.get("CLUSTER","DB_NAME")

def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect(
        host=ENDPOINT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()