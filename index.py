from flask import Flask, request, jsonify, render_template
import mysql.connector
from db_setup import create_db, create_tb, drop_db
from connectdb import connDB
from checkStat import set_status, get_status, set_fingerprint_id, get_fingerprint_id, set_confirm_id, get_confirm_id
from operationdb import add_user_to_db, remove_user_from_db, add_admin_to_db, remove_admin_from_db
from checkStat import set_del_id,get_del_id, get_confDel_id, add_user_or_not, get_stored_id
from operationdb import get_user_name, get_last_log, update_entry_log, insert_exit_log
from operationdb import get_admin_name, get_admin_last_log, insert_entry_log, update_exit_log

app = Flask(__name__, template_folder="HTML")

# Database
create_db()
create_tb()

# Database connection
conn = connDB()

global delstat
@app.route('/')
def home():
    set_status(0)
    return render_template('home.html')

# Dashboard
@app.route('/Dashboard')
def dashboard():
    set_status(0)
    return render_template('index.html')

# AddorDelpage
@app.route('/addordel')
def addordel():
    set_status(1)
    return render_template('addordel.html')

@app.route('/login')
def login():
    set_status(2)
    return render_template('login.html')

@app.route('/register')
def register():
    set_status(3)
    return render_template('register.html')

@app.route('/esp32/fingerprint', methods=['POST'])
def handle_fingerprint():
    finger_id = request.form.get('FingerID')
    if not finger_id:
        return "Invalid Request", 400
    
    try:
        finger_id = int(finger_id)
    except ValueError:
        return "Invalid Finger ID", 400
    
    user_name = get_user_name(finger_id)
    if not user_name:
        return "unknown", 404

    admin_name = get_admin_name(finger_id)
    if not user_name:
        return "unknown", 404
    
    last_log = get_last_log(finger_id)
    if last_log and last_log["out_time"] and not last_log["in_time"]:
        update_entry_log(last_log["log_id"])
        action = "entry"
    else:
        insert_exit_log(finger_id, user_name)
        action = "exit"
    
    last_admin_log = get_admin_last_log(finger_id)
    if last_admin_log and last_admin_log["in_time"] and not last_admin_log["out_time"]:
        update_exit_log(last_admin_log["log_id"])
        action = "entry"
    else:
        insert_entry_log(finger_id, admin_name)
        action = "exit"
    
    return f"{action} {user_name}"

# Status Check Add Page or Home Page
@app.route('/esp32', methods=['POST'])
def check_add_or_del():
    data = request.get_data(as_text=True).strip()  

    print(f"Received Raw Data from ESP32: '{data}'")  

    if data == 'Check_ADD_OR_DEL':
        response = f"status{get_status()}"  
        print(f"Sending Response: {response}")
    else:
        response = "status0"
        print(f"Unexpected Data! Sending Default: {response}")

    return response

# To Add Fingerprint
# take response from adordel.html
@app.route('/set_user', methods=['POST'])
def set_fingerid():
    """Receive fingerprint ID from the web form."""
    fingerid = request.form.get('fingerid')  # Get Fingerprint ID
    buttres = request.form.get('fingerid_add')  # Get Button Response
    print(fingerid)
    print(buttres)
    if not fingerid or not fingerid.isdigit():
        return render_template('addordel.html', message="Error: Invalid or missing Fingerprint ID")

    set_fingerprint_id(int(fingerid))  # Store the fingerprint ID
    return render_template('addordel.html', message="Fingerprint ID Stored Successfully")

@app.route('/set_admin_login', methods=['POST'])
def set_fingerid_Admin():
    """Receive fingerprint ID from the web form."""
    fingerid = request.form.get('fingerid')  # Get Fingerprint ID
    buttres = request.form.get('fingerid_add')  # Get Button Response
    print(fingerid)
    print(buttres)
    if not fingerid or not fingerid.isdigit():
        return render_template('login.html', message="Error: Invalid or missing Fingerprint ID")

    set_fingerprint_id(int(fingerid))  # Store the fingerprint ID
    return render_template('HOME.html', message="Fingerprint ID Stored Successfully")

@app.route('/set_admin', methods=['POST'])
def set_admin_fingerid():
    """Receive fingerprint ID from the web form."""
    fingerid = request.form.get('fingerid')  # Get Fingerprint ID
    buttres = request.form.get('fingerid_add')  # Get Button Response
    print(fingerid)
    print(buttres)
    if not fingerid or not fingerid.isdigit():
        return render_template('register.html', message="Error: Invalid or missing Fingerprint ID")

    set_fingerprint_id(int(fingerid))  # Store the fingerprint ID
    return render_template('register.html', message="Fingerprint ID Stored Successfully")

# For ESP32
@app.route('/esp32/get_fingerid', methods=['POST'])
def get_fingerid():
    data = request.get_data(as_text=True).strip()

    print(f"Received Raw Data from ESP32: '{data}'")  

    if data == "Get_Fingerid=get_id":
        response = get_fingerprint_id()
        print(f"Sending Response: {response}")
        return response
    else:
        return "Invalid Data",400
    
@app.route('/esp32/get_confirm_id', methods=['POST'])
def get_confirm_id_from_esp32():
    data = request.form.get("confirm_id")  # Extract confirm_id from POST data

    print(f"Received Confirm ID Request from ESP32: '{data}'")  

    if data:  # If confirm_id is received
        confirm_id = get_stored_id()  # Fetch stored confirm ID
        response = str(confirm_id)  # Convert to string for ESP32
        set_confirm_id(confirm_id)
        print(f"Sending Response: {response}")
        return response
    else:
        return "Invalid Data", 400
    

     
    
@app.route('/confirm_add', methods=['POST'])
def confirm_add():
    action = request.form.get('action')  # Get action (add, update, remove)
    
    print(f"Action: {action}")

    # User details
    name = request.form.get('name')
    print(name)
    gender = request.form.get('gender')
    print(gender)
    number = request.form.get('number')
    print(number)
    hostel = request.form.get('Hostel')
    print(hostel)
    department = request.form.get('Department')
    print(department)
    room = request.form.get('Room')
    print(room)


    finger_id = get_confirm_id()  # Retrieve the stored ID
    print("Fingerprint ID:",finger_id)
    if add_user_or_not() == True:
        if action == "add":
            # Ensure all fields are filled before adding a user
            if not all([name, gender, number, hostel, department, room]):
                return render_template('addordel.html', message="Error: Missing required fields")

            success, msg = add_user_to_db(finger_id, name, gender, number, hostel, department, room)
            return render_template('addordel.html', message=msg)

        elif action == "remove":
            global delstat
            delstat = True
            # Remove logic (modify this function in `operationdb.py`)
            success, msg = remove_user_from_db(finger_id)
            return render_template('addordel.html', message=msg)
    """elif action == "update":
        # Update logic (modify this function in `operationdb.py`)
        success, msg = update_user_in_db(finger_id, name, gender, number, hostel, department, room)
        return render_template('addordel.html', message=msg)"""

            

    return render_template('addordel.html', message="Error: Invalid Action")

    
@app.route('/confirm_add_admin', methods=['POST'])
def confirm_admin_add():
    action = request.form.get('action')  # Get action (add, remove)
    
    print(f"Action received: '{action}'")  # Debugging

    # User details
    name = request.form.get('name')
    print(f"Name: {name}")
    number = request.form.get('number')
    print(f"Number: {number}")

    finger_id = get_confirm_id()  # Retrieve stored ID
    print(f"Fingerprint ID: {finger_id}")

    if add_user_or_not():
        if action == "add":
            if not all([name, number]):
                return render_template('register.html', message="Error: Missing required fields")

            success, msg = add_admin_to_db(finger_id, name, number)
            return render_template('register.html', message=msg)

        elif action == "remove":
            global delstat
            delstat = True
            success, msg = remove_admin_from_db(finger_id)
            return render_template('register.html', message=msg)

    print("Invalid Action or add_user_or_not() returned False")
    return render_template('register.html', message="Error: Invalid Action")

    """elif action == "update":
        # Update logic (modify this function in `operationdb.py`)
        success, msg = update_user_in_db(finger_id, name, gender, number, hostel, department, room)
        return render_template('addordel.html', message=msg)"""

            

    return render_template('register.html', message="Error: Invalid Action")

@app.route('/esp32/delfinger', methods=['POST'])
def get_delete_id_from_esp32():
    global delstat  
    data = request.get_data(as_text=True).strip()
    print(f"Received Raw Data from ESP32: '{data}'")  

    if data == "DeleteID=check":
        if delstat == True:
            delID = get_stored_id()
            set_del_id(delID)
            response = get_del_id()
            print(f"Sending Response: {response}")
            delstat = False  
            return response  # ✅ Always return a response

    return "Invalid or Unhandled Request", 400  # ✅ Always return something


# Ensure `delstat` is initialized globally before this function is called
delstat = False



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
