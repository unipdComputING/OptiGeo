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
    self.N_GAUSS: int = 1
    self.surface = np.array([
        [0, 1, 2],
        [0, 1, 3],
        [1, 2, 3],
        [0, 2, 3],
    ]).copy()

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
  def build_B(self, nodes: list[Node]) -> tuple[np.ndarray, float]:
      B = np.zeros((6, 12))
      x = np.zeros((4, 1))
      y = np.zeros((4, 1))
      z = np.zeros((4, 1))

      for i in range(len(nodes)):
          x[i] = nodes[i].x[0]
          y[i] = nodes[i].x[1]
          z[i] = nodes[i].x[2]

      a = np.array([
          y[1] * (z[3] - z[2]) - y[2] * (z[3] - z[1]) + y[3] * (z[2] - z[1]),
          -y[0] * (z[3] - z[2]) + y[2] * (z[3] - z[0]) - y[3] * (z[2] - z[0]),
          y[0] * (z[3] - z[1]) - y[1] * (z[3] - z[0]) + y[3] * (z[1] - z[0]),
          -y[0] * (z[2] - z[1]) + y[1] * (z[2] - z[0]) - y[2] * (z[1] - z[0]),
      ])

      b = np.array([
          -x[1] * (z[3] - z[2]) + x[2] * (z[3] - z[1]) - x[3] * (z[2] - z[1]),
          x[0] * (z[3] - z[2]) - x[2] * (z[3] - z[0]) + x[3] * (z[2] - z[0]),
          -x[0] * (z[3] - z[1]) + x[1] * (z[3] - z[0]) - x[3] * (z[1] - z[0]),
          x[0] * (z[2] - z[1]) - x[1] * (z[2] - z[0]) + x[2] * (z[1] - z[0]),
      ])

      c = np.array([
          x[1] * (y[3] - y[2]) - x[2] * (y[3] - y[1]) + x[3] * (y[2] - y[1]),
          -x[0] * (y[3] - y[2]) + y[2] * (y[3] - y[0]) - x[3] * (y[2] - y[0]),
          x[0] * (y[3] - y[1]) - x[1] * (y[3] - y[0]) + x[3] * (y[1] - y[0]),
          -x[0] * (y[2] - y[1]) + x[1] * (y[2] - y[0]) - x[2] * (y[1] - y[0]),
      ])

      V = self.compute_Vol(nodes)
      for i in range(4):
          col = 3 * i
          B[0, col + 0] = a[i]
          B[1, col + 1] = b[i]
          B[2, col + 2] = c[i]
          B[3, col + 0] = b[i]
          B[3, col + 1] = a[i]
          B[4, col + 1] = c[i]
          B[4, col + 2] = b[i]
          B[5, col + 0] = c[i]
          B[5, col + 2] = a[i]

      B = B / (6 * V)
      return (B, V)
  # ---------------------------------------------------------------------------
  def stiffness(self, nodes: list[Node], prop: Property) -> np.ndarray:
      #(_, D) = prop.get_const_mat()
      D = prop.get_el_const_mat()
      K: np.ndarray = np.zeros((12, 12))
      (B, V) = self.build_B(nodes)

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
  def get_strain(self, el_nodes: list[Node], ip: int) -> np.ndarray:
    a: np.ndarray = np.concatenate((el_nodes[0].dof, el_nodes[1].dof, el_nodes[2].dof, el_nodes[3].dof), axis=0)
    B, _  = self.build_B(el_nodes)
    strain: np.ndarray = np.zeros(DIM_TENSOR, dtype=float)
    strain = B @ a
    return strain
  # ---------------------------------------------------------------------------
  def updates(self, el_nodes: list[Node], prop: Property,
              el_strain: np.ndarray, el_stress: np.ndarray, el_statev: np.ndarray) -> None:
      for ip in range(self.N_GAUSS):
          ostrain: np.ndarray = el_strain[ip, :]
          dstrain: np.ndarray = self.get_strain(el_nodes, ip)
          statev: np.ndarray = el_statev[ip, :]
          stress: np.ndarray = el_stress[ip, :]

          prop.get_const_mat(ostrain, dstrain, stress, statev)

          el_strain[ip, :] = ostrain + dstrain
          el_stress[ip, :] = stress
          el_statev[ip, :] = statev
      return
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