"""
La segmentation d'une image par sélection de couleurs consiste à 
extraire des plages de pixels ayant une certaine couleur. 
Cela permet de repérer des objets en fonction de leur couleur.

Ce document montre comment effectuer cette segmentation avec OpenCV. 
La représentation des couleurs RVB et la conversion en TSL sont expliquées 
dans Espace des couleurs RVB.
"""

import cv2 as cv
from matplotlib.pyplot import *
from matplotlib import cm
import numpy
import math

"""
On traite la photographie suivante, 
qui comporte des billes colorées posées sur un plan en bois. 
OpenCV range les couches dans l'ordre BGR (Blue,Green,Red). 
Pour afficher l'image avec Matplotlib, il faut les mettre dans l'ordre RGB.
"""
img1 = cv.imread("billes.png")
img2 = cv.cvtColor(img1,cv.COLOR_BGR2RGB)
figure(figsize=(4,4))
cv.imshow("lll",img2)
red,green,blue = cv.split(img2)
figure(figsize=(12,4))
subplot(131)
cv.imshow("Red",red)
subplot(132)
cv.imshow("Green",green)
subplot(133)
cv.imshow("Blue",blue)
cv.waitKey(0)




"""
La couche rouge permet de discriminer les billes bleues et vertes, 
qui apparaissent très sombres car elles comportent très peu de rouge. 
Pour segmenter l'image, il faut effectuer un seuillage :
"""
seuil=110.0
ret,seg_red = cv.threshold(red,seuil,255.0,cv.THRESH_BINARY_INV)
figure(figsize=(4,4))
cv.imshow("segmentation red",seg_red)
cv.waitKey(0)


seuil=200.0
ret,seg_red = cv.threshold(red,seuil,255.0,cv.THRESH_BINARY)
figure(figsize=(4,4))
cv.imshow("segmentation red",seg_red)

"""
La bille rouge n'est pas bien sélectionnée car une partie a une luminosité proche du fond
sur la couche rouge. Voila ce qui arrive si on abaisse le seuil :
"""
seuil=190.0
ret,seg_red = cv.threshold(red,seuil,255.0,cv.THRESH_BINARY)
figure(figsize=(4,4))
cv.imshow("Segmentation Red",seg_red)
cv.waitKey(0)
cv.destroyAllWindows()

"""
3. Couches TSL
La conversion d'une image RVB en image TSL est expliquée dans Espace des couleurs RVB.
 T est la teinte, qui est un angle en degrés, 
 S est la saturation, 
 et L la luminance. 
 Le format correspondant dans openCV est HSV (Hue,Saturation,Value).
"""
hsv = cv.cvtColor(img1,cv.COLOR_BGR2HSV)
hue,sat,val = cv.split(hsv)
figure(figsize=(12,4))
subplot(131)
cv.imshow("Hue",hue)
subplot(132)
cv.imshow("Saturation",sat)
subplot(133)
cv.imshow("Value",val)
cv.waitKey(0)


"""
La couche T permet de sélectionner des pixels on fonction de leur teinte. 
Par exemple, pour sélectionner les pixels jaunes, 
il faut sélectionner les pixels dont la teinte est dans une plage située à environ 
45 degrés. 
Dans OpenCV, les valeurs de teinte sont en faite comprises entre 0 et 180,
de manière à pouvoir les représenter sur une image en niveaux de gris. 
Il faut donc diviser les angles par deux.
"""


lower = numpy.array([36/2],dtype=numpy.uint8)
upper = numpy.array([60/2],dtype=numpy.uint8)
seg_hue = cv.inRange(hue,lower,upper)
figure(figsize=(4,4))
cv.imshow("Segmentation Hue",seg_hue)

"""
La bille jaune est très bien isolée, 
mais il y a aussi un contour sur deux billes vertes. 
L'examen de la couche S (saturation) montre que ces contours 
sont sans doute beaucoup moins saturés que le jaune de la bille. 
Nous allons donc faire une sélection directement sur l'image HSV, 
en choisissant aussi une plage de saturation :

"""
lower = numpy.array([36/2,180,0],dtype=numpy.uint8)
upper = numpy.array([60/2,255,255],dtype=numpy.uint8)
seg = cv.inRange(hsv,lower,upper)
figure(figsize=(4,4))
cv.imshow("Segmentation",seg)

"""
Une fois la bille jaune isolée, 
on peut obtenir sa position en calculant le barycentre des pixels blancs.
La teinte verte se situe vers 90 degrés. 
On peut sélectionner une bille verte :
"""
lower = numpy.array([70/2,0,0],dtype=numpy.uint8)
upper = numpy.array([100/2,255,255],dtype=numpy.uint8)
seg = cv.inRange(hsv,lower,upper)
figure(figsize=(4,4))
cv.imshow("Segmentation",seg)

"""
La teinte rouge se situe vers 0 degré :
"""


lower = numpy.array([0,190,0],dtype=numpy.uint8)
upper = numpy.array([15,255,255],dtype=numpy.uint8)
seg = cv.inRange(hsv,lower,upper)
figure(figsize=(4,4))
cv.imshow("Segmentation",seg)
cv.waitKey(0)
cv.destroyAllWindows()
"""
k=0
# Close the window when key q is pressed
while k!=113:
  # Display the image
  cv.imshow("Window", img2)
  k = cv.waitKey(0)
"""