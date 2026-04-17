import numpy as np
from Node import Node
from Property import Property
from Hexa8 import Hexa8
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
      Hexa8(2, [1,2,4,3,5,6,8,7], 1)
  ]

# -----------------------------------------------------------------------------
# Set BCs
# Restraint
  nodes[0].add_constraint(fix=[1, 0, 1], dof=[0, 1, 0])
  nodes[1].add_constraint(fix=[0, 0, 1], dof=[1, 1, 0])
  nodes[2].add_constraint(fix=[1, 1, 1], dof=[0, 0, 0])
  nodes[3].add_constraint(fix=[0, 1, 1], dof=[1, 0, 0])
  nodes[4].add_constraint(fix=[1, 0, 0], dof=[0, 1, 1])
  nodes[6].add_constraint(fix=[1, 1, 0], dof=[0, 0, 1])
  nodes[7].add_constraint(fix=[0, 1, 0], dof=[1, 0, 1])

# Forces
  nodes[4].add_load([0, 0, 250_000])
  nodes[5].add_load([0, 0, 250_000])
  nodes[6].add_load([0, 0, 250_000])
  nodes[7].add_load([0, 0, 250_000])

# -----------------------------------------------------------------------------
# Solve
  # Solve
  [a, strain, stress] = Liner_Solver(nodes, elements, props)

print(f"\na = {a}")
print(f"\nepsilon = {strain}")
print(f"\nsigma = {stress}")
