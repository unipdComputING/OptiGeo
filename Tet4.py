import numpy as np
import vtk
from Global import *
from Node import Node
from Property import Property

class Tet4:
  # ---------------------------------------------------------------------------
  def __init__(self, id: int = 0, connectivity: list[int] = (0, 0, 0, 0), id_prop: int = 0) -> None:
    self.id: int = id
    self.connectivity: list[int] = connectivity
    self.id_prop: int = id_prop
    self.TOT_EL_NODES: int = 4
    self.surface = np.array([
        [0, 1, 2],
        [0, 1, 3],
        [1, 2, 3],
        [0, 2, 3],
    ]).copy()
    self.nPtGauss: int = 1
    #                 2
    #               / |
    #             /  ||
    #           /   | |
    #         /    |  |
    #        0 ------ 3
    #         \   |  /
    #          \ | /
    #            1
  # ---------------------------------------------------------------------------
  def _get_surface_nodes(self, id_surf, nodes) -> list[Node]:
    """Private method to determine the list of nodes defining an element face.
    @param id_surf: Integer identifier of the hexahedral face (values from 0 to 2).
    @param nodes: Global list of nodes.
    @return: surf_nodes, the list of nodes defining the face specified by id_surf.
    """
    local_pos: list = self.surface[id_surf]
    surf_nodes: list[Node] = []
    for pos in local_pos:
      id_node = self.connectivity[pos]
      pos_node = find_pos(nodes, id_node)
      if pos_node >= 0:
        surf_nodes.append(nodes[pos_node])
    return surf_nodes
  # ---------------------------------------------------------------------------
  def add_surface_stress(self, nodes: list, id_surf: int,
                         stress_value: np.ndarray = np.zeros(3)) -> None:
      
      surf_nodes = self._get_surface_nodes(id_surf, nodes)
      a: float = surf_nodes[0].dist(surf_nodes[1])
      b: float = surf_nodes[0].dist(surf_nodes[2])
      c: float = surf_nodes[1].dist(surf_nodes[2])
      p: float = a + b + c
      Area_surf = np.sqrt(p * (p - a) * (p - b) * (p - c)) # formula di Erone col semiperimetro p
      for node in surf_nodes:
          node.add_load(stress_value * Area_surf / 3.0)
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
  def compute_Vol(self,nodes: list[Node]) -> float:
      n0 = nodes[0]
      n1 = nodes[1]
      n2 = nodes[2]
      n3 = nodes[3]
      vmat = np.array([
          [1, n0.x[0], n0.x[1], n0.x[2]],
          [1, n1.x[0], n1.x[1], n1.x[2]],
          [1, n2.x[0], n2.x[1], n2.x[2]],
          [1, n3.x[0], n3.x[1], n3.x[2]],
      ])
      Vol = np.linalg.det(vmat) / 6.
      if Vol < 0 :
          print("Det Negative")
      return Vol
  # ---------------------------------------------------------------------------
  def build_B(self,nodes: list[Node]) -> np.ndarray:
      B = np.zeros((6, 12))

      Index = np.array([ # matrice di combinazione per definire iterativamente i nodi da utilizzare
          [1, 2, 3],
          [0, 3, 2],
          [0, 1, 3],
          [0, 2, 1],
      ])

      for i in range(4):
          n0: Node = nodes[Index[i, 0]]
          n1: Node = nodes[Index[i, 1]]
          n2: Node = nodes[Index[i, 2]]

          bmat = np.array([
              [1, n0.x[1], n0.x[2]],
              [1, n1.x[1], n1.x[2]],
              [1, n2.x[1], n2.x[2]],
          ])
          b = np.linalg.det(bmat)

          cmat = np.array([
              [n0.x[0], 1, n0.x[2]],
              [n1.x[0], 1, n1.x[2]],
              [n2.x[0], 1, n2.x[2]],
          ])
          c = np.linalg.det(cmat)

          dmat = np.array([
              [n0.x[0], n0.x[1], 1],
              [n1.x[0], n1.x[1], 1],
              [n2.x[0], n2.x[1], 1],
          ])
          d = np.linalg.det(dmat)

          B[0, i*3 : i*3+3] = [b, 0, 0]
          B[1, i*3 : i*3+3] = [0, c, 0]
          B[2, i*3 : i*3+3] = [0, 0, d]
          B[3, i*3 : i*3+3] = [c, b, 0]
          B[4, i*3 : i*3+3] = [0, d, b]
          B[5, i*3 : i*3+3] = [d, 0, c]

      V = self.compute_Vol(nodes)
      if V<0:
          print("Jacobian Negative")

      B = B / (V * 6.)
      return B
  # ---------------------------------------------------------------------------
  def stiffness(self, nodes: list[Node], prop: Property) -> np.ndarray:
      (_, D) = prop.get_const_mat()
      K: np.ndarray = np.zeros((12, 12))
      B = self.build_B(nodes)
      V: float = self.compute_Vol(nodes)

      for i in range(4):
          for j in range(4):
            K[3*i:3*i+3, 3*j:3*j+3] += (B[0:6, 3*i:3*i+3].T @ D) @ B[0:6, 3*j:3*j+3] * V

      return K
  # ---------------------------------------------------------------------------
  def adding_surface_partialconstraint(self,id_surf:int,fix:np.ndarray,nodes:list[Node]) -> None:
    surf_nodes = self._get_surface_nodes(id_surf, nodes)
    for node in surf_nodes:
      node.add_constraint(fix, np.zeros(DIM_DOF))
  # ---------------------------------------------------------------------------
  def compute_B(self,nodes: list[Node]) -> np.ndarray:
      B = np.zeros((1, 72))
      b = self.build_B(nodes)
      for i in range(DIM_TENSOR):
          B[0, i * 12: i * 12 + 12] = b[i, :]
      return B
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  def get_actor(self, nodes: list[Node] = None, color=(0.8, 0.8, 0.8), opacity=1.0) -> vtk.vtkActor:
    if nodes is None:
        return None

    nodes_position = self.get_nodes_position(nodes)

    points = vtk.vtkPoints()
    for pos in nodes_position:
        points.InsertNextPoint(nodes[pos].x)

    # Create quad faces (your hex faces)
    vtk_polys = vtk.vtkCellArray()

    faces = [
        [0, 1, 2],
        [0, 1, 3],
        [1, 2, 3],
        [0, 2, 3]
    ]

    for face in faces:
        vtk_polys.InsertNextCell(3)
        for idx in face:
            vtk_polys.InsertCellPoint(idx)

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)

    # ⬅️ This is the key fix
    polydata.SetPolys(vtk_polys)

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