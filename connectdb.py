import mysql.connector

def connDB():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Hacktivate",
        database="Hostel"
    )
    return conn


