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
del_id = None
global delstat
confirmDel_id = None

def set_fingerprint_id(f_id):
    global fingerprint_id
    global stored_id
    global confirmDel_id
    fingerprint_id = f_id
    stored_id = f_id
    confirmDel_id = f_id
    print(f"Fingerprint id stored {fingerprint_id}")

def set_confirm_id(f_id):
    global confirm_id
    confirm_id = f_id
    print(f"Fingerprint id stored {confirm_id}")


def get_confirm_id():
    global confirm_id
    return confirm_id

def add_user_or_not():
    global stored_id, confirm_id  # Declare both variables as global

    if stored_id is None or confirm_id is None:
        print("Error: stored_id or confirm_id is not set")
        return False  # Return False if values are not initialized

    return stored_id == confirm_id  # Directly return the comparison result

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

def set_del_id(del_id1):
    global del_id
    del_id = del_id1
    print("Delete ID:",del_id)
    
def get_del_id():
    global del_id
    if del_id:
        response = f"del-id{del_id}"
        del_id = None
    else:
        response = "error"

    return response

def get_confDel_id():
    global confirmDel_id
    return confirmDel_id