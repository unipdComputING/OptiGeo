import numpy as np
from Node import Node
from Property import Property
import matplotlib.pyplot as plt
from Solver import Liner_Solver, assembly
from Tet4 import Tet4 as Element

if __name__ == "__main__":
  nodes: list[Node] = [
        Node(id=1, x=np.array([0., 0., 0.]), id_pos=0),
        Node(id=2, x=np.array([1., 0., 0.]), id_pos=0),
        Node(id=3, x=np.array([0., 1., 0.]), id_pos=0),
        Node(id=4, x=np.array([0., 0., 1.]), id_pos=0),
    ]
#--------------------------------------------------------------------------------------------------

  props: list[Property] = [
    Property(1, 210_000.0, 0.3),
  ]

  elements: list[Element] = [
      Element(1, [2, 3, 1, 4], 1),
  ]
# bottom fix
  nodes[0].set_fix()
  nodes[1].set_fix()
  nodes[2].set_fix()

# top load
  nodes[3].add_load([0, 0, -100])
  K = assembly(nodes, elements, props)
  '''fig1 = plt.figure(figsize=(8, 8))
  di = fig1.add_subplot(111, projection='3d')
  for i in range(len(elements)):
    elements[i].draw_element(di,nodes)
  plt.show()

  plt.spy(K)
  plt.show()
  plt.imshow(K, cmap='coolwarm')
  plt.colorbar(label='K(i,j)')
  plt.xlabel('cols j')
  plt.ylabel('row i')
  plt.title('Matrice di rigidezza globale')
  plt.show()'''

  a = Liner_Solver(nodes, elements, props,100)
  f = K @ a
  print(f"f:{f}")


