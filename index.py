from flask import Flask, request, jsonify, render_template
import mysql.connector
from db_setup import create_db, create_tb
from connectdb import connDB
import os

#template_dir = r"C:\Users\prath\Codebits 3.0\CODE-BITS-3.0\HTML"
app = Flask(__name__ ,template_folder = "HTML")


create_db()
create_tb()

# Database connection
conn = connDB()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/addordel')
def addordel():
    return render_template('addordel.html')

if __name__ == '__main__':
    app.run(debug=True)
