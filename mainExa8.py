import numpy as np
from Node import Node
from Property import Property
import matplotlib.pyplot as plt
#from Truss import Truss as Element
from Solver import Liner_Solver
from Hexa8 import Hexa8 as Element
from Global import *
if __name__ == "__main__":
  nodes: list[Node] = [
      Node(id=1, x=np.array([0., 0., 0.]), id_pos=0),
      Node(id=2, x=np.array([1., 0., 0.]), id_pos=1),
      Node(id=3, x=np.array([2., 0., 0.]), id_pos=2),
      Node(id=4, x=np.array([0., 1., 0.]), id_pos=3),
      Node(id=5, x=np.array([1., 1., 0.]), id_pos=4),
      Node(id=6, x=np.array([2., 1., 0.]), id_pos=5),
      Node(id=7, x=np.array([0., 2., 0.]), id_pos=6),
      Node(id=8, x=np.array([1., 2., 0.]), id_pos=7),
      Node(id=9, x=np.array([2., 2., 0.]), id_pos=8),
      Node(id=10, x=np.array([0., 0., 1.]), id_pos=9),
      Node(id=11, x=np.array([1., 0., 1.]), id_pos=10),
      Node(id=12, x=np.array([2., 0., 1.]), id_pos=11),
      Node(id=13, x=np.array([0., 1., 1.]), id_pos=12),
      Node(id=14, x=np.array([1., 1., 1.]), id_pos=13),
      Node(id=15, x=np.array([2., 1., 1.]), id_pos=14),
      Node(id=16, x=np.array([0., 2., 1.]), id_pos=15),
      Node(id=17, x=np.array([1., 2., 1.]), id_pos=16),
      Node(id=18, x=np.array([2., 2., 1.]), id_pos=17),
      Node(id=19, x=np.array([0., 0., 2.]), id_pos=18),
      Node(id=20, x=np.array([1., 0., 2.]), id_pos=19),
      Node(id=21, x=np.array([2., 0., 2.]), id_pos=20),
      Node(id=22, x=np.array([0., 1., 2.]), id_pos=21),
      Node(id=23, x=np.array([1., 1., 2.]), id_pos=22),
      Node(id=24, x=np.array([2., 1., 2.]), id_pos=23),
      Node(id=25, x=np.array([0., 2., 2.]), id_pos=24),
      Node(id=26, x=np.array([1., 2., 2.]), id_pos=25),
      Node(id=27, x=np.array([2., 2., 2.]), id_pos=26),

  ]
#--------------------------------------------------------------------------------------------------

  props: list[Property] = [
    Property(1, 210_000.0, 0.3),
  ]

  elements: list[Element] = [
      Element(1, [1, 2, 5, 4, 10, 11, 14, 13], 1,nodes),
      Element(2, [2, 3, 6, 5, 11, 12, 15, 14], 1,nodes),
      Element(3, [4, 5, 8, 7, 13, 14, 17, 16], 1,nodes),
      Element(4, [5, 6, 9, 8, 14, 15, 18, 17], 1,nodes),
      Element(5, [10, 11, 14, 13, 19, 20, 23, 22], 1,nodes),
      Element(6, [11, 12, 15, 14, 20, 21, 24, 23], 1,nodes),
      Element(7, [13, 14, 17, 16, 22, 23, 26, 25], 1,nodes),
      Element(8, [14, 15, 18, 17, 23, 24, 27, 26], 1,nodes),
  ]
#selecting nodes
  x_nodes: list[tuple[int, int]] = []
  for n in nodes:
      if n.x[0] == 0:
          for (e_id, s_id) in n.surfaces:
              x_nodes.append((e_id, s_id))

  y_nodes: list[tuple[int, int]] = []
  for n in nodes:
      if n.x[1] == 0:
          for (e_id, s_id) in n.surfaces:
              y_nodes.append((e_id, s_id))

  z_nodes: list[tuple[int, int]] = []
  for n in nodes:
      if n.x[2] == 0:
          for (e_id, s_id) in n.surfaces:
              z_nodes.append((e_id, s_id))

  load_nodes: list[tuple[int, int]] = []
  for n in nodes:
      if n.x[2] == 2:
          for (e_id, s_id) in n.surfaces:
              load_nodes.append((e_id, s_id))
#convert nodes_set to surface_id_set


  load_surf_id_list: list[tuple[int, int]] = selecting_surface_from_nodesset(4, load_nodes)
  x_surf_id_list: list[tuple[int, int]] = selecting_surface_from_nodesset(4, x_nodes)
  y_surf_id_list: list[tuple[int, int]] = selecting_surface_from_nodesset(4, y_nodes)
  z_surf_id_list: list[tuple[int, int]] = selecting_surface_from_nodesset(4, z_nodes)

  for (e_id,s_id) in x_surf_id_list:
    pos_el=find_pos(elements,e_id)
    pos_su=find_pos(elements[pos_el].surface,s_id)
    elements[pos_el].adding_surface_partialconstraint(pos_su, np.array([1, 0, 0]), nodes)
  for (e_id,s_id) in y_surf_id_list:
    pos_el=find_pos(elements,e_id)
    pos_su=find_pos(elements[pos_el].surface,s_id)
    elements[pos_el].adding_surface_partialconstraint(pos_su, np.array([0, 1, 0]), nodes)
  for (e_id,s_id) in z_surf_id_list:
    pos_el=find_pos(elements,e_id)
    pos_su=find_pos(elements[pos_el].surface,s_id)
    elements[pos_el].adding_surface_partialconstraint(pos_su, np.array([0, 0, 1]), nodes)

#applying uniformly distributed load:

  for (e_id,s_id) in load_surf_id_list:
    pos_el=find_pos(elements,e_id)
    pos_su=find_pos(elements[pos_el].surface,s_id)
    elements[pos_el].add_surface_stress(nodes, pos_su, np.array([0., 0., 1000.]))

  fig1 = plt.figure(figsize=(8, 8))
  elements[0].draw_hex8_element(fig1, nodes, color="black")
  for i in range(1, len(elements)):
    elements[i].draw_hex8_element(fig1, nodes, color="black")
  plt.show()
#  elements[0].add_surface_stress(nodes,1, np.array([0., 0., 1000.]))
  elements[0].compute_Vol(nodes)
  Liner_Solver(nodes, elements, props,1)
  fig2 = plt.figure(figsize=(8, 8))
  elements[0].draw_hex8_element(fig2, nodes, color="black")
  for i in range(1, len(elements)):
    elements[i].draw_hex8_element(fig2, nodes, color="black")
  plt.show()


#Analytical solution
  E=210_000
  poisson=0.3
  pressure = 1000
  epsilon = pressure / E
  deltaH =  2 * epsilon
  altezza_deformata = 2-deltaH
  print(f'H deformata = {altezza_deformata}')
  print(f'L deformata = {poisson * deltaH}')

  Toll = 0.000001
  a= nodes[find_pos(nodes,25)].x[2]
  b = nodes[find_pos(nodes, 25)].x[1]
  if a-altezza_deformata<Toll:
      print(f'Analysis successfully completed (errore spostamento in direzione z uguale a {a-altezza_deformata})')
  if b-poisson * deltaH-2<Toll:
      print(f'Analysis successfully completed (errore spostamento in direzione x e y uguale a {b-poisson * deltaH-2})')