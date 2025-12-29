import numpy as np
from Node import Node
from Property import Property
from Truss import Truss
from Hexa8 import Hexa8
from Solver import Liner_Solver
from Set import Set
from Space import Space

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def start(space: Space) -> None:
  space.update(update_func=start, interval_ms=60)
# -----------------------------------------------------------------------------

if __name__ == "__main__":
  nodes: list[Node] = [
    Node(id = 1, x = np.array([0.,       0.,    0.])),
    Node(id = 2, x = np.array([100.,     0.,    0.])),
    Node(id = 3, x = np.array([100.,   100.,    0.])),
    Node(id = 4, x = np.array([  0.,   100.,    0.])),
    Node(id = 5, x = np.array([0.,       0.,  100.])),
    Node(id = 6, x = np.array([100.,     0.,  100.])),
    Node(id = 7, x = np.array([100.,   100.,  100.])),
    Node(id = 8, x = np.array([  0.,   100.,  100.])),

    Node(id = 9, x = np.array([0.,       0., -100.])),
    Node(id =10, x = np.array([100.,     0., -100.])),
    Node(id =11, x = np.array([100.,   100., -100.])),
    Node(id =12, x = np.array([  0.,   100., -100.])),
  ]

  constrain_set: Set = Set('fix', (9, 10, 11, 12))
  constrain_set.fix(nodes)

  load_set: Set = Set('load', (5, 6, 7, 8))
  load_set.add_loads(nodes, np.array([0.0, 0.0, -20_000.0]))

  props: list[Property] = [
    Property(0, young = 210_000.0, area = 100., poisson = 0.2),
    Property(1, young = 30000., area = 500.0)
  ]

  elements: list = [
    Hexa8(1, [1, 2, 3, 4, 5, 6, 7, 8], 0),
    Truss( 2, [ 1,  9], 1),
    Truss( 3, [ 2, 10], 1),
    Truss( 4, [ 3, 11], 1),
    Truss( 5, [ 4, 12], 1),
    Truss( 6, [ 1, 10], 1),
    Truss( 7, [ 2, 11], 1),
    Truss( 8, [ 3, 12], 1),
    Truss( 9, [ 4,  9], 1),
  ]


  Liner_Solver(nodes, elements, props)

  space = Space(width=1200, height=1200)
  space.add_elements(elements=elements, nodes=nodes)

  start(space)
