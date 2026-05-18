from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QMessageBox
from .home_page import HomePage
from .config_page import ConfigPage
from .io_config_manager import IOConfigManager
from ..core.config_store import ConfigStore

class MainWindow(QMainWindow):
    def __init__(self, config_store: ConfigStore):
        super().__init__()
        self.setWindowTitle("CAN Data Parser")
        #self.resize(800, 600)
        self.setMinimumWidth(800)
        self.config_store = config_store
        
        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.home_page = HomePage(self.config_store)
        self.config_page = ConfigPage(self.config_store)
        self.io_manager = IOConfigManager(self.config_store)
        
        # Navigation Bar
        self.__create_menus()
        
        # Stacked Pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.home_page)
        self.main_layout.addWidget(self.stacked_widget)


    def show_config(self, s):
        #prompt a window to show configuration
        self.config_page.show()
    
    def show_about(self):
        QMessageBox.about(self, "About Application",
                          "Can Data Parser v1.1.1\n\n")
    
    def show_import_dialog(self):
        self.io_manager.import_config()
        
    def show_export_dialog(self):
        self.io_manager.export_config()
    
    def __create_menus(self):
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&Settings")
        
        configuration_action = QAction("Convertors and Rules", self)
        configuration_action.setMenuRole(QAction.MenuRole.NoRole)
        configuration_action.setStatusTip("Edit Convertors and Rules")
        configuration_action.triggered.connect(self.show_config)
        file_menu.addAction(configuration_action)
        
        file_menu.addSeparator()
        
        configuration_menu = file_menu.addMenu("&Configuration File")
        configuration_menu.menuAction().setMenuRole(QAction.MenuRole.NoRole)
        import_action = QAction("Import", self)
        import_action.setMenuRole(QAction.MenuRole.NoRole)
        import_action.setStatusTip("Import Configurations")
        import_action.triggered.connect(self.show_import_dialog)
        configuration_menu.addAction(import_action)
        
        export_action = QAction("Export", self)
        export_action.setMenuRole(QAction.MenuRole.NoRole)
        export_action.setStatusTip("Export Configurations")
        export_action.triggered.connect(self.show_export_dialog)
        configuration_menu.addAction(export_action)

        # Help menu
        help_menu = menu_bar.addMenu("&Help")
        
        about_action = QAction("About", self)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.setStatusTip("About this application")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        

        
