import io
from flask import Flask, request, jsonify
from sqlite3 import connect
from PIL import Image

app = Flask(__name__)

dbPathImg = 'ejercicio1/Imagenes.db'
dbPathData = 'ejercicio2/contaminacion.db'

# DB - Images
connectionImg = connect(dbPathImg)
dbImg = connectionImg.cursor()
# dbImg.execute("DROP TABLE IF EXISTS T_Img")
dbImg.execute(
    '''
    CREATE TABLE IF NOT EXISTS T_Img(
           id INTEGER PRIMARY KEY AUTOINCREMENT, 
           name TEXT,
           original BLOB,
           red BLOB, 
           green BLOB, 
           blue BLOB, 
           grayscale BLOB)
    '''
)

connectionImg.commit()
connectionImg.close()

# DB - Contaminación Data
connectionData = connect(dbPathData)
dbData = connectionData.cursor()
# dbData.execute("DROP TABLE IF EXISTS T_Conta")
dbData.execute(
    '''
    CREATE TABLE IF NOT EXISTS T_Conta(
           id INTEGER PRIMARY KEY AUTOINCREMENT, 
           nodo TEXT,
           d01 INTEGER,
           d25 INTEGER,
           d10 INTEGER)
    '''
)
connectionData.commit()
connectionData.close()


@app.route("/")
def hello_world():
    return "<p>Holaa</p>"


@app.route("/img/upload", methods=['POST'])
def uploadIMG():
    if 'img' not in request.files:
        return jsonify({'message': 'Archivo no subido', 'status': 400})

    file = request.files['img']
    # archivo binario temporal que tiene los datos de la img, necesario para que pillow pueda "abrir" el archivo de la imagen
    fByte = io.BytesIO(file.read())
    image = Image.open(fByte).convert('RGB')

    r, g, b = image.split()
    grayscale = image.convert('L')

    def toBytes(images):
        result = []
        for img in images:
            buffer = io.BytesIO()  # crea un archivo binario en ram
            img.save(buffer, format='png')  # guarda img en buffer binario
            # extraemos el contenido del buffer
            result.append(buffer.getvalue())
        return result

    original, red, green, blue, grayscale = toBytes(
        [image, r, g, b, grayscale])

    imgBytes = [
        file.filename,
        original,
        red,
        green,
        blue,
        grayscale
    ]
    try:
        connection = connect(dbPathImg)
        db = connection.cursor()
        db.execute(
            '''
         INSERT INTO T_Img (name, original, red, green, blue, grayscale)
          VALUES (?, ?, ?, ?, ?, ?)
          ''',
            imgBytes
        )
        connection.commit()
    except Exception as e:
        print(e)
        return jsonify({'message': "Error al guardar imagen en db", 'status': 500})
    finally:
        connection.close()

    return jsonify({'message': 'Imagen subida', 'status': 200})


@app.route("/contaminacion/upload", methods=['POST'])
def uploadData():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Datos no recibidos', 'status': 400})

    try:
        connection = connect(dbPathData)
        db = connection.cursor()

        for nodo, valores in data.items():
            for registro in valores:
                db.execute(
                    '''
                    INSERT INTO T_Conta (nodo, d01, d25, d10)
                    VALUES (?, ?, ?, ?)
                    ''',
                    (nodo, registro['d01'], registro['d25'], registro['d10'])
                )
        connection.commit()
    except Exception as e:
        print(e)
        return jsonify({'message': "Error al guardar datos en db", 'status': 500})
    finally:
        connection.close()
    return jsonify({'message': 'Datos subidos correctamente', 'status': 200})
