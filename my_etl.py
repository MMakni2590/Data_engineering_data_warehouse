import configparser
import psycopg2
from my_sql_queries import copy_table_queries, insert_table_queries

#Fetching the values from the dwh.cfg file
config = configparser.ConfigParser()
config.read('dwh.cfg')

ENDPOINT= config.get("CLUSTER","HOST")
DB_USER= config.get("CLUSTER","DB_USER")
DB_PASSWORD= config.get("CLUSTER","DB_PASSWORD")
DB_PORT= config.get("CLUSTER","DB_PORT")
DB_NAME= config.get("CLUSTER","DB_NAME")

#Function to load the staging tables
def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()

#Function to insert the tables
def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


#Main function to load and insert the tables
def main():
    #Connecting to the database
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    #Creating a connection object
    conn = psycopg2.connect(
        host=ENDPOINT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    #Creating a cursor object using the connection object
    cur = conn.cursor()
    
    #Calling the load_staging_tables and insert_tables functions
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    #Closing the connection
    conn.close()

#Calling the main function
if __name__ == "__main__":
    main()