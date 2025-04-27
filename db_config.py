# db_config.py
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="gk789.mysql", #PUT YOUR PASSWORD HERE
        database="flight_tracking")
