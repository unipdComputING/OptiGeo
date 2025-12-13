import Hexa8 as Element
from Node import Node
from Global import *
class Surface:
    def __init__(self,id: int = 0,sur_nodes: list[int] = (0, 0, 0, 0),id_element:int =0,nodes: list[Node]=None) -> None:
        self.id: int = id
        self.sur_nodes: list[int] = sur_nodes
        self.id_element: int = id_element
        for n_id in self.sur_nodes:
            pos = find_pos(nodes, n_id)
            node = nodes[pos]
            if id_element not in node.includedbyelement:
                node.includedbyelement.append(id_element)
            if id not in node.includedbysurface:
                node.includedbysurface.append(id)
            pair = (id_element, id)
            if pair not in node.surfaces:
                node.surfaces.append(pair)
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
