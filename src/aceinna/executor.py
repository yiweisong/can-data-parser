import sys
import os

# Set persistent configuration directory for Matplotlib to avoid rebuilding font cache every time
if sys.platform == 'win32':
    mpl_config_dir = os.path.join(os.getenv('APPDATA'), 'can-data-parser', 'matplotlib')
else:
    mpl_config_dir = os.path.join(os.path.expanduser('~'), '.config', 'can-data-parser', 'matplotlib')

if not os.path.exists(mpl_config_dir):
    try:
        os.makedirs(mpl_config_dir)
    except OSError:
        pass 
os.environ['MPLCONFIGDIR'] = mpl_config_dir

from PySide6.QtWidgets import QApplication
from aceinna.ui.main_window import MainWindow
from aceinna.core.config_store import ConfigStore

def main():
    app = QApplication(sys.argv)
    
    config_store = ConfigStore()
    
    window = MainWindow(config_store)
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
