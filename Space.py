import vtk
# from Shape import Shape as SP

class Space:
  # ---------------------------------------------------------------------------    
  def __init__(self, width=1000, height=800, background=(0.1, 0.1, 0.1)):
    self.renderer = vtk.vtkRenderer()
    self.renderer.SetBackground(*background)
    self.render_window = vtk.vtkRenderWindow()
    self.render_window.AddRenderer(self.renderer)
    self.render_window.SetSize(width, height)  # ✅ larger default size
    self.render_window.SetWindowName("Shape Viewer")

    self.interactor = vtk.vtkRenderWindowInteractor()
    self.interactor.SetRenderWindow(self.render_window)

    # Smooth camera control
    style = vtk.vtkInteractorStyleTrackballCamera()
    self.interactor.SetInteractorStyle(style)

    self.renderer.SetBackground(0.1, 0.1, 0.1)

    self.elements: list = []
    self.timer_id = None
  # ---------------------------------------------------------------------------
  def add_elements(self, elements: list = None, nodes = None, color=(0.8, 0.8, 0.8), opacity=1.0):
    if elements is None or nodes is None:
      return
    for element in elements:
      actor = element.get_actor(nodes, color, opacity)
      self.renderer.AddActor(actor)
      self.elements.append(element)
  # ---------------------------------------------------------------------------
  def update(self, update_func=None, interval_ms=30):
    """Starts the interactive scene with safe exit handling."""

    self.render_window.Render()
    self.interactor.Initialize()

    # --- Timer callback for animation ---
    if update_func:
      def timer_callback(caller, event):
        try:
          update_func(self)
          self.render_window.Render()
        except Exception as e:
          print(f"Timer update failed: {e}")

      self.interactor.AddObserver("TimerEvent", timer_callback)
      self.timer_id = self.interactor.CreateRepeatingTimer(interval_ms)

    # --- Define clean exit behavior ---
    def close_window():
      print("Closing window...")
      if self.timer_id is not None:
        self.interactor.DestroyTimer(self.timer_id)
      self.render_window.Finalize()
      self.interactor.TerminateApp()
      del self.render_window

    # --- Handle x close event ---
    def exit_callback(obj, event):
      close_window()

    self.render_window.AddObserver("WindowCloseEvent", exit_callback)

    # --- Handle keypress for quitting ---
    def keypress_callback(obj, event):
      key = obj.GetKeySym()
      if key in ("Escape", "q"):
        close_window()

    self.interactor.AddObserver("KeyPressEvent", keypress_callback)

    # --- Start interaction ---
    self.interactor.Start()
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
