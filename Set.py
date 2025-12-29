import numpy as np
from Node import Node
from Global import *

class Set:
  """! @brief Defines the Set classes."""
  # ---------------------------------------------------------------------------
  def __init__(self, name: str = "set", list_of: tuple[int, ...] = None, type: str = 'n') -> None:
    """! The Set base class initializer.
    @param name Set name definition (default = set).
    @param list_of List od integer id to define the set (default = None).
    @param type Type of set: 'n' -> nodes; 'e' -> elements, 's' -> element faces.
    @return  An instance of the Set class initialized.
    """
    self.name = name
    self.list: tuple[int, ...] = list_of
    self.type = type
    return
  # ---------------------------------------------------------------------------
  def fix(self, nodes: list[Node]) -> None:
    if self.type != 'n':
      return
    for id in self.list:
      pos = find_pos(nodes, id)
      nodes[pos].set_fix()
  # ---------------------------------------------------------------------------
  def add_loads(self, nodes: list[Node], load: np.ndarray = None) -> None:
    if self.type != 'n':
      return
    if load is None:
      return
    for id in self.list:
      pos = find_pos(nodes, id)
      nodes[pos].add_load(load)
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  