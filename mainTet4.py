import numpy as np
from Node import Node
from Property import Property
import matplotlib.pyplot as plt
#from Truss import Truss as Element
from Solver import Liner_Solver
from Tet4 import Tet4 as Element
if __name__ == "__main__":
  nodes: list[Node] = [
        Node(id=1, x=np.array([   1.,   1.,     1.]), id_pos=0),
        Node(id=2, x=np.array([1.,   -1.,     -1.]), id_pos=1),
        Node(id=3, x=np.array([-1.,1.,     -1.]), id_pos=2),
        Node(id=4, x=np.array([   -1.,-1.,     1.]), id_pos=3),
    ]
#--------------------------------------------------------------------------------------------------

  props: list[Property] = [
    Property(1, 210_000.0, 0.3),
  ]

  elements: list[Element] = [
    Element(1, [1, 2 ,3 ,4 ], 1),
  ]

  elements[0].draw_element(nodes)
  Liner_Solver(nodes, elements, props,100)

