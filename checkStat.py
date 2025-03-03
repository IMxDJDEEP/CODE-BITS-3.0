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

def set_fingerprint_id(f_id):
    global fingerprint_id
    fingerprint_id = f_id
    print(f"Fingerprint id stored {fingerprint_id}")

def get_fingerprint_id():
    global fingerprint_id
    if fingerprint_id:
        response = f"add-id{fingerprint_id}"
        fingerprint_id = None
    else:
        response = "error"

    return response



