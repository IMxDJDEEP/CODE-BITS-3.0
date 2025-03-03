from flask import Flask, request, jsonify, render_template
# Status Check Functions

checkStat = 0  # Default value

def set_status(value):
    global checkStat
    checkStat = value
    print(f"Status updated to: {checkStat}")

def get_status():
    global checkStat
    return checkStat

# ADD ID function

fingerprint_id = None
stored_id = None
confirm_id = None

def set_fingerprint_id(f_id):
    global fingerprint_id
    global stored_id
    fingerprint_id = f_id
    stored_id = f_id
    print(f"Fingerprint id stored {fingerprint_id}")

def set_confirm_id(f_id):
    global confirm_id
    confirm_id = f_id
    print(f"Fingerprint id stored {confirm_id}")


def get_confirm_id():
    global confirm_id
    return confirm_id

def add_user_or_not():
    global stored_id
    global confirm_id
    if stored_id == confirm_id:
        return True
    else:
        return False

def get_fingerprint_id():
    global fingerprint_id
    if fingerprint_id:
        response = f"add-id{fingerprint_id}"
        fingerprint_id = None
    else:
        response = "error"

    return response


def get_stored_id():
    global stored_id
    return stored_id
