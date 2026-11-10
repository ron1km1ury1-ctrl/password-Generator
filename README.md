# PASSWORD GENERATOR

A clean, dark-themed Windows desktop app for creating random passwords locally.

## Features
- Choose a password length from 8 to 128 characters
- Uses Python's cryptographically strong `secrets` module
- Copy a password to the clipboard
- Optional automatic refresh every 60 seconds
- Modern dark interface and custom shield-and-lock icon
- Builds as a standalone Windows executable

## Build and run on Windows
1. Install Python from [python.org](https://www.python.org/downloads/). Enable the Python launcher (`py`) during installation.
2. Download and extract this repository, or clone it with Git.
3. Keep the project files together in one folder.
4. Double-click `BUILD_PASSWORD_GENERATOR.bat`.
5. When the build completes, open `dist\PASSWORD GENERATOR.exe`.

The build script creates the icon from `make_icon.py` and uses PyInstaller. An internet connection may be needed to install PyInstaller the first time.

To run the source directly, open a terminal in the folder and run:

```bat
py PASSWORD_GENERATOR.py
```

## Publish a Windows download
Build the executable on Windows, then create a GitHub Release and attach `dist\PASSWORD GENERATOR.exe`.

## Security and privacy
Passwords are generated locally on your computer. The app does not send passwords over the internet and does not change your Windows or account login password. Automatic refresh replaces the displayed password every 60 seconds, so copy and save any password you intend to keep.

## Project files
- `PASSWORD_GENERATOR.py` — desktop app source
- `BUILD_PASSWORD_GENERATOR.bat` — Windows build helper
- `make_icon.py` — creates the Windows `.ico` icon
- `app_icon.svg` — editable vector icon artwork
