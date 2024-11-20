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
    if 'img' not in request.files:
        return 'Archivo no subido', 400
    
    file = request.files['img']
    fByte = io.BytesIO(file.read()) # archivo binario temporal que tiene los datos de la img, necesario para que pillow pueda "abrir" el archivo de la imagen
    image = Image.open(fByte).convert('RGB')

    r,g,b = image.split()
    grayscale = image.convert('L')

    def toBytes(images): 
        result = []
        for img in images:
            buffer = io.BytesIO() # crea un archivo binario en ram
            img.save(buffer, format='png') # guarda img en buffer binario
            result.append(buffer.getvalue()) # extraemos el contenido del buffer
        return result
    
    original, red, green, blue, grayscale = toBytes([image, r, g, b, grayscale])
    
    imgBytes = [
        file.filename,
        original,
        red,
        green,
        blue,
        grayscale
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