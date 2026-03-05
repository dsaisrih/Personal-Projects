@echo off
REM Build Idea Manager as Executable
REM This script converts the Python app to a standalone .exe file

echo Building Idea Manager executable...
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Build with PyInstaller
pyinstaller --onefile --windowed --name "Idea Manager" --distpath ".\release" idea.py

echo.
echo Build completed!
echo Your executable is located in: release\Idea Manager.exe
echo.
pause
