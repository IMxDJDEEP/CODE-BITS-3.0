from flask import Flask, request, jsonify, render_template
import mysql.connector
from db_setup import create_db, create_tb
from connectdb import connDB
from checkStat import set_status,get_status,set_fingerprint_id,get_fingerprint_id,set_confirm_id,get_confirm_id,add_user_or_not,get_stored_id
from operationdb import add_user_to_db

app = Flask(__name__, template_folder="HTML")

# Database
create_db()
create_tb()

# Database connection
conn = connDB()

# Mainpage
@app.route('/')
def index():
    set_status(0)
    return render_template('index.html')

# AddorDelpage
@app.route('/addordel')
def addordel():
    set_status(1)
    return render_template('addordel.html')

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
    confirm_id = request.form.get('confirm_id')  # Get ID from the form properly
    action = request.form.get('action')  # Get action (add, update, remove)
    
    print(f"Received Confirm ID: {confirm_id}")
    print(f"Action: {action}")

    # User details
    name = request.form.get('name')
    gender = request.form.get('gender')
    number = request.form.get('number')
    hostel = request.form.get('Hostel')
    department = request.form.get('Department')
    room = request.form.get('Room')

    # Validate confirm_id
    if not confirm_id or not confirm_id.isdigit():
        return render_template('addordel.html', message="Error: Invalid Fingerprint ID")

    confirm_id = int(confirm_id)  # Convert to integer
    finger_id = get_confirm_id()  # Retrieve the stored ID
    if add_user_or_not() == True:
        if action == "add":
            # Ensure all fields are filled before adding a user
            if not all([name, gender, number, hostel, department, room]):
                return render_template('addordel.html', message="Error: Missing required fields")

            success, msg = add_user_to_db(finger_id, name, gender, number, hostel, department, room)
            return render_template('addordel.html', message=msg)

    """elif action == "update":
        # Update logic (modify this function in `operationdb.py`)
        success, msg = update_user_in_db(finger_id, name, gender, number, hostel, department, room)
        return render_template('addordel.html', message=msg)

    elif action == "remove":
        # Remove logic (modify this function in `operationdb.py`)
        success, msg = remove_user_from_db(finger_id)
        return render_template('addordel.html', message=msg)"""

    return render_template('addordel.html', message="Error: Invalid Action")





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
