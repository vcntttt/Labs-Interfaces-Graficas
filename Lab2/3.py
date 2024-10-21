from utils import *
import math

roi2 = initImage('roi2.png')

mu11 = centralMoment(roi2, 1, 1)
mu20 = centralMoment(roi2, 2, 0)
mu02 = centralMoment(roi2, 0, 2)

theta = math.degrees(0.5 * math.atan2(2*mu11,mu20 - mu02))
print(f"mu11: {mu11}, mu20: {mu20}, mu02: {mu02}\ntheta: {theta}")