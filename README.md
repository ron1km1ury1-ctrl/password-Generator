# PASSWORD GENERATOR

A small Windows desktop app that creates random passwords and can refresh the displayed password every 60 seconds.

## Features
- Choose a password length from 8 to 128 characters
- Uses Python's `secrets` module to select letters, digits, and symbols
- Copy the displayed password to the clipboard
- Optional automatic refresh every 60 seconds
- Custom shield-and-lock application icon
- Builds as a standalone Windows executable

## Build and run on Windows
1. Install Python from [python.org](https://www.python.org/downloads/). During setup, enable the Python launcher (`py`) and add Python to PATH.
2. Download this repository and extract it, or clone it with Git.
3. Keep the project files together in one folder.
4. Double-click `BUILD_PASSWORD_GENERATOR.bat`.
5. When the build completes, open `dist\\PASSWORD GENERATOR.exe`.

The build script creates `app_icon.ico` from `make_icon.py` and uses PyInstaller to build the executable. It may need an internet connection the first time to install PyInstaller.

## Run from Python instead
Open a terminal in the project folder and run:

```bat
py PASSWORD_GENERATOR.py
```

## Publish a Windows download on GitHub
After building, open the repository's **Releases** page, draft a release, and attach `dist\\PASSWORD GENERATOR.exe`. The executable is built for Windows; build it on Windows for best compatibility.

## Security and privacy
Passwords are generated locally on your computer using Python's cryptographically strong `secrets` module. This app does not send passwords over the internet or change your Windows/device login password. The app replaces the displayed password when automatic refresh is running, so copy and save any password you intend to use before it refreshes.

## Project files
- `PASSWORD_GENERATOR.py` — desktop app source
- `BUILD_PASSWORD_GENERATOR.bat` — Windows build helper
- `make_icon.py` — creates the Windows `.ico` icon using only Python's standard library
- `app_icon.svg` — editable vector artwork for the app icon
