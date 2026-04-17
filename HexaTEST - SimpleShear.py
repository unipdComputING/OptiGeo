import numpy as np
from Node import Node
from Property import Property
from Hexa8 import Hexa8
from Solver import Liner_Solver
#from Set import Set
#from Space import Space

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

if __name__ == "__main__":
  nodes: list[Node] = [
    Node(id = 1, x = np.array([0.0, 0.0, 0.0])),
    Node(id = 2, x = np.array([1000.0, 0.0, 0.0])),
    Node(id = 3, x = np.array([0.0, 1000.0, 0.0])),
    Node(id = 4, x = np.array([1000.0, 1000.0, 0.0])),
    Node(id = 5, x = np.array([0.0, 0.0, 1000.0])),
    Node(id = 6, x = np.array([1000.0, 0.0, 1000.0])),
    Node(id = 7, x = np.array([0.0, 1000.0, 1000.0])),
    Node(id = 8, x = np.array([1000.0, 1000.0, 1000.0]))
  ]

  props: list[Property] = [
      Property(1, young=200000.0, poisson=0.25),
  ]

  elements: list = [
      Hexa8(2, [3,4,8,7,1,2,6,5], 1)
  ]

# -----------------------------------------------------------------------------
# Set BCs
# Restraint
  nodes[0].add_constraint(fix=[1, 1, 1], dof=[0, 0, 0])
  nodes[1].add_constraint(fix=[1, 1, 1], dof=[0, 0, 0])
  nodes[2].add_constraint(fix=[1, 1, 1], dof=[0, 0, 0])
  nodes[3].add_constraint(fix=[1, 1, 1], dof=[0, 0, 0])
  nodes[4].add_constraint(fix=[0, 1, 1], dof=[1, 0, 0])
  nodes[5].add_constraint(fix=[0, 1, 1], dof=[1, 0, 0])
  nodes[6].add_constraint(fix=[0, 1, 1], dof=[1, 0, 0])
  nodes[7].add_constraint(fix=[0, 1, 1], dof=[1, 0, 0])

# Forces
  nodes[4].add_load([-1000, 0, 0])
  nodes[5].add_load([-1000, 0, 0])
  nodes[6].add_load([-1000, 0, 0])
  nodes[7].add_load([-1000, 0, 0])

# -----------------------------------------------------------------------------
# Solve
  [a, K] = Liner_Solver(nodes, elements, props)
  f = K @ a
print(f"a = :{a}")
print(f"f = {f}")