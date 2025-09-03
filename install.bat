@echo off
echo ========================================
echo    INSTALADOR MERCADOLIBRE SCRAPER
echo ========================================
echo.

echo Instalando dependencias de Python...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo ========================================
echo    INSTALACION COMPLETADA
echo ========================================
echo.
echo Para ejecutar el scraper:
echo   python main.py
echo.
echo Para probar solo el scraper:
echo   python scraper.py
echo.
pause
