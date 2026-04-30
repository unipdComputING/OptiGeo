from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QTableWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QTabWidget, QSplitter, QTableWidgetItem, QSizePolicy, QLineEdit, QListView, QPlainTextEdit
#import vtk
#from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
import sys
import os
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtkmodules.all as vtk
from read_file import parse_input_file
from write_file import write_the_file
from All import All
from Vtk import build_mesh_actors

class MainWindow(QMainWindow):
    def __init__(self, file_path=None):
        super(MainWindow, self).__init__()
        
        self.file_path = file_path
        #self.df_globalproperties, self.df_nodes, self.df_beams,  self.df_tetra, self.df_hexa, self.df_properties, self.df_solvers = parse_input_file(self.file_path)
        all = All(self.file_path)
    #################################################################################################################################################################################################################################################################################
        self.setWindowTitle("OptiGeo")
        self.resize(900, 450)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.splitter = QSplitter(Qt.Vertical)

        self.main_layout.addWidget(self.splitter)
        
        #################### VTK ####################
        
        self.vtk_widget = QVTKRenderWindowInteractor()
        self.splitter.addWidget(self.vtk_widget)
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(1, 1, 1)
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.vtk_interactor = self.vtk_widget.GetRenderWindow().GetInteractor()

        style = vtk.vtkInteractorStyleTrackballCamera()
        self.vtk_interactor.SetInteractorStyle(style)
        self.vtk_interactor.Initialize()
        self.render_model(all)

        #################### BOTTOM ####################

        self.text_or_table_widget = QWidget()
        self.text_or_table_layout = QHBoxLayout(self.text_or_table_widget)
        self.text_or_table_tabs = QTabWidget(self.text_or_table_widget)
        
        self.text_editor_widget = QWidget()
        self.text_editor_layout = QGridLayout(self.text_editor_widget)
        
        self.table_editor_widget = QWidget()
        self.table_editor_layout = QHBoxLayout(self.table_editor_widget)
       
        self.text_or_table_tabs.addTab(self.text_editor_widget,"Text editor")
        self.text_or_table_tabs.addTab(self.table_editor_widget,"Table editor")

        self.text_or_table_layout.addWidget(self.text_or_table_tabs)
        self.splitter.addWidget(self.text_or_table_widget)

        #################### TEXT ####################

        self.text_edit = QPlainTextEdit()
        self.text_editor_layout.addWidget(self.text_edit, 0, 0, 1, 2)
        #self.text_edit.textChanged.connect(lambda: print(self.text_edit.document().toPlainText()))

        file_content = open(file_path)
        content = file_content.readlines()
        for i in range(len(content)):
            self.text_edit.insertPlainText(content[i])

        self.save_text_button = QPushButton("Save")
        self.save_text_button.setFixedSize(60,30)
        self.save_text_button.clicked.connect(self.save_text_button_operation)
        self.text_editor_layout.addWidget(self.save_text_button, 1, 0)
        
        #################### TABLE ####################

        #$$$$$$$$$$$$$$ ELEMENTS $$$$$$$$$$$$$$

        self.elements_widget = QWidget()
        self.elements_layout = QHBoxLayout(self.elements_widget)
        self.elements_tabs = QTabWidget(self.elements_widget)
        self.elements = ["Node","Beams", "Tetra", "Hexa"] # Aggiunto beams
        k = 0
        #for element, ml in zip([self.df_nodes, self.df_beams, self.df_tetra, self.df_hexa], [len(self.df_nodes), len(self.df_beams),  len(self.df_tetra), len(self.df_hexa)]):
        dataframes = [all.df_nodes, all.df_beams, all.df_tetra, all.df_hexa] ###############################################################################################################################################
        for element, ml, df_ref in zip(dataframes, [len(df) for df in dataframes], dataframes):
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
                self.beams_table = table
            elif k == 2:
                self.tet_table = table
            elif k == 3:
                self.hexa_table = table
        ############################################################################################################################################################################################################################################################
            
            table.itemChanged.connect(lambda item, idx=k: self.update_dataframe(all, item, idx))

            save_btn = QPushButton("Save")
            save_btn.setFixedSize(70, 30)
            save_btn.clicked.connect(lambda checked, et=k: self.save_file(all, et))
            add_btn = QPushButton("+")
            add_btn.setFixedSize(30, 30)
            add_btn.clicked.connect(lambda checked, et=k: self.add_tofile(all, et))
            delete_btn = QPushButton("-")
            delete_btn.setFixedSize(30, 30)
            delete_btn.clicked.connect(lambda checked, et=k: self.delete_infile(all, et))

            self.buttons_widget = QWidget()
            self.buttons_layout = QHBoxLayout(self.buttons_widget)
            self.buttons_layout.addWidget(save_btn)
            self.buttons_layout.addWidget(add_btn)
            self.buttons_layout.addWidget(delete_btn)
            self.buttons_layout.addStretch()

            main_layout.addWidget(table, 1)
            main_layout.addWidget(self.buttons_widget, 0)
            
            self.elements_tabs.addTab(tab_widget, self.elements[k])
            k += 1

        self.elements_layout.addWidget(self.elements_tabs)
        
        #$$$$$$$$$$$$$$ PROPERTIES $$$$$$$$$$$$$$

        self.properties_widget = QWidget()
        self.properties_layout = QHBoxLayout(self.properties_widget)

        #$$$$$$$$$$$$$$ SOLVERS $$$$$$$$$$$$$$

        self.solvers_widget = QWidget()
        self.solvers_layout = QHBoxLayout(self.solvers_widget)

        ##############################################
        self.all_tabs = QTabWidget()
        self.all_tabs.addTab(self.elements_widget, "Elements")
        self.all_tabs.addTab(self.properties_widget, "Properties")
        self.all_tabs.addTab(self.solvers_widget, "Solvers")

        self.table_editor_layout.addWidget(self.all_tabs)
        self.splitter.setSizes([500, 500])

    
    # TEXT METHODS #
    def save_text_button_operation(self):
        self.success_label = QLabel("Saved correctly")
        self.text_editor_layout.addWidget(self.success_label, 1, 1)
        self.success_label.setStyleSheet("color: green")
    
    # TABLE METHODS # #implementare motore GMSH (NETGEN?) per visualizzare in VTK con pyvista

    def save_file(self, all, et):
        write_the_file(self.file_path, all.df_globalproperties, all.df_nodes, all.df_beams,  all.df_tetra, all.df_hexa, all.df_properties, all.df_solvers)
        self.render_model(all)
        print(self.file_path)

    def add_tofile(self, all, et):
        table, default_id, num_cols, df = self.match_item(all, et)
        table.blockSignals(True)
        default_values = [default_id] + ["0"]*(num_cols - 1)
        all.get_df(et).loc[len(df)] = default_values
        print(df)
        row_position = table.rowCount()
        table.insertRow(row_position)
        
        for col in range(num_cols):
            item = QTableWidgetItem(default_values[col])
            table.setItem(row_position, col, item)
        
        table.setCurrentCell(row_position, 0)
        table.blockSignals(False)
        print(f"Riga aggiunta in posizione {row_position}")


    def delete_infile(self, all, et):
        table, default_id, num_cols, df = self.match_item(all, et)
        table.blockSignals(True)
        row = table.currentRow()
        if row != -1:
            all.set_df(et, all.get_df(et).drop(index=row).reset_index(drop=True))
            table.removeRow(row)
            print(f"Riga {row} eliminata")
        table.blockSignals(False)

    def match_item(self, all, elemtype):
        match elemtype:
            case 0:
                table = self.node_table
                default_id = str(len(all.df_nodes)+1)+"N"
                num_cols = len(all.df_nodes.columns)
                df = all.df_nodes
            case 1: 
                table = self.beams_table
                default_id = str(len(all.df_beams)+1)+"B"
                num_cols = len(all.df_beams.columns)
                df = all.df_beams
            case 2:
                table = self.tet_table
                default_id = str(len(all.df_tetra)+1)+"T"
                num_cols = len(all.df_tetra.columns)
                df = all.df_tetra
            case 3:
                table = self.hexa_table
                default_id = str(len(all.df_hexa)+1)+"H"
                num_cols = len(all.df_hexa.columns)
                df = all.df_hexa
#####################################################################################################################################################
        return table, default_id, num_cols, df

    def update_dataframe(self, all,item, idx):
        ########################################################################################################################################################
        df = all.get_df(idx)
        row = item.row()
        col = item.column()
        value = item.text()
        original_type = df.dtypes.iloc[col]
        try:
            if original_type == "int64":
                value = int(value)
            elif original_type == "float64":
                value = float(value)
        except ValueError:
            pass
        
        df.loc[df.index[row], df.columns[col]] = value
    
    def render_model(self, all):
        self.renderer.RemoveAllViewProps()

        for elements_df in [all.df_beams, all.df_tetra, all.df_hexa]:
            actors = build_mesh_actors(all.df_nodes, elements_df)
            for actor in actors:
                self.renderer.AddActor(actor)

        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()
        
        

'''''
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
'''