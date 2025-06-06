import os
import subprocess
from PIL import Image

WSQ_DIR = "wsq"  # Pasta onde estão os arquivos .wsq
OUT_DIR = "alternativas"
os.makedirs(OUT_DIR, exist_ok=True)

if not os.path.exists("falhas_resolucao.txt"):
    print("⛔ Arquivo falhas_resolucao.txt não encontrado!")
    exit(1)

with open("falhas_resolucao.txt", "r") as f:
    arquivos_raw_pgm = [linha.strip() for linha in f if linha.strip().endswith("_raw.pgm")]

# Remover o sufixo "_raw.pgm" e obter o nome do .wsq correspondente
wsq_filenames = [nome.replace("_raw.pgm", ".wsq") for nome in arquivos_raw_pgm]

print(f"🔁 Tentando reprocessar {len(wsq_filenames)} arquivos usando dwsq (sem -raw_out)...")

for wsq in wsq_filenames:
    wsq_path = os.path.join(WSQ_DIR, wsq)

    if not os.path.exists(wsq_path):
        print(f"❌ Arquivo não encontrado: {wsq_path}")
        continue

    pgm_output = os.path.join(OUT_DIR, wsq.replace(".wsq", "_alt.pgm"))
    png_output = pgm_output.replace(".pgm", ".png")

    # Chamada ao dwsq (sem -raw_out)
    try:
        subprocess.run(["dwsq", pgm_output, wsq_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Erro ao executar dwsq para {wsq}: {e}")
        continue

    # Tenta abrir o .pgm com PIL
    try:
        img = Image.open(pgm_output)
        img.save(png_output)
        print(f"✅ {wsq} → {png_output}")
    except Exception as e:
        print(f"⛔ Falha ao converter {pgm_output}: {e}")

print("✅ Reprocessamento alternativo concluído. Veja a pasta 'alternativas/'")
