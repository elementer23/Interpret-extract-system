# Interpret Extract System

This project uses AI and OCR to find, extract, and interpret annotations from technical drawings (P&ID). The goal is to export this structured data for personal or professional use.

## Prerequisites

Before starting, ensure you have the following two components ready:

1. **Tesseract-OCR Engine**: This must be installed separately on your Windows system, and its installation directory must be added to your Windows Environment Variables (`PATH`). 
   * *Please refer to the separate installation guide provided in this package for step-by-step instructions.*
2. **uv**: A fast Python package and dependency manager that automatically installs the correct Python version and libraries for this project.

---

## Installation & Setup

### 1. Installing uv (Windows)
If you do not have `uv` installed yet, open **PowerShell as an Administrator** and run the following command:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Once the installation is complete, **close that PowerShell window entirely** to apply the system changes.

### 2. Syncing Dependencies
Now, navigate to the project folder you received. Open a **new** terminal (PowerShell or Command Prompt) inside this specific folder and run:

```bash
uv sync
```

`uv` will automatically detect the project requirements, download the correct, stable Python environment, and install all 150+ required AI and UI libraries. 

---

## How to Run the Application

Once the sync is complete, you have two ways to start the application:

### Option A: Via the Terminal (Recommended for testing)
Inside the same project terminal, simply type and execute:
```bash
uv run start-app
```

### Option B: Via the Desktop Shortcut (Easiest)
Close your terminal. In the root of the project folder, locate the file named **`start.bat`** and double-click it. This will automatically open a background terminal and launch the PyQt6 interface for you instantly.

---

## 🛠️ Adding Custom AI Models (Optional)
The application comes pre-packaged with a core default model. If you wish to use a newly trained or custom YOLO model in the future:
1. Navigate to: `C:\Users\<Your_Username>\AppData\Local\interpret_extract_system\models\`
2. Place your new `.pt` file inside this folder.
3. Name the file whatever you desire (example): **`custom_yolo.pt`** (or use the settings dropdown inside the application to switch between detected models). Make sure that the file is a `.pt` since that's the base extension that **YOLO** uses. 

**CONGRATULATIONS!** Your system is now fully operational. Detailed explanations of features, workflows, and exporting data can be found in the comprehensive user guide included in this package.
