import numpy as np
from Global import *
from Node import Node
from Property import Property
import matplotlib.pyplot as plt

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
    ])
  # ---------------------------------------------------------------------------
  def add_surface_stress(self, nodes: list, id_surf: int,
                         stress_value: np.ndarray = np.zeros(3)) -> None:
      n0: Node = nodes[self.surface[id_surf, 0]]
      n1: Node = nodes[self.surface[id_surf, 1]]
      n2: Node = nodes[self.surface[id_surf, 2]]

      a=n0.dist(n1)
      b=n0.dist(n2)
      c=n1.dist(n2)
      p=a+b+c
      Area_surf = np.sqrt(p*(p-a)*(p-b)*(p-c))
      surf_nodes = [n0, n1, n2]
      for node in surf_nodes:
          node.add_load(stress_value * Area_surf / 3)
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
  def computeVol(self,nodes: list[Node]) -> float:
      el_nodes = get_el_nodes(self.connectivity,nodes)
      n0 = el_nodes[0]
      n1 = el_nodes[1]
      n2 = el_nodes[2]
      n3 = el_nodes[3]

      a = n3.direction(n0)
      b = n3.direction(n1)
      c = n3.direction(n2)
      axb = np.cross(a, b)
      Vol = 1/6 * axb @ c
      return Vol

  # ---------------------------------------------------------------------------
  def build_B(self,nodes: list[Node]) -> np.ndarray:
      B = np.zeros((6, 12))
      Index = np.array([
          [1, 2, 3],
          [0, 2, 3],
          [0, 1, 3],
          [0, 1, 2],
      ])
      el_nodes = get_el_nodes(self.connectivity, nodes)

      for i in range(4):
          n0: Node = el_nodes[Index[i,0]]
          n1: Node = el_nodes[Index[i,1]]
          n2: Node = el_nodes[Index[i,2]]

          bmat = np.array([
              [1, n0.x[1], n0.x[2]],
              [1, n1.x[1], n1.x[2]],
              [1, n2.x[1], n2.x[2]],
          ])
          b = -np.linalg.det(bmat)

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
          d = -np.linalg.det(dmat)

          B[0, i*3:i*3+3] = [b, 0, 0]
          B[1, i*3:i*3+3] = [0, c, 0]
          B[2, i*3:i*3+3] = [0, 0, d]
          B[3, i*3:i*3+3] = [c, b, 0]
          B[4, i*3:i*3+3] = [d, 0, b]
          B[5, i*3:i*3+3] = [0, d, c]

      V = self.computeVol(nodes)
      B = B * V/6
      return B

  # ---------------------------------------------------------------------------
  def stiffness(self, nodes: list[Node], prop: Property) -> np.ndarray:
      el_nodes = get_el_nodes(self.connectivity, nodes)
      coords = np.array([n.x for n in el_nodes])

      E = prop.young
      nu = prop.poisson
      D = self.D_matrix(E, nu)
      K = np.zeros((12, 12))
      B = self.build_B(nodes)

      for i in range(4):
          for j in range(4):
            K += B[0:5, 3*i:3*i+3].T @ D @ B[0:5, 3*j:3*j+3]


  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  def adding_surface_partialconstraint(self,id_surf:int,fix:np.ndarray,nodes:list[Node]) -> None:
      n0: Node = nodes[self.surface[id_surf, 0]]
      n1: Node = nodes[self.surface[id_surf, 1]]
      n2: Node = nodes[self.surface[id_surf, 2]]
      n0.add_partialconstraint(fix)
      n1.add_partialconstraint(fix)
      n2.add_partialconstraint(fix)
  # ---------------------------------------------------------------------------
  def draw_element(self, nodes: list[Node]) -> None:
      x = [nodes[n-1].x[0] for n in self.connectivity]
      y = [nodes[n-1].x[1] for n in self.connectivity]
      z = [nodes[n-1].x[2] for n in self.connectivity]

      fig = plt.figure(figsize=(10, 6))
      di = fig.add_subplot(111, projection='3d')
      di.scatter(x, y, z)