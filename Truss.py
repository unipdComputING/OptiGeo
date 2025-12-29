import  numpy as np
import vtk
from Global import *
from Node import Node
from Property import Property

'''
                <1>  <2>
connectivity = [(i), (j)]
'''


class Truss:
  # ---------------------------------------------------------------------------
  def __init__(self, id: int = 0, connectivity: list[int] = (0, 0), id_prop: int = 0) -> None:
    self.id: int = id
    self.connectivity: list[int] = connectivity
    self.id_prop: int = id_prop
    self.TOT_EL_NODES: int = 2
    self.actor: vtk.vtkActor = None
  # ---------------------------------------------------------------------------
  def stiffness(self, el_nodes: list[Node], prop: Property) -> np.ndarray:
    n1: Node = el_nodes[0]
    n2: Node = el_nodes[1]
    l0: float = n1.dist(n2)
    if l0 <= 0.0:
      return np.zeros((2 * DIM_DOF, 2 * DIM_DOF))
    y: np.ndarray = n1.direction(n2)
    yy: np.ndarray = np.outer(y, y)
    K: np.ndarray = np.block([
      [ yy, -yy],
      [-yy,  yy]
    ])
    return (prop.young * prop.area / l0**3) * K
  # ---------------------------------------------------------------------------
  def get_nodes_position(self, nodes: list[Node]) -> list[int]:
    nodes_position: list[int] = []
    for id_node in self.connectivity:
      pos: int = find_pos(nodes, id_node)
      if pos < 0:
        print(f"ERROR in EL: {self.id}: node {id_node} not defined")
        quit()
      nodes_position.append(pos)
    return nodes_position
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  def get_actor(self, nodes: list[Node] = None, color=(0.8, 0.8, 0.8), opacity=1.0) -> vtk.vtkActor:
    if nodes is None:
      return None
    nodes_position: list[int] = self.get_nodes_position(nodes)
    """Create and return a vtkActor for rendering"""

    points = vtk.vtkPoints()
    for i in range(len(nodes_position)):
      p = nodes[nodes_position[i]].x
      points.InsertNextPoint(p)
    
    # Create vertices to represent each point
    vertices = vtk.vtkCellArray()
    for i in range(points.GetNumberOfPoints()):
        vertex = vtk.vtkVertex()
        vertex.GetPointIds().SetId(0, i)
        vertices.InsertNextCell(vertex)

    lines = vtk.vtkCellArray()
    line = vtk.vtkLine()
    line.GetPointIds().SetId(0, 0)
    line.GetPointIds().SetId(1, 1)
    lines.InsertNextCell(line)


    # vtk_lines = vtk.vtkActor()
    # vtk_lines.GetProperty().SetColor(0/255, 128/255, 255/255)   # Green lines
    # vtk_lines.GetProperty().SetLineWidth(6)     # Thicker lines
    # vtk_lines.SetPoints(points)
    # vtk_lines.SetLines(lines)

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(lines)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    actor.GetProperty().SetOpacity(opacity)
    actor.GetProperty().SetEdgeVisibility(True)
    actor.GetProperty().SetEdgeColor(0, 0, 0)

    self.actor = actor
    return actor
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------