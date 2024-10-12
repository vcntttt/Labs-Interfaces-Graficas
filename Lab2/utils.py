from PIL import Image
import numpy as np


def initImage(path):
    img = Image.open(path).convert('L')  # carga en escala de grises
    imgArray = np.array(img)
    # binarizar la imagen con respecto a 128
    imgArray = (imgArray > 128).astype(np.uint8)

    return imgArray


def moment(image, p, q):
    m = 0
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if (image[y, x] == 1):
              m += (x**p) * (y**q)
    return m


def centroid(image):
    M00 = moment(image, 0, 0)
    M10 = moment(image, 1, 0)
    M01 = moment(image, 0, 1)

    centroide = (float(M10/M00), float(M01/M00))
    return centroide


def centralMoment(image, p, q):
    mu = 0
    cx, cy = centroid(image)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if (image[y, x] == 1):
              mu += ((x - cx)**p) * ((y - cy)**q) 

    return mu


def momentoCentralNormalizado(image, p, q):
    return centralMoment(image, p, q) * \
        (1 / centralMoment(image, 0, 0)) ** ((p+q+2)/2)
