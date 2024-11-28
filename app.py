from flask import Flask, render_template, url_for, request, jsonify
from pymysql import MySQLError, connect
import os

app = Flask(__name__)


# Connect Db
def connect_db():
    return connect(
        host="localhost", # or 127.0.0.1
        port=3307,
        database="flask_crud_image",
        ssl={"disable": True} 
    )

def upload_file(sourcefile):
    upload_dir = "static/uploads"   
    sourcefile.save(os.path.join(upload_dir, sourcefile.filename)) 


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/add-product', methods=["GET", "POST"])
def addProduct():
    if request.method == "POST":
        name = request.form['name']
        source_file = request.files['thumbnail']
        upload_file(sourcefile=source_file)
        
        return jsonify({"name": name})


if __name__ == '__main__':
    app.run(debug=True)