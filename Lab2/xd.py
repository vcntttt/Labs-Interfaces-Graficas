import cv2
import numpy as np

# Función para cargar y verificar la imagen
def cargar_imagen(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen en {path}")
    return img

# Cargar y procesar roi_1.png para el cálculo del centroide
img1 = cargar_imagen('roi1.png')

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

# Cargar y procesar roi_2.png para otros cálculos
img2 = cargar_imagen('roi2.png')

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
hu_moments = cv2.HuMoments(moments2).flatten()

# Imprimir los momentos de Hu
print("\nMomentos de Hu (roi_2.png):")
print(f"  I1 = {hu_moments[0]}")
print(f"  I2 = {hu_moments[1]}")
print(f"  I3 = {hu_moments[2]}")
