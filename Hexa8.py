import  numpy as np
from matplotlib.figure import Figure
from Surface import Surface
from Global import *
from Node import Node
from Property import Property
import matplotlib.pyplot as plt
class Hexa8:
  # ---------------------------------------------------------------------------
  def __init__(self, id: int = 0, connectivity: list[int] = (0, 0, 0, 0, 0, 0, 0, 0), id_prop: int = 0,nodes: list[Node]=None) -> None:
    self.id: int = id
    self.connectivity: list[int] = connectivity
    self.id_prop: int = id_prop
    self.TOT_EL_NODES: int = 8
    self.surface:list[Surface] = [
          Surface(1, [self.connectivity[0], self.connectivity[1], self.connectivity[2], self.connectivity[3]], id,nodes),
          Surface(2, [self.connectivity[4], self.connectivity[5], self.connectivity[6], self.connectivity[7]], id,nodes),
          Surface(3, [self.connectivity[0], self.connectivity[1], self.connectivity[5], self.connectivity[4]], id,nodes),
          Surface(4, [self.connectivity[3], self.connectivity[2], self.connectivity[6], self.connectivity[7]], id,nodes),
          Surface(5, [self.connectivity[0], self.connectivity[4], self.connectivity[7], self.connectivity[3]], id,nodes),
          Surface(6, [self.connectivity[1], self.connectivity[2], self.connectivity[6], self.connectivity[5]], id,nodes),
  ]
    """"
    self.surface = np.array([
        [self.connectivity[0], self.connectivity[1], self.connectivity[2], self.connectivity[3]],
        [self.connectivity[4], self.connectivity[5], self.connectivity[6], self.connectivity[7]],
        [self.connectivity[0], self.connectivity[1], self.connectivity[5], self.connectivity[4]],
        [self.connectivity[3], self.connectivity[2], self.connectivity[6], self.connectivity[7]],
        [self.connectivity[0], self.connectivity[4], self.connectivity[7], self.connectivity[3]],
        [self.connectivity[1], self.connectivity[2], self.connectivity[6], self.connectivity[5]],
    ])
    """
    #        7 ──────────── 6
    #      / |            / |
    #     4 ──────────── 5  |
    #     |  |           |  |
    #     |  |           |  |
    #     |  3 ──────────── 2
    #     | /            | /
    #     0 ──────────── 1

  # ---------------------------------------------------------------------------
  def add_surface_stress(self, nodes: list, id_surf: int,
                         stress_value: np.ndarray = np.zeros(3)) -> None:
      """
      n0: Node = nodes[find_pos(nodes,self.surface[id_surf, 0])]
      n1: Node = nodes[find_pos(nodes,self.surface[id_surf, 1])]
      n2: Node = nodes[find_pos(nodes,self.surface[id_surf, 2])]
      n3: Node = nodes[find_pos(nodes,self.surface[id_surf, 3])]
      """
      n0: Node = nodes[find_pos(nodes,self.surface[id_surf].sur_nodes[0])]
      n1: Node = nodes[find_pos(nodes,self.surface[id_surf].sur_nodes[1])]
      n2: Node = nodes[find_pos(nodes,self.surface[id_surf].sur_nodes[2])]
      n3: Node = nodes[find_pos(nodes,self.surface[id_surf].sur_nodes[3])]
      v01 = n0.direction(n1)
      v02 = n0.direction(n2)
      A1 = 0.5 * np.linalg.norm(np.cross(v01, v02))

      v02b = n0.direction(n2)
      v03 = n0.direction(n3)
      A2 = 0.5 * np.linalg.norm(np.cross(v02b, v03))

      Area_surf = A1 + A2

      surf_nodes = [n0, n1, n2, n3]
      for node in surf_nodes:
          node.add_load(stress_value * Area_surf / 4)

  # ---------------------------------------------------------------------------
  def compute_Vol(self, nodes: list[Node]) -> float:
      # Calcolo del volume decomponendo in 6 tetraedri

      index_mat = np.array([ # matrice di combinazione per definire iterativamente gli esaedri

          [self.connectivity[0], self.connectivity[1], self.connectivity[2], self.connectivity[6]],
          [self.connectivity[0], self.connectivity[2], self.connectivity[3], self.connectivity[6]],
          [self.connectivity[0], self.connectivity[4], self.connectivity[5], self.connectivity[6]],
          [self.connectivity[0], self.connectivity[5], self.connectivity[1], self.connectivity[6]],
          [self.connectivity[0], self.connectivity[3], self.connectivity[7], self.connectivity[6]],
          [self.connectivity[0], self.connectivity[7], self.connectivity[4], self.connectivity[6]],

      ])
      vol = np.zeros(6)
      for i in range (6):
          n0 = nodes[find_pos(nodes,index_mat[i,0])]
          n1 = nodes[find_pos(nodes,index_mat[i,1])]
          n2 = nodes[find_pos(nodes,index_mat[i,2])]
          n3 = nodes[find_pos(nodes,index_mat[i,3])]

          a = n3.direction(n0)
          b = n3.direction(n1)
          c = n3.direction(n2)
          axb = np.cross(a, b)
          vol[i] = 1 / 6 * axb @ c
      tot_vol = np.sum(vol)
      return tot_vol

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
  def stiffness(self, nodes: list[Node], prop: Property) -> np.ndarray:

      coords = np.array([n.x for n in nodes])

      D = prop.ElasticTensor()

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
  def draw_hex8_element(self,figure: plt.Figure, nodes: list, color="black", show_node_id=True):

      if figure.axes:
          ax = figure.axes[0]
      else:
          ax = figure.add_subplot(111, projection='3d')

      node_by_id = {n.id: n for n in nodes}
      pts = [node_by_id[nid].x for nid in self.connectivity]

      xs = [p[0] for p in pts]
      ys = [p[1] for p in pts]
      zs = [p[2] for p in pts]
      ax.scatter(xs, ys, zs)

      edges = [
          (0, 1), (1, 2), (2, 3), (3, 0),
          (4, 5), (5, 6), (6, 7), (7, 4),
          (0, 4), (1, 5), (2, 6), (3, 7)
      ]

      for i, j in edges:
          ax.plot([pts[i][0], pts[j][0]],
                  [pts[i][1], pts[j][1]],
                  [pts[i][2], pts[j][2]],
                  color=color)

      if show_node_id:
          for nid in self.connectivity:
              p = node_by_id[nid].x
              ax.text(p[0], p[1], p[2], str(nid), fontsize=8, color=color)
  # ---------------------------------------------------------------------------
  def adding_surface_partialconstraint(self,id_surf:int,fix:np.ndarray,nodes:list[Node]) -> None:
      """
      n0: Node = nodes[find_pos(nodes,self.surface[id_surf, 0])]
      n1: Node = nodes[find_pos(nodes,self.surface[id_surf, 1])]
      n2: Node = nodes[find_pos(nodes,self.surface[id_surf, 2])]
      n3: Node = nodes[find_pos(nodes,self.surface[id_surf, 3])]
      """
      n0: Node = nodes[find_pos(nodes,self.surface[id_surf].sur_nodes[0])]
      n1: Node = nodes[find_pos(nodes,self.surface[id_surf].sur_nodes[1])]
      n2: Node = nodes[find_pos(nodes,self.surface[id_surf].sur_nodes[2])]
      n3: Node = nodes[find_pos(nodes,self.surface[id_surf].sur_nodes[3])]
      n0.add_partialconstraint(fix)
      n1.add_partialconstraint(fix)
      n2.add_partialconstraint(fix)
      n3.add_partialconstraint(fix)
  # ---------------------------------------------------------------------------
  def find_ele_id(self, ele_nodes: list[int], nodes: list[Node]) -> int:
      e1: list[int] = nodes[find_pos(nodes, ele_nodes[0])].includedbyelement
      e2: list[int] = nodes[find_pos(nodes, ele_nodes[1])].includedbyelement
      e3: list[int] = nodes[find_pos(nodes, ele_nodes[2])].includedbyelement
      e4: list[int] = nodes[find_pos(nodes, ele_nodes[3])].includedbyelement
      commonlist = set(e1) & set(e2) & set(e3) & set(e4)
      if len(commonlist) > 1:
          print(f'Error:there might be overlap between {len(commonlist)} elements')
          return -1
      else:
          common = commonlist[0]
          return common

  # ---------------------------------------------------------------------------