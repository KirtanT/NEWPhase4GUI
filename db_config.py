# db_config.py
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
<<<<<<< Updated upstream
        password="", #PUT YOUR PASSWORD HERE
        database="flight_tracking")
=======
        password="gk789.mysql", #PUT YOUR PASSWORD HERE
        database="flight_tracking"

    )
>>>>>>> Stashed changes
