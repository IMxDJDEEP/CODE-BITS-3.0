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

def drop_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Hacktivate",
        database="Hostel"
    )
    cursor = conn.cursor()

    # Disable foreign key checks to allow dropping dependent tables
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

    # Drop tables in correct order (child tables first, then parent)
    cursor.execute("DROP TABLE IF EXISTS admin_log;")
    cursor.execute("DROP TABLE IF EXISTS admin_finger;")
    cursor.execute("DROP TABLE IF EXISTS entry_exit_log;")
    cursor.execute("DROP TABLE IF EXISTS users;")

    # Enable foreign key checks back
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    conn.commit()
    print("Tables dropped successfully.")
    
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
            user_name varchar(255),
            purpose VARCHAR(255),
            out_time DATETIME,
            in_time DATETIME,
            FOREIGN KEY (fingerid) REFERENCES users(fingerid) ON DELETE CASCADE
            );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_finger (
        fingeridA INT PRIMARY KEY, 
        name VARCHAR(255) NOT NULL,
        number VARCHAR(15) NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_log (
        log_id INT AUTO_INCREMENT PRIMARY KEY,
        fingeridA INT NOT NULL,
        admin_name VARCHAR(255) NOT NULL,
        in_time DATETIME,
        out_time DATETIME,
        FOREIGN KEY (fingeridA) REFERENCES admin_finger(fingeridA) ON DELETE CASCADE
    );
    """)


    conn.commit()
    print("Tables created successfully.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_db()
    create_tb()