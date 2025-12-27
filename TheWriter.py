from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QTableWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QTabWidget, QSplitter, QTableWidgetItem, QSizePolicy, QLineEdit, QListView, QFormLayout
#import vtk
#from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from TheReader import read_main_file

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("OptiGeo")
        self.resize(900, 450)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.splitter = QSplitter(Qt.Horizontal)
        
        #################### VTK ####################
        
        self.container = QWidget()
        self.splitter.addWidget(self.container)
        
        #################### ELEMENTS ####################
        
        self.elements_widget = QWidget()
        self.elements_layout = QVBoxLayout(self.elements_widget)
        self.elements_tabs = QTabWidget(self.elements_widget)
        
        dfnode, dftetra, dfhexa, dfprops, mnodes, mtetra, mhexa, mprops = read_main_file("stuff.txt")
        print(dfprops.head())
        self.dfnode = dfnode
        self.dftetra = dftetra
        self.dfhexa = dfhexa
        self.element_list = [self.dfnode, self.dftetra, self.dfhexa]
        self.mnodes = mnodes
        self.mtetra = mtetra
        self.mhexa = mhexa
        self.mlist = [self.mnodes, self.mtetra, self.mhexa]
        self.elements = ['Node', 'Tetra', 'Hexa']
        k = 0
        for element, ml in zip(self.element_list, self.mlist):
            
            tab_widget = QWidget()
            main_layout = QVBoxLayout(tab_widget)
 
            table = QTableWidget()
            table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            table.setColumnCount(len(element.columns))
            table.setHorizontalHeaderLabels(element.columns.tolist())
            table.setRowCount(len(element))
            
            for i in range(len(element)):
                for j in range(len(element.columns)):
                    table.setItem(i, j, QTableWidgetItem(str(element.iat[i, j])))

            if k == 0:
                self.node_table = table
            elif k == 1:
                self.tet_table = table
            elif k == 2:
                self.hexa_table = table
  
            save_btn = QPushButton("Save")
            save_btn.clicked.connect(lambda checked, et=k: self.save_file(et))
            add_btn = QPushButton("+")
            add_btn.setFixedSize(30, 30)
            add_btn.clicked.connect(lambda checked, et=k: self.add_tofile(et))
            delete_btn = QPushButton("-")
            delete_btn.setFixedSize(30, 30)
            delete_btn.clicked.connect(lambda checked, et=k: self.delete_infile(et))

            buttons_widget = QWidget()
            buttons_layout = QHBoxLayout(buttons_widget)
            buttons_layout.addWidget(save_btn)
            buttons_layout.addWidget(add_btn)
            buttons_layout.addWidget(delete_btn)
            buttons_layout.addStretch()

            main_layout.addWidget(table, 1)
            main_layout.addWidget(buttons_widget, 0)
            
            self.elements_tabs.addTab(tab_widget, self.elements[k])
            k += 1

        self.elements_layout.addWidget(self.elements_tabs)
        
        #################### MATERIAL PROPERTIES ####################
        
        self.m_properties_widget = QWidget()
        self.m_properties_layout = QHBoxLayout(self.m_properties_widget)
        self.propertieselector_widget = QWidget()
        self.propertieselector_layout = QVBoxLayout(self.propertieselector_widget)
        self.properties = QListView()
        model = QStandardItemModel()
        self.properties.setModel(model)
        self.properties.setMaximumWidth(150)
        for element in list(dfprops["id"]):
            model.appendRow(QStandardItem(str(element)))
        self.propertieselector_layout.addWidget(self.properties)
        self.propertiesmodifier_widget = QWidget()
        self.propertiesmodifier_layout = QFormLayout(self.propertiesmodifier_widget)
        self.propertiesmodifier_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.propertiesmodifier_layout.setFormAlignment(Qt.AlignRight | Qt.AlignTop)
        self.property_lineedits = []

        for stuff in list(dfprops.columns[2:]):
            lineedit = QLineEdit()
            self.property_lineedits.append(lineedit)
            self.propertiesmodifier_layout.addRow(stuff, lineedit)
        
        self.m_properties_layout.addWidget(self.propertieselector_widget, 0)
        self.m_properties_layout.addWidget(self.propertiesmodifier_widget, 1)
        
        #################### SIMULATION PROPERTIES ####################
        
        self.simulation_widget = QWidget()
        self.simulation_layout = QGridLayout(self.simulation_widget)
        
        #################### SOLVER ####################
        
        self.solver_widget = QWidget()
        self.solver_layout = QGridLayout(self.solver_widget)
        
        #################### OTHER ####################
        
        self.help_widget = QWidget()
        self.help_layout = QGridLayout(self.help_widget)
        self.help_layout.setSpacing(0) 
        with open("help.txt", "r") as f:
            content = f.readlines()
        for line in content:
            self.label = QLabel(line)
            self.help_layout.addWidget(self.label)
        
        
        
        #################### TERMINATOR ####################
        
        self.all_tabs = QTabWidget()
        self.all_tabs.addTab(self.elements_widget, "Elements")
        self.all_tabs.addTab(self.m_properties_widget, "Properties")
        self.all_tabs.addTab(self.simulation_widget, "Simulation")
        self.all_tabs.addTab(self.solver_widget, "Solvers")
        self.all_tabs.addTab(self.help_widget, "?")
        
        self.splitter.addWidget(self.all_tabs)
        self.splitter.setSizes([700, 300])
        
        self.master_layout = QVBoxLayout(self.central_widget)
        self.master_layout.addWidget(self.splitter)
        
        #################### METHODS ####################
        
    def add_tofile(self, elemtype):
        match elemtype:
            case 0: 
                table = self.node_table
                num_cols = len(self.dfnode.columns)
                default_id = "N"
            case 1: 
                table = self.tet_table
                num_cols = len(self.dftetra.columns)
                default_id = "T"
            case 2: 
                table = self.hexa_table
                num_cols = len(self.dfhexa.columns)
                default_id = "H"
        
        row_position = table.rowCount()
        table.insertRow(row_position)
        
        default_values = [default_id] + ["0"] * (num_cols - 1)  
        for col in range(num_cols):
            item = QTableWidgetItem(default_values[col])
            table.setItem(row_position, col, item)
        
        table.setCurrentCell(row_position, 0)
        print(f"Riga aggiunta in posizione {row_position}")

    def delete_infile(self, elemtype):
        match elemtype:
            case 0: 
                table = self.node_table
            case 1: 
                table = self.tet_table
            case 2: 
                table = self.hexa_table
        
        row = table.currentRow()
        
        if row != -1:
            table.removeRow(row)
            print(f"Riga {row} eliminata")
    
    def save_file(self, elemtype):
        match elemtype:
            case 0: 
                table = self.node_table
                indexes = self.mnodes
            case 1: 
                table = self.tet_table
                indexes = self.mtetra
            case 2: 
                table = self.hexa_table
                indexes = self.mhexa
        
        table.clearSelection()
        
        row_data = []
        for row in range(table.rowCount()):
            sub_row_data = []
            for column in range(table.columnCount()):
                item = table.item(row, column)
                sub_row_data.append(item.text() if item else "")
            row_data.append(' '.join(sub_row_data))

        with open("stuff.txt", "r") as f:
            lines = f.readlines()
        for idx in sorted(indexes, reverse=True):
            del lines[idx]
        lines[min(indexes):min(indexes)] = row_data
        
        with open('stuff.txt', 'w') as f:
            for riga in lines:
                f.write(riga.rstrip('\n') + '\n')
        
        _, _, _, _, mnodes, mtetra, mhexa, _ = read_main_file("stuff.txt")
        self.mnodes = mnodes
        self.mtetra = mtetra
        self.mhexa = mhexa
        
            
app = QApplication()
window = MainWindow()
window.show()
app.exec()