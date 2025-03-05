import mysql.connector
from connectdb import connDB
from datetime import datetime

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

def add_admin_to_db(fingerid, name, number):
    
    conn = connDB()
    cursor = conn.cursor()
    
    try:
        sql = """
        INSERT INTO admin_finger (fingerid, name, number) 
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (fingerid, name, number))
        conn.commit()
        return True, "Admin Added Successfully"
    except mysql.connector.Error as err:
        return False, f"Error : {err}"
    finally:
        cursor.close()
        conn.close()


def remove_admin_from_db(f_id):
    conn = connDB()
    cursor = conn.cursor()

    try:
        sql = "DELETE FROM admin_finger WHERE fingerid = %s"
        cursor.execute(sql, (f_id,))
        conn.commit()

        if cursor.rowcount > 0:
            return True, "Admin Deleted Successfully"
        else:
            return False, "Error: No matching Admin found"
    
    except mysql.connector.Error as err:
        return False, f"Error: {err}"

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

# Fetch user name by Finger ID
def get_user_name(finger_id):
    conn = connDB()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name FROM users WHERE fingerid = %s", (finger_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user['name'] if user else None

# Fetch last log entry
def get_last_log(finger_id):
    conn = connDB()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT log_id, in_time, out_time FROM entry_exit_log WHERE fingerid = %s ORDER BY log_id DESC LIMIT 1",
        (finger_id,)
    )
    last_log = cursor.fetchone()
    cursor.close()
    conn.close()
    return last_log

def insert_exit_log(finger_id, user_name):
    conn = connDB()
    cursor = conn.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
        "INSERT INTO entry_exit_log (fingerid, out_time, user_name) VALUES (%s, %s, %s)",
        (finger_id, current_time, user_name)
    )
    conn.commit()
    cursor.close()

# Update entry log
def update_entry_log(log_id):
    conn = connDB()
    cursor = conn.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("UPDATE entry_exit_log SET in_time = %s WHERE log_id = %s", (current_time, log_id))
    conn.commit()
    cursor.close()
    conn.close()