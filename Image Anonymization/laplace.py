import cv2
import numpy as np
from PIL import Image

image = cv2.imread('pic1.jpg')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

epsilon = 0.08
sensitivity = 1.0

def add_noise_to_region(region, epsilon, sensitivity):
    scale = sensitivity / epsilon
    noise = np.random.laplace(0, scale, region.shape)
    noisy_region = region + noise
    noisy_region = np.clip(noisy_region, 0, 255)
    return noisy_region

for i in range(20):
    newEpi = epsilon*(0.9**i)
    for (x, y, w, h) in faces:
        face_region = image[y:y+h, x:x+w]
        noisy_face_region = add_noise_to_region(face_region, newEpi, sensitivity)
        image[y:y+h, x:x+w] = noisy_face_region

    anonymized_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    anonymized_image.save(f'laplace{newEpi}.jpg')
