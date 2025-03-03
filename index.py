from flask import Flask, request, jsonify, render_template
import mysql.connector
from db_setup import create_db, create_tb
from connectdb import connDB
from checkStat import set_status,get_status,set_fingerprint_id,get_fingerprint_id

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
