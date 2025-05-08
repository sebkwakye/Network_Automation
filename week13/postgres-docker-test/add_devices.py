import psycopg2
import sys

# def add_network_devices():
#     """Add some sample network devices to the database."""
#     conn = None
#     try:
#         # Connect to the PostgreSQL server
#         conn = psycopg2.connect(
#             host="localhost",
#             database="networkdata",
#             user="netadmin",
#             password="mysecretpassword",
#             port="5432"
#         )
#
#         # Create a cursor
#         cur = conn.cursor()
#
#         # List of sample network devices
#         devices = [
#             ('router1', '192.168.1.1', 'router'),
#             ('switch1', '192.168.1.2', 'switch'),
#             ('firewall1', '192.168.1.3', 'firewall')
#         ]
#
#         # Insert each device into the network_devices table
#         for device in devices:
#             cur.execute(
#                 "INSERT INTO network_devices (hostname, ip_address, device_type) VALUES (%s, %s, %s)",
#                 device
#             )
#
#         # Commit the changes so they are saved in the database
#         conn.commit()
#         print(f"Added {len(devices)} devices to the database")
#
#         # Retrieve and display all devices from the table
#         cur.execute("SELECT * FROM network_devices")
#         rows = cur.fetchall()
#
#         print("\nNetwork Devices:")
#         for row in rows:
#             print(f"ID: {row[0]}, Hostname: {row[1]}, IP: {row[2]}, Type: {row[3]}")
#
#         # Close the cursor
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(f"Error: {error}")
#     finally:
#         if conn is not None:
#             conn.close()
#
#
# if __name__ == '__main__':
#     add_network_devices()


# Database connection details
DB_CONFIG = {
    "host": "localhost",
    "database": "networkdata",
    "user": "netadmin",
    "password": "mysecretpassword",
    "port": "5432"
}

def get_connection():
    """Establish and return a new database connection."""
    return psycopg2.connect(**DB_CONFIG)

def create_table():
    """Create the network_devices table if it doesn't exist."""
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS network_devices (
                id SERIAL PRIMARY KEY,
                hostname VARCHAR(100) NOT NULL,
                ip_address VARCHAR(15) NOT NULL,
                device_type VARCHAR(20)
            )
        ''')
        conn.commit()
        print("Table 'network_devices' created or verified successfully.")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error creating table: {error}")
    finally:
        if conn:
            conn.close()

def add_network_devices():
    """Add some sample network devices to the database."""
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        devices = [
            ('router1', '192.168.1.1', 'router'),
            ('switch1', '192.168.1.2', 'switch'),
            ('firewall1', '192.168.1.3', 'firewall')
        ]
        for device in devices:
            cur.execute(
                "INSERT INTO network_devices (hostname, ip_address, device_type) VALUES (%s, %s, %s)",
                device
            )
        conn.commit()
        print(f"Added {len(devices)} devices to the database.")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error adding devices: {error}")
    finally:
        if conn:
            conn.close()

def show_all_devices():
    """Display all network devices from the database."""
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM network_devices")
        rows = cur.fetchall()
        if rows:
            print("\nNetwork Devices:")
            for row in rows:
                print(f"ID: {row[0]}, Hostname: {row[1]}, IP: {row[2]}, Type: {row[3]}")
        else:
            print("No devices found.")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error retrieving devices: {error}")
    finally:
        if conn:
            conn.close()

def search_device_by_hostname():
    """Search for a network device by hostname."""
    hostname = input("Enter the hostname to search for: ").strip()
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM network_devices WHERE hostname = %s", (hostname,))
        device = cur.fetchone()
        if device:
            print(f"Device Found: ID: {device[0]}, Hostname: {device[1]}, IP: {device[2]}, Type: {device[3]}")
        else:
            print("Device not found.")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error searching device: {error}")
    finally:
        if conn:
            conn.close()

def update_device_info():
    """Update a device's information given its hostname."""
    hostname = input("Enter the hostname of the device to update: ").strip()
    new_ip = input("Enter the new IP address: ").strip()
    new_type = input("Enter the new device type: ").strip()
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE network_devices SET ip_address = %s, device_type = %s WHERE hostname = %s",
            (new_ip, new_type, hostname)
        )
        if cur.rowcount == 0:
            print("No device found with that hostname.")
        else:
            conn.commit()
            print("Device information updated successfully.")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error updating device: {error}")
    finally:
        if conn:
            conn.close()

def delete_device():
    """Delete a device from the database based on its hostname."""
    hostname = input("Enter the hostname of the device to delete: ").strip()
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM network_devices WHERE hostname = %s", (hostname,))
        if cur.rowcount == 0:
            print("No device found with that hostname.")
        else:
            conn.commit()
            print("Device deleted successfully.")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error deleting device: {error}")
    finally:
        if conn:
            conn.close()

def main_menu():
    """Display a simple menu to perform database operations."""
    create_table()  # Ensure the table is created

    while True:
        print("\n--- Network Device Manager ---")
        print("1. Add sample network devices")
        print("2. Show all devices")
        print("3. Search device by hostname")
        print("4. Update device information")
        print("5. Delete device")
        print("6. Exit")
        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            add_network_devices()
        elif choice == "2":
            show_all_devices()
        elif choice == "3":
            search_device_by_hostname()
        elif choice == "4":
            update_device_info()
        elif choice == "5":
            delete_device()
        elif choice == "6":
            print("Exiting the Network Device Manager. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    main_menu()