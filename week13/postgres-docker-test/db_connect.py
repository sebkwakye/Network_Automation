import psycopg2
from psycopg2 import sql


def connect_to_db():
    """Connect to the PostgreSQL database server and create a table."""
    conn = None
    try:
        # Connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host="localhost",
            database="networkdata",
            user="netadmin",
            password="mysecretpassword",
            port="5432"
        )

        # Create a cursor
        cur = conn.cursor()

        # Execute a test query to display PostgreSQL version
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)

        # Create the network_devices table if it does not exist
        cur.execute('''
            CREATE TABLE IF NOT EXISTS network_devices (
                id SERIAL PRIMARY KEY,
                hostname VARCHAR(100) NOT NULL,
                ip_address VARCHAR(15) NOT NULL,
                device_type VARCHAR(20)
            )
        ''')

        # Commit the changes
        conn.commit()
        print("Table created successfully")

        # Close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect_to_db()
