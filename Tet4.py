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
  def computeVol(self,nodes: list[Node]) -> float:
      n0 = nodes[0]
      n1 = nodes[1]
      n2 = nodes[2]
      n3 = nodes[3]

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

      for i in range(4):
          n0: Node = nodes[Index[i,0]]
          n1: Node = nodes[Index[i,1]]
          n2: Node = nodes[Index[i,2]]

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
      if V<0:
          print("Jacobian Negative")

      B = B /(V*6)
      return B
  # ---------------------------------------------------------------------------
  def stiffness(self, nodes: list[Node], prop: Property) -> np.ndarray:

      D = prop.ElasticTensor()
      K = np.zeros((12, 12))
      B = self.build_B(nodes)
      V = self.computeVol(nodes)

      for i in range(4):
          for j in range(4):
            K[3*i:3*i+3,3*j:3*j+3] += B[0:6, 3*i:3*i+3].T @ D @ B[0:6, 3*j:3*j+3] * V

      return K
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

      fig = plt.figure(figsize=(8, 8))
      di = fig.add_subplot(111, projection='3d')
      di.scatter(x, y, z)
      for i in self.connectivity:
          di.text(nodes[find_pos(nodes,i)].x[0], nodes[find_pos(nodes,i)].x[1], nodes[find_pos(nodes,i)].x[2], str(nodes[i-1].id), fontsize=9)
      comb_plot = np.array([
          [1, 2, 3],
          [0, 2, 3],
          [0, 1, 3],
          [0, 1, 2]
      ])
      for i in range(0, 3):
          for j in range(0, 3):
            di.plot(
              [nodes[find_pos(nodes,self.connectivity[i])].x[0], nodes[find_pos(nodes,self.connectivity[comb_plot[i,j]])].x[0]],
              [nodes[find_pos(nodes,self.connectivity[i])].x[1], nodes[find_pos(nodes,self.connectivity[comb_plot[i,j]])].x[1]],
             [nodes[find_pos(nodes,self.connectivity[i])].x[2], nodes[find_pos(nodes,self.connectivity[comb_plot[i,j]])].x[2]],
              color='black')
      di.set_title((f"Elemento Tetra4: {self.id}"))
      di.set_xlabel("Coordinata x")
      di.set_ylabel("Coordinata y")
      di.set_zlabel("Coordinata z")
      plt.show()