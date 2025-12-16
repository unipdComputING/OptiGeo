import numpy as np
from Node import Node
from Property import Property
from Truss import Truss as Element
from Solver import Liner_Solver

if __name__ == "__main__":
  nodes: list[Node] = [
    Node(id = 100, x = np.array([0.,       0., 0.]), id_pos = 0),
    Node(id =  66, x = np.array([1000., 1000., 0.]), id_pos = 1),
    Node(id =  23, x = np.array([2000.,    0., 0.]), id_pos = 2),
  ]

  nodes[0].set_fix()
  nodes[2].set_fix()
  nodes[1].add_constraint(fix = np.array([0, 0, 1]))

  nodes[1].add_load(np.array([0.0, -20_000., 0.]))

  props: list[Property] = [
    Property(0, 210_000.0, 100.),
    Property(1, 30000., 500.0)
  ]

  elements: list[Element] = [
    Element(0, [100, 66], 0),
    Element(1, [ 66, 23], 0),
  ]

  Liner_Solver(nodes, elements, props)
