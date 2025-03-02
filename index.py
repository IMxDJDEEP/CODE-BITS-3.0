from flask import Flask, request, jsonify, render_template
import mysql.connector
from db_setup import create_db, create_tb
from connectdb import connDB
from checkStat import set_status,get_status

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

@app.route('/esp32', methods=['POST'])
def check_add_or_del():
    data = request.get_data(as_text=True).strip()  # Read raw data and strip spaces

    print(f"Received Raw Data from ESP32: '{data}'")  # Debug log

    if data == 'Check_ADD_OR_DEL':
        response = f"status{get_status()}"  # Get latest status
        print(f"Sending Response: {response}")
        set_status(0)  # Reset status after sending
    else:
        response = "status0"
        print(f"Unexpected Data! Sending Default: {response}")

    return response




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
