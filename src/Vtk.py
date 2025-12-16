import vtk
from Node import Node
from Element import Element

# -----------------------------------------------------------------------------
def draw_mesh(nodes: list[Node] = None, elements: list[Element] = None) -> None:

  points = vtk.vtkPoints()
  for node in nodes:
    points.InsertNextPoint(node.x)
  
  lines = vtk.vtkCellArray()
  for element in elements:
    line = vtk.vtkLine()
    line.GetPointIds().SetId(0, element.id_nodes[0])
    line.GetPointIds().SetId(1, element.id_nodes[1])
    lines.InsertNextCell(line)

  # Create vertices to represent each point
  vertices = vtk.vtkCellArray()
  for i in range(points.GetNumberOfPoints()):
      vertex = vtk.vtkVertex()
      vertex.GetPointIds().SetId(0, i)
      vertices.InsertNextCell(vertex)

  # Create a polydata object to hold the points and vertices
  points_polydata = vtk.vtkPolyData()
  points_polydata.SetPoints(points)
  points_polydata.SetVerts(vertices)

  lines_polydata = vtk.vtkPolyData()
  lines_polydata.SetPoints(points)
  lines_polydata.SetLines(lines)

  # Mapper and actor
  points_mapper = vtk.vtkPolyDataMapper()
  lines_mapper = vtk.vtkPolyDataMapper()
  points_mapper.SetInputData(points_polydata)
  lines_mapper.SetInputData(lines_polydata)

  points_actor = vtk.vtkActor()
  points_actor.SetMapper(points_mapper)
  points_actor.GetProperty().SetPointSize(20)  # make points larger
  points_actor.GetProperty().SetColor(255/255, 128/255, 0/255) # red color
  points_actor.GetProperty().SetRenderPointsAsSpheres(True)
  lines_actor = vtk.vtkActor()
  lines_actor.SetMapper(lines_mapper)
  lines_actor.GetProperty().SetColor(0/255, 128/255, 255/255)   # Green lines
  lines_actor.GetProperty().SetLineWidth(6)     # Thicker lines

  # Renderer, render window, and interactor
  renderer = vtk.vtkRenderer()
  renderer.AddActor(lines_actor)
  renderer.AddActor(points_actor)
  renderer.SetBackground(0.1, 0.1, 0.1)  # dark background

  render_window = vtk.vtkRenderWindow()
  render_window.AddRenderer(renderer)
  render_window.SetSize(800, 800)

  interactor = vtk.vtkRenderWindowInteractor()
  interactor.SetRenderWindow(render_window)

  # Optional: smoother interaction
  style = vtk.vtkInteractorStyleTrackballCamera()
  interactor.SetInteractorStyle(style)

  # Start rendering
  render_window.Render()
  interactor.Start()
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