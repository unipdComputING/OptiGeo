from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QSplitter, QTableWidgetItem, QSizePolicy, QLineEdit, QListView, QFormLayout
#import vtk
#from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os
from mainwindow import MainWindow as AppMainWindow

class StartWindow(QMainWindow):
    def __init__(self):
        super(StartWindow, self).__init__()

        self.setWindowTitle("OptiGeo - Start Menu")
        self.resize(600, 300)

        ###########################################################

        self.central_widget = QWidget()
        self.splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self.central_widget)
        
        ########################################################### pyvista

        self.left_widget = QWidget()
        self.left_layout = QGridLayout(self.left_widget)
        self.label = QLabel()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.pixmap = QPixmap(os.path.join(base_dir, "72704765.png"))
        self.label.setPixmap(self.pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
       
        self.left_layout.addWidget(self.label)
        self.splitter.addWidget(self.left_widget)

        ###########################################################
       
        self.buttons_widget = QWidget()
        self.buttons_layout = QVBoxLayout(self.buttons_widget)
        self.create_file_button = QPushButton("Create new project ...")
        self.choose_file_button = QPushButton("Choose file ...")
        self.quit_button = QPushButton("Quit")
        self.create_file_button.setFixedHeight(30)
        self.choose_file_button.setFixedHeight(30)
        self.quit_button.setFixedHeight(30)
        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.create_file_button)
        self.buttons_layout.addWidget(self.choose_file_button)
        self.buttons_layout.addWidget(self.quit_button)
        self.buttons_layout.addStretch()
        self.create_file_button.clicked.connect(self.new_file)

        self.splitter.addWidget(self.buttons_widget)

        ###########################################################

        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.splitter)
        self.splitter.setSizes([600, 400])

    def open_main_window(self, file_path=None):
            self.main_window = AppMainWindow(file_path)
            self.main_window.show()
            self.close()

    def new_file(self):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, "second_basic_input_file.txt")
            if file_path:
                self.open_main_window(file_path=file_path)

    def choose_file():
            pass

    def app_quit(self):
            self.close()

if __name__ == "__main__":
    start_app = QApplication()
    start_window = StartWindow()
    start_window.show()
    start_app.exec()