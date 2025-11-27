import numpy as np
from Node import Node
from Property import Property
import matplotlib.pyplot as plt
#from Truss import Truss as Element
from Solver import Liner_Solver
from Hexa8 import Hexa8 as Element
if __name__ == "__main__":
  nodes: list[Node] = [
        Node(id=1, x=np.array([   0.,   0.,     0.]), id_pos=0),
        Node(id=2, x=np.array([1.,   0.,     0.]), id_pos=1),
        Node(id=3, x=np.array([1.,1.,     0.]), id_pos=2),
        Node(id=4, x=np.array([   0.,1.,     0.]), id_pos=3),
        Node(id=5, x=np.array([0., 0., 1.]), id_pos=4),
        Node(id=6, x=np.array([1., 0., 1.]), id_pos=5),
        Node(id=7, x=np.array([1., 1., 1.]), id_pos=6),
        Node(id=8, x=np.array([0., 1., 1.]), id_pos=7),
  ]
#--------------------------------------------------------------------------------------------------
  nodes[0].add_partialconstraint(fix=np.array([1, 0, 0]))
  nodes[3].add_partialconstraint(fix=np.array([1, 0, 0]))
  nodes[7].add_partialconstraint(fix=np.array([1, 0, 0]))
  nodes[4].add_partialconstraint(fix=np.array([1, 0, 0]))

  nodes[0].add_partialconstraint(fix=np.array([0, 0, 1]))
  nodes[1].add_partialconstraint(fix=np.array([0, 0, 1]))
  nodes[2].add_partialconstraint(fix=np.array([0, 0, 1]))
  nodes[3].add_partialconstraint(fix=np.array([0, 0, 1]))

  nodes[0].add_partialconstraint(fix=np.array([0, 1, 0]))
  nodes[1].add_partialconstraint(fix=np.array([0, 1, 0]))
  nodes[5].add_partialconstraint(fix=np.array([0, 1, 0]))
  nodes[4].add_partialconstraint(fix=np.array([0, 1, 0]))
  props: list[Property] = [
    Property(1, 210_000.0, 0.3),
  ]

  elements: list[Element] = [
    Element(1, [1, 2 ,3 ,4 ,5 ,6 ,7 ,8 ], 1),
  ]
  elements[0].draw_element(nodes)
  elements[0].add_surface_stress( nodes, 1, np.array([0., 0., 1000]))


  Liner_Solver(nodes, elements, props,100)
  elements[0].draw_element(nodes)
