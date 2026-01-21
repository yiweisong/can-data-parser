# Packaging Instructions

## 1. Environment Setup

To ensure a clean environment and faster packaging, it is recommended to use a fresh virtual environment.

```bash
# Create venv
python -m venv venv

# Activate venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller
```

## 2. Address Matplotlib Font Cache Issue

The "building font cache" message usually appears on the first run. To minimize startup time:

1.  **Reduce Matplotlib Imports:** If possible, only import `matplotlib.pyplot` when needed, or use a non-interactive backend if checking generic things.
2.  **Bundle Cache (Advanced):** You can try to locate your local `fontlist-v330.json` (or similar) from your `.matplotlib` folder and include it in `datas` in `build.spec`.
    *   Find `mpl-data` in your python environment.
    *   Add it to `datas` in `build.spec`.

However, the simplest fix for users is to let them run it once. The cache should be persistent if the application has write access to its user data directory.

## 3. Icon Issue

The `build.spec` references `aceinna.ico`. Ensure this file exists in the directory where you run `pyinstaller`.

If the icon doesn't show on the `.exe` file in Explorer immediately, it might be the **Windows Icon Cache**.
*   Try moving the .exe to a different folder.
*   Right-click -> Properties to see if the icon is there.

## 4. Building

Run PyInstaller with the spec file:

```bash
pyinstaller --clean --noconfirm build.spec
```

The `--clean` flag helps clear PyInstaller caches.
