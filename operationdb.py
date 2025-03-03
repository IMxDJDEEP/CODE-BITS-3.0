import mysql.connector
from connectdb import connDB

def add_user_to_db(fingerid, name, gender, number, hostel, department, room):
    
    conn = connDB
    cursor = conn.cursor()
    
    try:
        sql = """
        insert into users  (fingerid, name, gender, number, hostel, department, room) values (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (fingerid, name, gender, number, hostel, department, room))
        conn.commit()
        return True,"User Added Successfully"
    except mysql.connector.Error as err:
        return False, f"Error : {err}"
    finally:
        cursor.close()
        conn.close()

