import configparser
import psycopg2
from my_sql_queries import create_table_queries, drop_table_queries

#Fetching the values from the dwh.cfg file
config = configparser.ConfigParser()
config.read('dwh.cfg')

ENDPOINT= config.get("CLUSTER","HOST")
DB_USER= config.get("CLUSTER","DB_USER")
DB_PASSWORD= config.get("CLUSTER","DB_PASSWORD")
DB_PORT= config.get("CLUSTER","DB_PORT")
DB_NAME= config.get("CLUSTER","DB_NAME")

#Function to drop the tables
def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

#Function to create the tables
def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

#Main function to drop and create the tables
def main():
    #Connecting to the database
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect(
        host=ENDPOINT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    #Creating a cursor object using the connection object
    cur = conn.cursor()

    #Calling the drop_tables and create_tables functions
    drop_tables(cur, conn)
    create_tables(cur, conn)

    #Closing the connection
    conn.close()

#Calling the main function
if __name__ == "__main__":
    main()