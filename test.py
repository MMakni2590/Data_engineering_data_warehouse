import configparser
import psycopg2
from my_sql_queries import analytical_queries

#Fetching the values from the dwh.cfg file
config = configparser.ConfigParser()
config.read('dwh.cfg')

ENDPOINT= config.get("CLUSTER","HOST")
DB_USER= config.get("CLUSTER","DB_USER")
DB_PASSWORD= config.get("CLUSTER","DB_PASSWORD")
DB_PORT= config.get("CLUSTER","DB_PORT")
DB_NAME= config.get("CLUSTER","DB_NAME")

#Function to run the analytical queries
analytical_questions = ["what is the top 5 most played songs? ","When is the top 5 highest usage times of day by hour for songs?"]
def analytics(cur, conn):
    for i, query in enumerate(analytical_queries):
        #Executing the query
        cur.execute(query)
        #Fetching the results
        rows = cur.fetchall()
        #Printing the results
        print(f"Query {i+1}: {analytical_questions[i]}")
        for row in rows:
            print(row)
        

def main():
    #Connecting to the database
    config = configparser.ConfigParser()
    #Reading the dwh.cfg file
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
    #Calling the analytics function
    analytics(cur, conn)
    #Closing the connection
    conn.close()

#Calling the main function
if __name__ == "__main__":
    main()

