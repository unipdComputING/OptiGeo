import  numpy as np
from Node import Node
from Property import Property

"""! @brief Defines the Hexa8 finite element classes."""
class Hexa8:
  """! The Hexa8 class.
  Defines the finite element.
  """
  # ---------------------------------------------------------------------------
  def __init__(self, id: int = 0, connectivity: list[int] = (0, 0, 0, 0, 0, 0, 0, 0), id_prop: int = 0) -> None:
    """! The Hexa8 base class initializer.
    @param id  The id of the element.
    @param connectivity  The connectivity matrix of the element.
    @param id_prop  The id_prop of the element.
    @return  An instance of the Hexa8 class initialized.
    """
    self.id: int = id
    self.connectivity: list[int] = connectivity
    self.id_prop: int = id_prop
    self.TOT_EL_NODES: int = 8
  # ---------------------------------------------------------------------------
  # nodes = [n1, n2, n3, n4, n5, n6, n7, n8]
  def stiffness(self, nodes: list[Node], prop: Property):
    """! Retrieves the element's stiffness matrix.
            @return  Nothing.
            """
    pass
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------