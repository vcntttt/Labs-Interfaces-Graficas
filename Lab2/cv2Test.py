import cv2
import numpy as np
from utils import *

img1 = initImage("roi1.png")
img2 = initImage("roi2.png")

# Calcular los momentos de la imagen
moments1 = cv2.moments(img1)

# Imprimir los momentos calculados para roi_1.png
print("Momentos calculados para roi_1.png:")
for key, value in moments1.items():
    print(f"  {key}: {value}")

# Calcular el centroide usando los momentos M10 y M01
x_c = moments1['m10'] / moments1['m00']
y_c = moments1['m01'] / moments1['m00']

print(f"\nCentroide de roi_1.png: (x_c = {x_c}, y_c = {y_c})")

# Calcular los momentos de la imagen
moments2 = cv2.moments(img2)

# Imprimir los momentos calculados para roi_2.png
print("\nMomentos calculados para roi_2.png:")
for key, value in moments2.items():
    print(f"  {key}: {value}")

# Calcular el momento central normalizado η12
mu12 = moments2['nu12']
print(f"\nMomento central normalizado η12 (roi_2.png): {mu12}")

# Calcular el ángulo de orientación usando los momentos centrales
mu11 = moments2['mu11']
mu20 = moments2['mu20']
mu02 = moments2['mu02']

theta = 0.5 * np.arctan2(2 * mu11, mu20 - mu02)
theta_degrees = np.degrees(theta)

print(f"\nÁngulo de orientación (roi_2.png): {theta_degrees} grados")

# Calcular los momentos de Hu
hu_moments = cv2.HuMoments(moments1).flatten()

# Imprimir los momentos de Hu
print("\nMomentos de Hu (roi_1.png):")
print(f"  H1 = {hu_moments[0]}")
print(f"  H2 = {hu_moments[1]}")
print(f"  H3 = {hu_moments[2]}")

m00 = moments1['m00']
p = 1
q = 2
norm_moment = mu11 / (m00 ** ((p + q) / 2 + 1))