import vtk
import numpy as np
from Global import *
from Node import Node
from Element import Element
from Truss import Truss
from Tet4 import Tet4
from Hexa8 import Hexa8

# -----------------------------------------------------------------------------
def draw_mesh(nodes: list[Node] = None, elements: list[Element] = None) -> None:

  points = vtk.vtkPoints()
  for node in nodes:
    points.InsertNextPoint(node.x)
  
  lines = vtk.vtkCellArray()
  for element in elements:
    line = vtk.vtkLine()
    line.GetPointIds().SetId(0, element.id_nodes[0])
    line.GetPointIds().SetId(1, element.id_nodes[1])
    lines.InsertNextCell(line)

  # Create vertices to represent each point
  vertices = vtk.vtkCellArray()
  for i in range(points.GetNumberOfPoints()):
      vertex = vtk.vtkVertex()
      vertex.GetPointIds().SetId(0, i)
      vertices.InsertNextCell(vertex)

  # Create a polydata object to hold the points and vertices
  points_polydata = vtk.vtkPolyData()
  points_polydata.SetPoints(points)
  points_polydata.SetVerts(vertices)

  lines_polydata = vtk.vtkPolyData()
  lines_polydata.SetPoints(points)
  lines_polydata.SetLines(lines)

  # Mapper and actor
  points_mapper = vtk.vtkPolyDataMapper()
  lines_mapper = vtk.vtkPolyDataMapper()
  points_mapper.SetInputData(points_polydata)
  lines_mapper.SetInputData(lines_polydata)

  points_actor = vtk.vtkActor()
  points_actor.SetMapper(points_mapper)
  points_actor.GetProperty().SetPointSize(20)  # make points larger
  points_actor.GetProperty().SetColor(255/255, 128/255, 0/255) # red color
  points_actor.GetProperty().SetRenderPointsAsSpheres(True)
  lines_actor = vtk.vtkActor()
  lines_actor.SetMapper(lines_mapper)
  lines_actor.GetProperty().SetColor(0/255, 128/255, 255/255)   # Green lines
  lines_actor.GetProperty().SetLineWidth(6)     # Thicker lines

  # Renderer, render window, and interactor
  renderer = vtk.vtkRenderer()
  renderer.AddActor(lines_actor)
  renderer.AddActor(points_actor)
  renderer.SetBackground(0.1, 0.1, 0.1)  # dark background

  render_window = vtk.vtkRenderWindow()
  render_window.AddRenderer(renderer)
  render_window.SetSize(800, 800)

  interactor = vtk.vtkRenderWindowInteractor()
  interactor.SetRenderWindow(render_window)

  # Optional: smoother interaction
  style = vtk.vtkInteractorStyleTrackballCamera()
  interactor.SetInteractorStyle(style)

  # Start rendering
  render_window.Render()
  interactor.Start()
# -----------------------------------------------------------------------------
def save_vtk(path: str, nodes: list[Node] = None, elements: list[any] = None, 
             offset: list[int] = None, strain: np.ndarray = None, stress: np.ndarray = None,
             statev: np.ndarray = None) -> None:
  if nodes is None or elements is None:
    return
  
  n_points: int = len(nodes)
  n_cells: int = len(elements)
  conn_size: int = 0
  for el in elements:
    conn_size += el.TOT_EL_NODES + 1
  with open(path, "w") as file:
    file.write("# vtk DataFile Version 3.0\n")
    file.write("FEM results\n")
    file.write("ASCII\n")
    file.write("DATASET UNSTRUCTURED_GRID\n")
    # --
    # MESH
    # --
    # POINTS
    file.write(f"POINTS {n_points} double\n")
    for n in nodes:
      x = n.x[0]; y = n.x[1]; z = n.x[2]
      file.write(f"{x} {y} {z}\n")
    # CELLS/ELEMENTS
    file.write(f"CELLS {n_cells} {conn_size}\n")
    for el in elements:
      st: str = f"{el.TOT_EL_NODES}" 
      for id in el.connectivity:
        st += f" {id - 1}"
      file.write(st + "\n")
    # CELL TYPES
    # VTK_LINE  = 3   (Truss)
    # VTK_TETRA = 10  (Tet4)
    # VTK_VOXEL = 11  (Hexa8)
    file.write(f"CELL_TYPES  {n_cells}\n")
    for el in elements:
      if type(el) == Truss:
        file.write("3\n")
      elif type(el) == Tet4:
        file.write("10\n")
      elif type(el) == Hexa8:
        file.write("11\n")
    # --
    # SOLUTIONS
    # --
    # POINTS DATA
    file.write(f"POINT_DATA {n_points} \n")
    file.write("VECTORS displacements double\n")
    for n in nodes:
      file.write(f"{n.dof[0]} {n.dof[1]} {n.dof[2]}\n")
    # CELLS DATA
    if offset is None:
      return
    #
    file.write(f"CELL_DATA {n_cells}\n")
    #
    file.write("SCALARS property int 1\n")
    file.write("LOOKUP_TABLE default\n")
    for el in elements:
      file.write(f"{el.id_prop}\n")
    #
    file.write("VECTORS strain_voigt double\n")
    for i, el in enumerate(elements):
      el_strain: np.ndarray = strain[offset[i] : offset[i + 1], :]
      # valor medio le vtk non hanno i punti di integrzione ... forse la nuova versione
      str: np.ndarray = el_strain.sum(axis=0) / el.N_GAUSS
      file.write(f"{str[0]} {str[1]} {str[2]}\n")
    #
    file.write("VECTORS strain_voigt_shear double\n")
    for i, el in enumerate(elements):
      el_strain: np.ndarray = strain[offset[i] : offset[i + 1], :]
      # valor medio le vtk non hanno i punti di integrzione ... forse la nuova versione
      str: np.ndarray = el_strain.sum(axis=0) / el.N_GAUSS
      file.write(f"{str[3]} {str[4]} {str[5]}\n")
    #
    file.write("VECTORS stress_voigt double\n")
    for i, el in enumerate(elements):
      el_stress: np.ndarray = stress[offset[i] : offset[i + 1], :]
      # valor medio le vtk non hanno i punti di integrzione ... forse la nuova versione
      str: np.ndarray = el_stress.sum(axis=0) / el.N_GAUSS
      file.write(f"{str[0]} {str[1]} {str[2]}\n")
    #
    file.write("VECTORS stress_voigt_shear double\n")
    for i, el in enumerate(elements):
      el_stress: np.ndarray = stress[offset[i] : offset[i + 1], :]
      # valor medio le vtk non hanno i punti di integrzione ... forse la nuova versione
      str: np.ndarray = el_stress.sum(axis=0) / el.N_GAUSS
      file.write(f"{str[3]} {str[4]} {str[5]}\n")
    #
    #
    for id_statev in range(TOT_STATEV):
      file.write(f"SCALARS SDV{id_statev} double\n")
      file.write("LOOKUP_TABLE default\n")
      for i, el in enumerate(elements):
        el_statev: np.ndarray = statev[offset[i] : offset[i + 1], :]
        # valor medio le vtk non hanno i punti di integrzione ... forse la nuova versione
        stv: np.ndarray = el_statev.sum(axis=0) / el.N_GAUSS
        file.write(f"{stv[id_statev]}\n")


    

   
   
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------