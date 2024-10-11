from PIL import Image
import math

def centroide(imagen):
    roi = Image.open(imagen).convert('L')
    data = roi.load()
    ancho, largo = roi.size

    Mpq10 = 0
    Mpq01 = 0
    Mpq00 = 0

    for i in range(ancho):
        for j in range(largo):
            if data[i, j] == 255:
                Mpq10 += math.pow(j,1) * math.pow(i,0)
                Mpq01 += math.pow(j,0) * math.pow(i,1)
                Mpq00 += math.pow(j,0) * math.pow(i,0)

    xCentroide = Mpq10/Mpq00
    yCentroide = Mpq01/Mpq00
    
    return xCentroide

def momentoCentral(imagen, p, q):
    roi = Image.open(imagen).convert('L')
    data = roi.load()
    ancho, largo = roi.size