import numpy as np
from  Global import *
from Node import Node
from Element import Element
from Property import Property
from Vtk import save_vtk

# -----------------------------------------------------------------------------
def Liner_Solver(nodes: list[Node] = None, elements: list[Element] = None, props: list[Property] = None) -> None:

  if nodes is None or elements is None or props is None:
    return

  # 1. stiffness assembly
  K: np.ndarray = assembly(nodes, elements, props)
  # 2. apply bcs
  (a, fix) = apply_bcs(nodes)
  # 3. loads assembly
  f: np.ndarray = loads_assembly(nodes, K, a)
  # 4. solver
  solver(nodes, K, a, f, fix)
  # 5. outputs
  ip_offset: list[int] = build_offset(elements)
  rows: int = ip_offset[-1]
  strain: np.ndarray = np.zeros((rows, DIM_TENSOR), dtype=float)
  stress: np.ndarray = np.zeros((rows, DIM_TENSOR), dtype=float)
  statev: np.ndarray = np.zeros((rows, TOT_STATEV), dtype=float)
  updates(elements, nodes, props, ip_offset, strain, stress, statev)
  save_vtk("test.vtk", nodes, elements, ip_offset, strain, stress, statev)

  return
# -----------------------------------------------------------------------------
def assembly(nodes: list[Node], elements: list[Element], props: list[Property]) -> np.ndarray:
  DIM_PROBLEM: int = len(nodes) * DIM_DOF
  K: np.ndarray = np.zeros((DIM_PROBLEM, DIM_PROBLEM))
  for element in elements:
    # id_n1: int = element.connectivity[0]
    # id_n2: int = element.connectivity[1]
    TOT_EL_NODES: int = element.TOT_EL_NODES
    # n1: Node = nodes[element.connectivity[0]]
    # n2: Node = nodes[element.connectivity[1]]
    # prop: Property = props[element.id_prop]
    # elK: np = element.stiffness(n1, n2, prop)

    nodes_position: list[int] = element.get_nodes_position(nodes)
    pos_prop = find_pos(props, element.id_prop)
    if pos_prop < 0:
      print(f"ERROR in EL: {element.id}: properties {element.id_prop} not defined")
      quit()
    el_nodes: list[Node] = get_el_nodes(element.connectivity, nodes)
    elK: np.ndarray = element.stiffness(el_nodes,
                                        props[pos_prop])
    for node_row in range(TOT_EL_NODES):
      pos_row: int = nodes_position[node_row]
      for node_col in range(TOT_EL_NODES):
        pos_col: int = nodes_position[node_col]
        for i in range(DIM_DOF):
          row: int = DIM_DOF * pos_row + i
          el_row: int = DIM_DOF * node_row + i
          for j in range(DIM_DOF):
            col: int = DIM_DOF * pos_col + j
            el_col: int = DIM_DOF * node_col + j
            K[row, col] += elK[el_row, el_col]
  return K
# -----------------------------------------------------------------------------
def apply_bcs(nodes: list[Node]) -> tuple[np.ndarray, np.ndarray]:
  DIM_PROBLEM: int = len(nodes) * DIM_DOF
  fix: np.ndarray = np.zeros(DIM_PROBLEM)
  a: np.ndarray = np.zeros(DIM_PROBLEM)
  cont: int = 0
  for node in nodes:
    for i in range(DIM_DOF):
      fix[cont] = node.fix[i]
      a[cont] = node.dof[i]
      cont += 1
  return (a, fix)
# -----------------------------------------------------------------------------
def loads_assembly(nodes: list[Node], K: np.ndarray, a: np.ndarray) -> np.ndarray:
  DIM_PROBLEM: int = len(nodes) * DIM_DOF
  f: np.ndarray = np.zeros(DIM_PROBLEM)
  cont: int = 0
  for node in nodes:
    for i in range(DIM_DOF):
      f[cont] = node.load[i]
      cont += 1
  return f - K @ a
# -----------------------------------------------------------------------------
def solver(nodes: list[Node], K: np.ndarray, a: np.ndarray, f: np.ndarray, fix: np.ndarray) -> None:
  penalty: float = np.max(K) * 1000_000_000.0
  DIM_PROBLEM: int = len(nodes) * DIM_DOF
  for i in range(DIM_PROBLEM):
    K[i, i] += fix[i] * penalty

  u: np.ndarray = np.linalg.solve(K, f)
  u[:] *= 1 - fix[:]
  a += u

  # for i in range(DIM_PROBLEM):
  #   K[i, i] -= fix[i] * penalty  

  # ff = K @ a

  cont: int = 0
  for node in nodes:
    for i in range(DIM_DOF):
      node.dof[i] = a[cont]
      cont += 1
# -----------------------------------------------------------------------------
def build_offset(elements: list[Element]) -> list[int]:
  '''
  Vettore che tiene conto dell'accumulo di punti di integrazione.
  Ha dimensione tot_elements + 1
  '''
  offset: list[int] = [0]
  for i, element in enumerate(elements):
      offset.append(offset[i] + element.N_GAUSS)
  return offset
# -----------------------------------------------------------------------------
def updates(elements: list[Element], nodes: list[Node], props: list[Property], 
            offset: list[int], strain: np.ndarray, stress: np.ndarray, statev: np.ndarray)-> None:
    
    cont: int = 0

    for i, elem in enumerate(elements):
      pos_prop: int = find_pos(props, elem.id_prop)
      prop: Property = props[pos_prop]
      el_nodes: list[Node] = get_el_nodes(elem.connectivity, nodes)
      el_strain: np.ndarray = strain[offset[i] : offset[i + 1], :]
      el_stress: np.ndarray = stress[offset[i] : offset[i + 1], :]
      el_statev: np.ndarray = statev[offset[i] : offset[i + 1], :]
      elem.updates(el_nodes, prop, el_strain, el_stress, el_statev)
      '''
      NOTA: qui stiamo facendo un passaggio per riferimento dai vettori globali: strain, stress, statev
      a quelli locagli degli elementi el_... questo implica che se modifichiamo i vettori locali
      anche quelli globali verranno aggiornati e quindi non c'è bisogno di aggiornare in modo 
      esplicito i vettori globali.
      Facciamo la stessa cosa anche dentro elem.updates()
      '''
      
    return
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------