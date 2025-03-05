import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import mysql.connector
import datetime

app = Flask(__name__)

# Twilio Credentials
ACCOUNT_SID = os.environ.get('AC375a69367c7925e3449ad744b735093a')
AUTH_TOKEN = os.environ.get('b5166454c6cd661796ce2c9f8d409838')

# Database Configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Hacktivate"
DB_NAME = "Hostel"

# State management
user_states = {}  # Dictionary to store user states

def connect_db():
    try:
        db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return db
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def fetch_hosteler_info(name):
    db = connect_db()
    if db:
        cursor = db.cursor(dictionary=True)
        query = "SELECT user_name, purpose, out_time, in_time FROM entry_exit_log WHERE user_name = %s"
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        db.close()
        return result
    return None

def fetch_contacts(contact_type):
    db = connect_db()
    if db:
        cursor = db.cursor(dictionary=True)
        query = "SELECT name, contact_number FROM admin_finger WHERE type = %s"
        cursor.execute(query, (contact_type,))
        results = cursor.fetchall()
        db.close()
        return results
    return None

def calculate_remaining_time(out_time_str, in_time_str):
    if out_time_str and in_time_str:
        out_time = datetime.datetime.strptime(out_time_str, '%H:%M:%S').time()
        in_time = datetime.datetime.strptime(in_time_str, '%H:%M:%S').time()
        out_datetime = datetime.datetime.combine(datetime.date.today(), out_time)
        in_datetime = datetime.datetime.combine(datetime.date.today(), in_time)
        duration = in_datetime - out_datetime
        return str(duration)
    elif out_time_str:
        out_time = datetime.datetime.strptime(out_time_str, '%H:%M:%S').time()
        out_datetime = datetime.datetime.combine(datetime.date.today(), out_time)
        now = datetime.datetime.now()
        duration = now - out_datetime
        return str(duration)
    else:
        return "N/A"

def check_outside_duration(name):
    db = connect_db()
    if db:
        cursor = db.cursor(dictionary=True)
        query = "SELECT out_time FROM entry_exit_log WHERE user_name = %s AND in_time IS NULL"
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        db.close()
        if result and result['out_time']:
            out_time = datetime.datetime.strptime(str(result['out_time']), '%H:%M:%S').time()
            out_datetime = datetime.datetime.combine(datetime.date.today(), out_time)
            now = datetime.datetime.now()
            duration = now - out_datetime
            if duration.total_seconds() > 3600:  # 1 hour in seconds
                return True
    return False

@app.route("/sms", methods=['POST'])
def sms_reply():
    from_number = request.form['From']  # Get the user's phone number
    message_body = request.form['Body'].lower()
    resp = MessagingResponse()
    message = resp.message()

    if 'git' in message_body:
        message.body("Welcome to the Hostel Chatbot! Please enter your name.")
        user_states[from_number] = "waiting_for_name"  # Set state
        return str(resp)

    if from_number in user_states and user_states[from_number] == "waiting_for_name":
        hosteler_info = fetch_hosteler_info(message_body.capitalize())
        if hosteler_info:
            out_time = hosteler_info.get('out_time')
            in_time = hosteler_info.get('in_time')
            remaining_time = calculate_remaining_time(str(out_time) if out_time else None, str(in_time) if in_time else None)

            info_message = f"Hosteler Information:\n"
            info_message += f"Name: {hosteler_info['user_name']}\n"
            info_message += f"Purpose: {hosteler_info['purpose']}\n"
            info_message += f"Out Time: {out_time}\n"
            info_message += f"Remaining Time: {remaining_time}\n"
            message.body(info_message)

            if check_outside_duration(message_body.capitalize()):
                message.body(f"Alert: {message_body.capitalize()} has been outside for more than 1 hour.")
        else:
            message.body("Name not found. Please enter your name again.")
        user_states.pop(from_number) #reset state.
        return str(resp)

    if 'help' in message_body:
        warden_contacts = fetch_contacts("warden")
        watchman_contacts = fetch_contacts("watchman")
        contact_message = "Contact Information:\n"
        if warden_contacts:
            contact_message += "\nWarden:\n"
            for warden in warden_contacts:
                contact_message += f"{warden['name']}: {warden['contact_number']}\n"
        if watchman_contacts:
            contact_message += "\nWatchman:\n"
            for watchman in watchman_contacts:
                contact_message += f"{watchman['name']}: {watchman['contact_number']}\n"
        message.body(contact_message)
        return str(resp)

    if 'exit' in message_body:
        message.body("Thank you for using the Hostel Chatbot. Goodbye!")
        return str(resp)

    message.body("Please type 'git' to start, 'help' for contact information, or 'exit' to quit.")
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)