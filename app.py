import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, render_template, request
from pymongo import MongoClient
from bson import ObjectId
from werkzeug.utils import secure_filename

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

app=Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    fruit = list(db.fruit.find({}))
    return render_template('dashboard.html', fruit=fruit)

@app.route('/fruit', methods=['GET'])
def fruit():
    fruit = list(db.fruit.find({}))
    return render_template('fruit.html', fruit=fruit)

@app.route('/addFruit', methods=['GET', 'POST'])
def addFruit():
    if request.method=='POST':
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        nama_gambar = request.files['gambar']

        if nama_gambar:
            nama_file_asli = nama_gambar.filename
            nama_file_gambar = nama_file_asli.split('/')[-1]
            file_path = f'static/assets/imgFruit/{nama_file_gambar}'
            nama_gambar.save(file_path)

        else:
            nama_file_gambar = None

        doc = {
            'nama': nama,
            'harga': harga,
            'gambar': nama_file_gambar,
            'deskripsi': deskripsi
        }
        db.fruit.insert_one(doc)
        return redirect(url_for("fruit"))
    return render_template('AddFruit.html')

@app.route('/editFruit/<_id>',methods=['GET', 'POST'])
def editFruit(_id):
    if request.method=='POST':
        id = request.form['_id']
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        nama_gambar = request.files['gambar']

        doc = {
            'nama': nama,
            'harga': harga,
            'deskripsi': deskripsi
        }
        if nama_gambar:
            nama_file_asli = nama_gambar.filename
            nama_file_gambar = nama_file_asli.split('/')[-1]
            file_path = f'static/assets/imgFruit/{nama_file_gambar}'
            nama_gambar.save(file_path)
            doc['gambar']= nama_file_gambar

        db.fruit.update_one({"_id": ObjectId(_id)}, {"$set": doc})
        return redirect(url_for("fruit"))
    
    id = ObjectId(_id)
    data = list(db.fruit.find({"_id": id}))
    print(data)
    return render_template('EditFruit.html', data=data)

@app.route('/deleteFruit/<_id>', methods=['GET', 'POST'])
def deleteFruit(_id):
    id = ObjectId(_id)
    db.fruit.delete_one({"_id": id}) 
    return redirect(url_for("fruit"))

if __name__ =='__main__':
    #debug is SET to TRUE, CHANGE FOR PROD
    app.run(port=5000, debug=True)


