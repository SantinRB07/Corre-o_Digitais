import os

print("📏 Tamanho de cada arquivo _raw.pgm:")

for fname in os.listdir():
    if fname.endswith("_raw.pgm"):
        size = os.path.getsize(fname)
        print(f"{fname}: {size} bytes")

