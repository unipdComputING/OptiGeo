import numpy as np
from Global import *

class Node:
  # ---------------------------------------------------------------------------
  def __init__(self, id: int = 0, x: np = np.zeros(DIM_SPACE)):
    self.id: int = id
    self.x: np = x
    self.dof: np = np.zeros(DIM_DOF)
    self.fix: np = np.zeros(DIM_DOF)
    self.load: np = np.zeros(DIM_DOF)
  # ---------------------------------------------------------------------------
  def dist(self, node: "Node") -> float:
    # x = node.x - self.x
    x = self.direction(node)
    return np.sqrt(np.dot(x, x))
  # ---------------------------------------------------------------------------
  def direction(self, node: "Node") -> np:
    return node.x - self.x
  # ---------------------------------------------------------------------------
  def add_load(self, load: np) -> None:
    self.load += load
  # ---------------------------------------------------------------------------
  def add_constraint(self, fix: np = np.zeros(DIM_DOF), dof: np = np.zeros(DIM_DOF)) -> None:
    self.fix = fix
    self.dof = dof
  # ---------------------------------------------------------------------------
  def set_fix(self) -> None:
    self.fix = np.ones(DIM_DOF)
    self.dof = np.zeros(DIM_DOF)
  # ---------------------------------------------------------------------------
  def set_free(self) -> None:
    self.fix = np.zeros(DIM_DOF)
    self.dof = np.zeros(DIM_DOF)
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------