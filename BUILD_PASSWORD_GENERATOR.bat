@echo off
cd /d "%~dp0"
title Build PASSWORD GENERATOR
echo =====================================
echo       PASSWORD GENERATOR BUILDER
echo =====================================
echo.

where py >nul 2>nul
if errorlevel 1 (
    echo Python launcher was not found.
    echo Install Python from https://www.python.org/downloads/
    echo During installation, enable "Add Python to PATH".
    pause
    exit /b 1
)

echo Creating the application icon...
py make_icon.py
if errorlevel 1 (
    echo Could not create the application icon.
    pause
    exit /b 1
)

echo Installing or updating PyInstaller...
py -m pip install --upgrade pyinstaller
if errorlevel 1 (
    echo Could not install PyInstaller.
    pause
    exit /b 1
)

echo.
echo Building Windows application...
py -m PyInstaller --onefile --windowed --clean --icon app_icon.ico --name "PASSWORD GENERATOR" PASSWORD_GENERATOR.py
if errorlevel 1 (
    echo Build failed. Check the error messages above.
    pause
    exit /b 1
)

echo.
echo SUCCESS!
echo Your app is in the dist folder:
echo dist\PASSWORD GENERATOR.exe
pause
