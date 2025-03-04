import mysql.connector

def create_db():

    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Hacktivate",
        database = "Hostel"
    )

    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS Hostel")
    conn.commit()
    print("DATABASE Hostel Is Created")

    cursor.close()
    conn.close()

def create_tb():
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Hacktivate",
        database = "Hostel"
    )

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
            fingerid INT PRIMARY KEY,
            name VARCHAR(255),
            gender VARCHAR(10),
            number VARCHAR(20),
            hostel VARCHAR(50),
            department VARCHAR(50),
            room VARCHAR(20)
           );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entry_exit_log (
        log_id INT AUTO_INCREMENT PRIMARY KEY,
        fingerid INT,
        purpose VARCHAR(255),
        out_time DATETIME,
        in_time DATETIME,
        FOREIGN KEY (fingerid) REFERENCES users(fingerid) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_finger (
        log_id INT AUTO_INCREMENT PRIMARY KEY,
        fingerid INT,
        name VARCHAR(255),
        number VARCHAR(20)
        )
    """)

    conn.commit()
    print("Tables created successfully.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_db()
    create_tb()