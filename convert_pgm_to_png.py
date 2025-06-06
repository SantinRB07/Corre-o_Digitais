import os
import numpy as np
from PIL import Image

def fatorar_resolucao(n_bytes):
    candidatos = []
    for w in range(100, 800):
        if n_bytes % w == 0:
            h = n_bytes // w
            proporcao = w / h
            if 0.4 <= proporcao <= 1.0:
                candidatos.append((w, h))
    return candidatos

print("🔍 Gerando múltiplas resoluções para análise...")

for fname in os.listdir():
    if fname.endswith("_raw.pgm"):
        filesize = os.path.getsize(fname)
        candidatos = fatorar_resolucao(filesize)

        if not candidatos:
            print(f"⛔ {fname}: nenhuma resolução plausível ({filesize} bytes)")
            continue

        with open(fname, 'rb') as f:
            raw = f.read()

        for i, (width, height) in enumerate(candidatos[:5]):  # tenta até 5 por arquivo
            try:
                img_array = np.frombuffer(raw[:width * height], dtype=np.uint8).reshape((height, width))
                img = Image.fromarray(img_array)
                output_name = fname.replace("_raw.pgm", f"_{width}x{height}_v{i+1}.png")
                img.save(output_name)
                print(f"✅ {fname} → {output_name}")
            except Exception as e:
                print(f"⚠️ Erro {width}x{height}: {e}")

print("✅ Geração concluída. Verifique visualmente quais versões estão corretas.")
