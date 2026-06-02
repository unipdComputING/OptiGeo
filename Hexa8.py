import  numpy as np
from numpy import ndarray as nd
import vtk
from Node import Node
from Property import Property
from Global import *


class Hexa8:
  # ---------------------------------------------------------------------------
  def __init__(self, id: int = 0, connectivity: list[int] = (0, 0, 0, 0, 0, 0, 0, 0), id_prop: int = 0,nu:float=0) -> None:
    self.id: int = id
    self.connectivity: list[int] = connectivity
    self.id_prop: int = id_prop
    self.TOT_EL_NODES: int = 8
    self.nu: float = nu
    self.N_GAUSS: int = 8
    self.surface:np.ndarray = np.array([
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 1, 5, 4],
        [3, 2, 6, 7],
        [0, 4, 7, 3],
        [1, 2, 6, 5],
    ]).copy()
  # ---------------------------------------------------------------------------
  def _get_surface_nodes(self, id_surf, nodes) -> list[Node]:
    """Private method to determine the list of nodes defining an element face.
    @param id_surf: Integer identifier of the hexahedral face (values from 0 to 5).
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
  def add_surface_stress(self, nodes: list[Node], id_surf: int,
                         stress_value: np.ndarray = np.zeros(3)) -> None:
    surf_nodes = self._get_surface_nodes(id_surf, nodes)
    v1 = surf_nodes[1].direction(surf_nodes[0])
    v2 = surf_nodes[1].direction(surf_nodes[2])
    Area_surf = np.linalg.norm(np.cross(v1, v2))
    for node in surf_nodes:
      node.add_load(stress_value * Area_surf / 4)
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
  def shape_grad_local(self,xi: float, eta: float, zeta: float) -> np.ndarray:
    xi_i = np.array([-1, 1, 1, -1, -1, 1, 1, -1])
    eta_i = np.array([-1, -1, 1, 1, -1, -1, 1, 1])
    zeta_i = np.array([-1, -1, -1, -1, 1, 1, 1, 1])

    dN = np.zeros((8, 3))
    for i in range(8):
      #--dNi/dsci
      dN[i, 0] = 0.125 * xi_i[i] * (1 + eta_i[i] * eta) * (1 + zeta_i[i] * zeta)
      #--dNi/deta
      dN[i, 1] = 0.125 * eta_i[i] * (1 + xi_i[i] * xi) * (1 + zeta_i[i] * zeta)
      #--dNi/dzeta
      dN[i, 2] = 0.125 * zeta_i[i] * (1 + xi_i[i] * xi) * (1 + eta_i[i] * eta)
    return dN
  # ---------------------------------------------------------------------------
  def build_B(self,dN_dxyz: np.ndarray) -> np.ndarray:
    B = np.zeros((6, 24))
    for i in range(8):
      dNx, dNy, dNz = dN_dxyz[i, :]
      col = 3 * i

      B[0, col + 0] = dNx
      B[1, col + 1] = dNy
      B[2, col + 2] = dNz

      B[3, col + 0] = dNy
      B[3, col + 1] = dNx

      B[4, col + 1] = dNz
      B[4, col + 2] = dNy

      B[5, col + 0] = dNz
      B[5, col + 2] = dNx
    return B
  # ---------------------------------------------------------------------------
  def compute_B(self, nodes: list[Node], ip) -> np.ndarray:
      coords = np.array([n.x for n in nodes])
      a = 1. / np.sqrt(3.)
      gp = np.array([
          [-a, -a, -a],
          [a, -a, -a],
          [a, a, -a],
          [-a, a, -a],
          [-a, -a, a],
          [a, -a, a],
          [a, a, a],
          [-a, a, a],
      ])

      xi = gp[ip,0]
      eta = gp[ip,1]
      zeta = gp[ip,2]
      dN_dxi = self.shape_grad_local(xi, eta, zeta)  # 8x3

      # Jacobian
      J = coords.T @ dN_dxi  # 3x3

      invJ = np.linalg.inv(J)
      dN_dxyz = dN_dxi @ invJ.T
      B = self.build_B(dN_dxyz)
      return B
  # ---------------------------------------------------------------------------
  def stiffness(self, nodes: list[Node], prop: Property,
                el_strain: nd, el_dstrain: nd, el_stress: nd, el_statev: nd) -> {nd, nd}:

    coords = np.array([n.x for n in nodes])

    #(_, D) = prop.get_const_mat()
    #D = prop.get_el_const_mat()

    a = 1. / np.sqrt(3.)
    gp = [-a, a]
    # stiffness matrix
    K : nd = np.zeros((24, 24), dtype=float)
    # internal load
    Fi: nd = np.zeros((24), dtype=float)
    # tengent constitutive tensor
    D: nd = np.zeros((DIM_TENSOR, DIM_TENSOR), dtype=float)

    ig: int = 0
    for xi in gp:
      for eta in gp:
        for zeta in gp:
          strain : nd = el_strain [ig, :]
          dstrain: nd = el_dstrain[ig, :]
          stress:  nd = el_stress [ig, :]
          statev:  nd = el_statev [ig, :]
          energy_density: float = 0.0 #######################################TEST
          prop.get_const_mat(strain, dstrain, stress, D, energy_density, statev)

          dN_dxi = self.shape_grad_local(xi, eta, zeta)  # 8x3

          # Jacobian
          J = coords.T @ dN_dxi  # 3x3
          detJ = np.linalg.det(J)
          if detJ <= 0:
              print(f"Hex8 {self.id}: detJ <= 0, negative jacobian determinant")

          invJ = np.linalg.inv(J)
          dN_dxyz = dN_dxi @ invJ.T
          B = self.build_B(dN_dxyz)

          K  += B.T @ (D @ B) * detJ
          Fi += B.T @ stress * detJ

          el_stress [ig, :] = stress
          el_statev [ig, :] = statev

          ig += 1

    return K
  # ---------------------------------------------------------------------------
  def adding_surface_partialconstraint(self,id_surf:int,fix:np.ndarray,nodes:list[Node]) -> None:
    surf_nodes = self._get_surface_nodes(id_surf, nodes)
    for node in surf_nodes:
      node.add_constraint(fix, np.zeros(DIM_DOF))
  # ---------------------------------------------------------------------------
  def get_strain(self, el_nodes: list[Node], ip: int) -> np.ndarray:
    a: np.ndarray = np.concatenate((el_nodes[0].dof, el_nodes[1].dof, el_nodes[2].dof, el_nodes[3].dof,
                                    el_nodes[4].dof, el_nodes[5].dof, el_nodes[6].dof, el_nodes[7].dof), axis=0)
    B = self.compute_B(el_nodes, ip)
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

          # prop.get_const_mat(ostrain, dstrain, stress, statev)
          D: nd = np.zeros((DIM_TENSOR, DIM_TENSOR), dtype=float)
          energy_density: float = 0.0 #######################################TEST
          prop.get_const_mat(ostrain, dstrain, stress, D, energy_density, statev)

          el_strain[ip, :] = ostrain + dstrain
          el_stress[ip, :] = stress
          el_statev[ip, :] = statev
      return
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
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
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 1, 5, 4],
        [1, 2, 6, 5],
        [2, 3, 7, 6],
        [3, 0, 4, 7]
    ]

    for face in faces:
        vtk_polys.InsertNextCell(4)
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