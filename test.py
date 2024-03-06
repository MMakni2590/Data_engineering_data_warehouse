

import configparser
import psycopg2
from my_sql_queries import analytical_queries

config = configparser.ConfigParser()
config.read('dwh.cfg')

ENDPOINT= config.get("CLUSTER","HOST")
DB_USER= config.get("CLUSTER","DB_USER")
DB_PASSWORD= config.get("CLUSTER","DB_PASSWORD")
DB_PORT= config.get("CLUSTER","DB_PORT")
DB_NAME= config.get("CLUSTER","DB_NAME")

analytical_questions = ["what is the top 5 most played song? ","When is the top 5 highest usage time of day by hour for songs?"]
def analytics(cur, conn):
    for i, query in enumerate(analytical_queries):
        cur.execute(query)
        rows = cur.fetchall()
        print(f"Query {i+1}: {analytical_questions[i]}")
        for row in rows:
            print(row)
        

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
    
    analytics(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()

