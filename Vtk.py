import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from Node import Node
from Element import Element

# -----------------------------------------------------------------------------
#def draw_mesh(nodes: list[Node] = None, elements: list[Element] = None) -> None:
def build_mesh_actors(nodes_df, elements_df) -> list:
  actors = []

  # Prima colonna = id nodo
  node_id_col = nodes_df.columns[0]  # "id"
  node_index = {str(v): i for i, v in enumerate(nodes_df[node_id_col])}

  # Coordinate = colonne x, y, z
  coord_cols = ["x", "y", "z"]

  points = vtk.vtkPoints()
  for _, row in nodes_df.iterrows():
      points.InsertNextPoint(*[float(row[c]) for c in coord_cols])

  # Nodi come sfere
  vertices = vtk.vtkCellArray()
  for i in range(points.GetNumberOfPoints()):
      vertex = vtk.vtkVertex()
      vertex.GetPointIds().SetId(0, i)
      vertices.InsertNextCell(vertex)

  points_polydata = vtk.vtkPolyData()
  points_polydata.SetPoints(points)
  points_polydata.SetVerts(vertices)
  points_mapper = vtk.vtkPolyDataMapper()
  points_mapper.SetInputData(points_polydata)
  points_actor = vtk.vtkActor()
  points_actor.SetMapper(points_mapper)
  points_actor.GetProperty().SetPointSize(5)
  points_actor.GetProperty().SetColor(1.0, 0.0, 0.0)
  points_actor.GetProperty().SetRenderPointsAsSpheres(True)
  actors.append(points_actor)

  if elements_df is not None and len(elements_df) > 0:
      # Colonne che iniziano con "NODE" = nodi dell'elemento
      element_node_cols = [c for c in elements_df.columns if c.upper().startswith("NODE")] #Boh sta roba è da cambiare
      n_nodes = len(element_node_cols)

      match n_nodes:
          case 2: vtk_cell_type, cell_factory = vtk.VTK_LINE,       vtk.vtkLine
          case 3: vtk_cell_type, cell_factory = vtk.VTK_TRIANGLE,   vtk.vtkTriangle
          case 4: vtk_cell_type, cell_factory = vtk.VTK_TETRA,      vtk.vtkTetra
          case 8: vtk_cell_type, cell_factory = vtk.VTK_HEXAHEDRON, vtk.vtkHexahedron
          case _:
              print(f"Tipo elemento con {n_nodes} nodi non supportato")
              return actors

      cells = vtk.vtkCellArray()
      for _, row in elements_df.iterrows():
          cell = cell_factory()
          valid = True
          for i, col in enumerate(element_node_cols):
              nid = str(row[col]).strip()
              if nid in node_index:
                  cell.GetPointIds().SetId(i, node_index[nid])
              else:
                  print(f"Nodo {nid} non trovato in node_index")
                  valid = False
                  break
          if valid:
              cells.InsertNextCell(cell)

      ug = vtk.vtkUnstructuredGrid()
      ug.SetPoints(points)
      ug.SetCells(vtk_cell_type, cells)

      mapper = vtk.vtkDataSetMapper()
      mapper.SetInputData(ug)

      actor = vtk.vtkActor()
      actor.SetMapper(mapper)
      actor.GetProperty().SetColor(0.2, 0.6, 1.0)
      actor.GetProperty().EdgeVisibilityOn()
      actor.GetProperty().SetEdgeColor(1, 1, 1)
      actors.append(actor)
  
  return actors
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
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------