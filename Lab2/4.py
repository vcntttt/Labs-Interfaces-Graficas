from utils import *


def h1(image):
    return momentoCentralNormalizado(image, 2, 0) + momentoCentralNormalizado(image, 0, 2)


def h2(image):
    return (momentoCentralNormalizado(image, 2, 0) - momentoCentralNormalizado(image, 0, 2))**2 + 4 * momentoCentralNormalizado(image, 1, 1)**2


def h3(image):
    return (momentoCentralNormalizado(image, 3, 0) - 3 * momentoCentralNormalizado(image, 1, 2))**2 + (3 * momentoCentralNormalizado(image, 2, 1) - momentoCentralNormalizado(image, 0, 3))**2


roi1 = initImage('roi1.png')
print(h1(roi1))
print(h2(roi1))
print(h3(roi1))
