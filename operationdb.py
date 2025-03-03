import mysql.connector
from connectdb import connDB

def add_user_to_db(fingerid, name, gender, number, hostel, department, room):
    
    conn = connDB()
    cursor = conn.cursor()
    
    try:
        sql = """
        INSERT INTO users (fingerid, name, gender, number, hostel, department, room) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (fingerid, name, gender, number, hostel, department, room))
        conn.commit()
        return True, "User Added Successfully"
    except mysql.connector.Error as err:
        return False, f"Error : {err}"
    finally:
        cursor.close()
        conn.close()

def remove_user_from_db(f_id):
    conn = connDB()
    cursor = conn.cursor()

    try:
        sql = "DELETE FROM users WHERE fingerid = %s"
        cursor.execute(sql, (f_id,))
        conn.commit()

        if cursor.rowcount > 0:
            return True, "User Deleted Successfully"
        else:
            return False, "Error: No matching user found"
    
    except mysql.connector.Error as err:
        return False, f"Error: {err}"

    finally:
        cursor.close()
        conn.close()