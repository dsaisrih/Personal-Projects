# Idea Manager - Executable Build Guide

## Quick Start (Easiest Way)

### Option 1: Run the Build Script
1. In the project folder, **double-click** `BUILD_EXE.bat`
2. Wait for the build to complete
3. Your `.exe` file will be in the `release/` folder

### Option 2: Manual Build (PowerShell)
```powershell
# Navigate to project folder
cd "c:\Users\dsais\OneDrive\Desktop\Projects\Python\Idea Manager Project - 3"

# Build the executable
.\.venv\Scripts\pyinstaller.exe --onefile --windowed --name "Idea Manager" idea.py
```

## After Building

✅ **Executable Location:** `dist/Idea Manager.exe`

You can now:
- Move the `.exe` anywhere on your computer
- Run it without Python installed
- Send it to others (no installation needed!)

## Troubleshooting

**Issue: "mysql-connector-python not found"**
- Solution: The exe bundles all dependencies automatically

**Issue: Database connection fails**
- Make sure MySQL is running on your machine
- Check database credentials in the code (line with `self.host`, `self.user`)

## Creating a Shortcut

1. Right-click `Idea Manager.exe`
2. Click "Send to" → "Desktop (create shortcut)"
3. Now you have a desktop shortcut!

## Sharing the App

The `.exe` file is completely standalone. You can:
- Share via email
- Put on USB drive
- Upload to cloud storage
- Anyone can run it (on Windows with MySQL installed)

---

**Note:** PyInstaller bundles Python + all libraries into a single executable (about 150-200 MB)
