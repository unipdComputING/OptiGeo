import numpy as np
from Node import Node
from Property import Property
from Tet4 import Tet4
from Solver import Liner_Solver
import matplotlib as plt
#from Set import Set
#from Space import Space

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

if __name__ == "__main__":
  nodes: list[Node] = [
    Node(id = 1, x = np.array([0.0, 0.0, 0.0])),
    Node(id = 2, x = np.array([1000.0, 0.0, 0.0])),
    Node(id = 3, x = np.array([1000.0, 1000.0, 0.0])),
    Node(id = 4, x = np.array([1000.0, 0.0, 1000.0])),
  ]

  props: list[Property] = [
      Property(1, young=200000.0, poisson=0.25),
  ]

  elements: list = [
      Tet4(2, [1, 2, 3, 4], 1)
  ]

# -----------------------------------------------------------------------------
# Set BCs
# Restraint
  nodes[0].add_constraint(fix=[0, 1, 1], dof=[1, 0, 0])
  nodes[1].add_constraint(fix=[1, 1, 1], dof=[0, 0, 0])
  nodes[2].add_constraint(fix=[1, 0, 1], dof=[0, 1, 0])
  nodes[3].add_constraint(fix=[1, 1, 0], dof=[0, 0, 1])

# Forces
  nodes[3].add_load(np.array([0, 0, 10_000]))

# -----------------------------------------------------------------------------
# Solve
  [a, strain, stress] = Liner_Solver(nodes, elements, props)

print(f"\na = {a}")
print(f"\nepsilon = {strain}")
print(f"\nsigma = {stress}")