import os
import cv2
import numpy as np
import shutil
from skimage.measure import shannon_entropy
from sklearn.preprocessing import StandardScaler
import joblib

# Load modelo e scaler
clf = joblib.load("modelo_svm.joblib")
scaler = joblib.load("scaler.joblib")

def calcular_nitidez(img):
    return cv2.Laplacian(img, cv2.CV_64F).var()

def calcular_textura(img):
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1)
    return np.mean(sobelx**2 + sobely**2)

# Pasta com digitais a analisar
entrada = "wsq"
saida = "selecionadas"
os.makedirs(saida, exist_ok=True)

for fname in os.listdir(entrada):
    if fname.endswith(".png"):
        fpath = os.path.join(entrada, fname)
        img = cv2.imread(fpath, cv2.IMREAD_GRAYSCALE)
        if img is None: continue

        entropia = shannon_entropy(img)
        nitidez = calcular_nitidez(img)
        textura = calcular_textura(img)
        proporcao = img.shape[1] / img.shape[0]

        X = np.array([[entropia, nitidez, textura, proporcao]])
        X_scaled = scaler.transform(X)
        prob = clf.predict_proba(X_scaled)[0][1]

        if prob > 0.5:
            shutil.copy(fpath, os.path.join(saida, fname))
            print(f"✅ {fname} selecionada (confiança: {prob:.2f})")
        else:
            print(f"⛔ {fname} descartada (confiança: {prob:.2f})")
