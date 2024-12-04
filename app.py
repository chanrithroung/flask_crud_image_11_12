from flask import Flask, render_template, url_for, request, jsonify, redirect
from pymysql import MySQLError, connect
from datetime import datetime
import os

app = Flask(__name__)


# Connect Db
def connect_db():
    return connect(
        host="localhost", # or 127.0.0.1
        port=3307,
        user="root",
        passwd="",
        database="flask_crud_image",
        ssl={"disable": True} 
    )

def upload_file(sourcefile):
    upload_dir = "static/uploads"
    _, ext = os.path.splitext(sourcefile.filename)
    safe_file_name = 'image' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ext
    sourcefile.save(os.path.join(upload_dir, safe_file_name))

    return safe_file_name



@app.route('/')
def add_product():
    return render_template("add_product.html")


@app.route("/index")
def index():
    con = connect_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM `products` ORDER BY `id` DESC;")
    products = cursor.fetchall()

    # return jsonify(products)

    return render_template('index.html', products=products)


@app.route('/admin-dashboard')
def dashboard():
    return render_template('dashborad.html')


@app.route('/add-product', methods=["GET", "POST"])
def addProduct():
    if request.method == "POST":
        name = request.form['name']
        source_file = request.files['thumbnail']
        price = request.form['price']
        qty = request.form['qty']
        thumbnail = upload_file(sourcefile=source_file)
        description = request.form['description']

        sql = f"""
           INSERT INTO `products`(`name`, `price`, `qty`, `thumbnail`, `description`) 
           VALUES ('{name}','{price}','{qty}','{thumbnail}','{description}')
        """
        # return sql

        con = connect_db()
        cursor = con.cursor()
        cursor.execute(sql)
        con.commit()

        
        return redirect('/')
    

@app.route('/list-products')
def list_product():
    con = connect_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM `products`")
    products = cursor.fetchall()
    return render_template('list-product.html', products=products)





@app.route('/edit/<id>', methods=["GET", "POST"])
def edit_product(id):
    con = connect_db()
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM `products` WHERE `id` = '{id}' ")
    product = cursor.fetchall()

    
    return render_template('edit-product.html', product=product)
    
@app.route("/submit-edit", methods=["GET", "POST"])
def submit_edit():
    if request.method == "POST":
        id          = request.form['id']
        name        = request.form['name']
        price       = request.form['price']
        qty         =  request.form['qty']
        thumbnail   = request.files['thumbnail']
        description = request.form['description']

        if thumbnail:
            thumbnail = upload_file(sourcefile=thumbnail)
        else:
            thumbnail = request.form['old-thumbnail']
        
        sql = f"""
           UPDATE `products` SET `name` = '{name}', `price` = '{price}', `qty` = '{qty}', `thumbnail` = '{thumbnail}', `description` = '{description}' WHERE `id` = '{id}';
        """
        # return sql

        con = connect_db()
        cursor = con.cursor()
        cursor.execute(sql)
        con.commit()

        return redirect('list-products')
if __name__ == '__main__':
    app.run(debug=True)


