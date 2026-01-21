import sys
import os

# Add src to python path to ensure imports work if run from project root
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.core.config_store import ConfigStore

def main():
    app = QApplication(sys.argv)
    
    config_store = ConfigStore()
    
    window = MainWindow(config_store)
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
