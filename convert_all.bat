@echo off
echo == INICIANDO CONVERSÃO NA PASTA /wsq ==

cd wsq

echo.
echo Arquivos .wsq encontrados:
dir *.wsq
echo.

for %%f in (*.wsq) do (
    echo Convertendo %%f...
    dwsq %%~nf_raw.pgm %%f -raw_out
)

echo.
echo Chamando o script Python para gerar .png...
python ..\convert_pgm_to_png.py

echo.
echo ✅ Conversão completa!
pause