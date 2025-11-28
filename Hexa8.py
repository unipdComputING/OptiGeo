import  numpy as np
from Global import *
from Node import Node
from Property import Property
import matplotlib.pyplot as plt
class Hexa8:
  # ---------------------------------------------------------------------------
  def __init__(self, id: int = 0, connectivity: list[int] = (0, 0, 0, 0, 0, 0, 0, 0), id_prop: int = 0,nu:float=0) -> None:
    self.id: int = id
    self.connectivity: list[int] = connectivity
    self.id_prop: int = id_prop
    self.TOT_EL_NODES: int = 8
    self.nu: float = nu
    self.surface = np.array([
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 1, 5, 4],
        [3, 2, 6, 7],
        [0, 4, 7, 3],
        [1, 2, 6, 5],
    ])
  # ---------------------------------------------------------------------------
  # nodes = [n1, n2, n3, n4, n5, n6, n7, n8]
  def stiffness(self, nodes: list[Node], prop: Property):
    pass
  # ---------------------------------------------------------------------------
  def add_surface_stress(self, nodes: list, id_surf: int,
                         stress_value: np.ndarray = np.zeros(3)) -> None:
      n0: Node = nodes[self.surface[id_surf, 0]]
      n1: Node = nodes[self.surface[id_surf, 1]]
      n2: Node = nodes[self.surface[id_surf, 2]]
      n3: Node = nodes[self.surface[id_surf, 3]]
      v1 = n1.direction(n0)
      v2 = n1.direction(n2)
      Area_surf = np.linalg.norm(np.cross(v1, v2))
      surf_nodes = [n0, n1, n2, n3]
      for node in surf_nodes:
          node.add_load(stress_value * Area_surf / 4)

  # ---------------------------------------------------------------------------
  #def stiffness(self, n1: Node, n2: Node, prop: Property) -> np.ndarray:

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
  def D_matrix(self,E: float, nu: float) -> np.ndarray:
      l = E*nu/((1+nu) * (1-2*nu))
      m = E/(2*(1+nu))

      D = np.array([
          [l + 2*m, l, l, 0., 0., 0.],
          [l, l + 2*m, l, 0., 0., 0.],
          [l, l, l + 2*m, 0., 0., 0.],
          [0., 0., 0., m, 0., 0.],
          [0., 0., 0., 0., m, 0.],
          [0., 0., 0., 0., 0., m]
      ])
      return D
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
  def stiffness(self, nodes: list[Node], prop: Property) -> np.ndarray:

      coords = np.array([n.x for n in nodes])

      E = prop.young
      nu = prop.poisson
      D = self.D_matrix(E, nu)

      a = 1. / np.sqrt(3.)
      gp = [-a, a]
      K = np.zeros((24, 24))

      for xi in gp:
          for eta in gp:
              for zeta in gp:
                  dN_dxi = self.shape_grad_local(xi, eta, zeta)  # 8x3

                  # Jacobian
                  J = coords.T @ dN_dxi  # 3x3
                  detJ = np.linalg.det(J)
                  if detJ <= 0:
                      print(f"Hex8 {self.id}: detJ <= 0，negative jacobian determinant")

                  invJ = np.linalg.inv(J)
                  dN_dxyz = dN_dxi @ invJ.T
                  B = self.build_B(dN_dxyz)

                  K += B.T @ D @ B * detJ

      return K
  # ---------------------------------------------------------------------------
  def draw_element(self, nodes: list[Node]) -> None:
      x = [nodes[n-1].x[0] for n in self.connectivity]
      y = [nodes[n-1].x[1] for n in self.connectivity]
      z = [nodes[n-1].x[2] for n in self.connectivity]

      fig = plt.figure(figsize=(10, 6))
      di = fig.add_subplot(111, projection='3d')
      di.scatter(x, y, z)
      for i in self.connectivity:
          di.text(nodes[find_pos(nodes,i)].x[0], nodes[find_pos(nodes,i)].x[1], nodes[find_pos(nodes,i)].x[2], str(nodes[i-1].id), fontsize=9)
      for i in range(0, 3):
          di.plot(
              [nodes[find_pos(nodes,self.connectivity[i])].x[0], nodes[find_pos(nodes,self.connectivity[i+1])].x[0]],
              [nodes[find_pos(nodes,self.connectivity[i])].x[1], nodes[find_pos(nodes,self.connectivity[i+1])].x[1]],
              [nodes[find_pos(nodes,self.connectivity[i])].x[2], nodes[find_pos(nodes,self.connectivity[i+1])].x[2]],
          )
          di.plot(
              [nodes[find_pos(nodes,self.connectivity[i])].x[0], nodes[find_pos(nodes,self.connectivity[i+4])].x[0]],
              [nodes[find_pos(nodes,self.connectivity[i])].x[1], nodes[find_pos(nodes,self.connectivity[i+4])].x[1]],
              [nodes[find_pos(nodes,self.connectivity[i])].x[2], nodes[find_pos(nodes,self.connectivity[i+4])].x[2]],
          )
          di.plot(
              [nodes[find_pos(nodes,self.connectivity[i+4])].x[0], nodes[find_pos(nodes,self.connectivity[i+5])].x[0]],
              [nodes[find_pos(nodes,self.connectivity[i+4])].x[1], nodes[find_pos(nodes,self.connectivity[i+5])].x[1]],
              [nodes[find_pos(nodes,self.connectivity[i+4])].x[2], nodes[find_pos(nodes,self.connectivity[i+5])].x[2]],
          )
      di.plot(
          [nodes[self.connectivity[3]-1].x[0], nodes[self.connectivity[0]-1].x[0]],
          [nodes[self.connectivity[3]-1].x[1], nodes[self.connectivity[0]-1].x[1]],
          [nodes[self.connectivity[3]-1].x[2], nodes[self.connectivity[0]-1].x[2]],
      )
      di.plot(
          [nodes[self.connectivity[7]-1].x[0], nodes[self.connectivity[4]-1].x[0]],
          [nodes[self.connectivity[7]-1].x[1], nodes[self.connectivity[4]-1].x[1]],
          [nodes[self.connectivity[7]-1].x[2], nodes[self.connectivity[4]-1].x[2]],
      )
      di.plot(
          [nodes[self.connectivity[3]-1].x[0], nodes[self.connectivity[7]-1].x[0]],
          [nodes[self.connectivity[3]-1].x[1], nodes[self.connectivity[7]-1].x[1]],
          [nodes[self.connectivity[3]-1].x[2], nodes[self.connectivity[7]-1].x[2]],
      )
      plt.show()
  # ---------------------------------------------------------------------------
  def adding_surface_partialconstraint(self,id_surf:int,fix:np.ndarray,nodes:list[Node]) -> None:
      n0: Node = nodes[self.surface[id_surf, 0]]
      n1: Node = nodes[self.surface[id_surf, 1]]
      n2: Node = nodes[self.surface[id_surf, 2]]
      n3: Node = nodes[self.surface[id_surf, 3]]
      n0.add_partialconstraint(fix)
      n1.add_partialconstraint(fix)
      n2.add_partialconstraint(fix)
      n3.add_partialconstraint(fix)
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------