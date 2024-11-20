import io
from flask import Flask, request
from sqlite3 import connect
from PIL import Image

app = Flask(__name__)
dbPath = 'ejercicio1/Imagenes.db'
connection = connect(dbPath)
db = connection.cursor()
db.execute("drop table if exists T_Img")
db.execute(
    '''
    CREATE TABLE T_Img(
           id INTEGER PRIMARY KEY AUTOINCREMENT, 
           name TEXT,
           original BLOB,
           red BLOB, 
           green BLOB, 
           blue BLOB, 
           grayscale BLOB)
    '''
)

@app.route("/")
def hello_world():
    return "<p>Hellooo!</p>"

@app.route("/img/upload", methods=['POST'])
def uploadIMG():
    if 'file' not in request.files:
        return 'Archivo no subido', 400
    
    file = request.files['img']
    image = Image.open(file.read()).convert('RGB')

    r,g,b = image.split()
    grayscale = image.convert('L')

    imgBytes = [
        file.filename,
        image.tobytes(),
        r.tobytes(),
        g.tobytes(),
        b.tobytes(),
        grayscale.tobytes()
    ]

    connection = connect(dbPath)
    db = connection.cursor()
    db.execute(
        '''
        INSERT INTO T_Img (name, original, red, green, blue, grayscale)
        VALUES (?, ?, ?, ?, ?, ?)
        ''',
        imgBytes
    )
    connection.commit()
    connection.close()

    return 'Imagen subida', 200