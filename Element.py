import  numpy as np
from Global import *
from Node import Node
from Property import Property

'''
                <1>  <2>
connectivity = [(i), (j)]
'''


class Element:
  # ---------------------------------------------------------------------------
  def __init__(self, id: int = 0, connectivity: list[int] = (0, 0), id_prop: int = 0) -> None:
    self.id: int = id
    self.connectivity: list[int] = connectivity
    self.id_prop: int = id_prop
    self.TOT_EL_NODES: int = 2
  # ---------------------------------------------------------------------------
  def stiffness(self, n1: Node, n2: Node, prop: Property) -> np.ndarray:
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
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------