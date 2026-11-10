# PASSWORD GENERATOR

A simple Windows desktop app that generates a random password, shows it in a GUI window, and refreshes it automatically every 60 seconds.

## What it does
- Generates a password between 8 and 128 characters
- Uses letters, numbers, and special characters
- Refreshes the displayed password every 60 seconds
- Lets you copy the current password to your clipboard
- Runs as a desktop app on Windows

## Important note
This app does not change your laptop or device login password. It only changes the password shown inside the app window.

## Run it on your laptop
1. Install Python from: https://www.python.org/downloads/
2. Make sure the Python launcher is added to PATH during installation.
3. Download or clone this repository to your laptop.
4. Open the project folder.
5. Double-click `BUILD_PASSWORD_GENERATOR.bat`.
6. Wait for the build to finish.
7. Open the generated file in the `dist` folder:
   `dist\PASSWORD GENERATOR.exe`

## Files in this repository
- `PASSWORD_GENERATOR.py` — the application code
- `BUILD_PASSWORD_GENERATOR.bat` — builds the Windows executable using PyInstaller

## Build command used
```bat
py -m PyInstaller --onefile --windowed --clean --name "PASSWORD GENERATOR" PASSWORD_GENERATOR.py
```

## Publish to GitHub
1. Upload this repository to GitHub.
2. Create a Release.
3. Attach the built `dist\PASSWORD GENERATOR.exe` file.
4. Share the Release link with users.
