import os
import cv2
import numpy as np
import pandas as pd
from skimage.measure import shannon_entropy

def calcular_nitidez(img):
    return cv2.Laplacian(img, cv2.CV_64F).var()

def calcular_textura(img):
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1)
    return np.mean(sobelx**2 + sobely**2)

def extrair_features(path, label):
    dados = []
    for fname in os.listdir(path):
        if fname.endswith(".png"):
            fpath = os.path.join(path, fname)
            img = cv2.imread(fpath, cv2.IMREAD_GRAYSCALE)
            if img is None: continue
            entropia = shannon_entropy(img)
            nitidez = calcular_nitidez(img)
            textura = calcular_textura(img)
            proporcao = img.shape[1] / img.shape[0]
            dados.append([entropia, nitidez, textura, proporcao, label])
    return dados

dados = []
dados += extrair_features("boas", 1)
dados += extrair_features("borradas", 0)

df = pd.DataFrame(dados, columns=["entropia", "nitidez", "textura", "proporcao", "label"])
df.to_csv("dataset.csv", index=False)
print("✅ Dataset salvo em dataset.csv")
