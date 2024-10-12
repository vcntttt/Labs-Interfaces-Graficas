from utils import *


roi2 = initImage('roi2.png')

mu11 = centralMoment(roi2, 1, 1)
mu20 = centralMoment(roi2, 2, 0)
mu02 = centralMoment(roi2, 0, 2)


theta = np.degrees(0.5 * np.arctan((2*mu11)/(mu20 - mu02)))
print(theta)