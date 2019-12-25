import psycopg2
from flaskr.dbconfig import config

def connect():
    # Connect to the PostgreSQL database server
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()
        # display the PostgreSQL database server version
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print("Successfully connected to the DB: " + db_version[0])

        return conn

     # close the communication with the PostgreSQL
        #cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
