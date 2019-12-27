# Run this script to import the CSV data from prompts.csv into the DB

from flaskr.db import connect
import psycopg2
import csv

def import_prompts():

    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = connect()

        # create a cursor
        cur = conn.cursor()

        #create books table if it doesn't exists
        sql = 'CREATE TABLE IF NOT EXISTS prompts (id SERIAL PRIMARY KEY, summary varchar (2000), category varchar(200), custom boolean, author varchar(200), upvotes int default 0, downvotes int default 0)'
        cur.execute(sql)

        with open ('picoloprompts.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                cur.execute(
                    "INSERT INTO prompts (summary, category, custom, author, upvotes, downvotes) VALUES (%s, %s, %s, %s, %s, %s)",
                    row
                )
                print ("Inserting " + row[0] + " " + row[1] + " into the database")
        conn.commit()
        print ("Prompts imported and commited")
    except Exception as e:
        print ("Could not import the file into the DB")
        print (e)

if __name__ == '__main__':
    import_prompts()
