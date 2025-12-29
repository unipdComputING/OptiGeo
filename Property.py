import numpy as np
from Global import *

"""! @brief Defines the Property classes."""
class Property:
  # ---------------------------------------------------------------------------
  def __init__(self, id: int = 0, young: float = 0, poisson: float = 0.0, area: float = 0) -> None:
    """! The Property base class initializer.
    @param id  The property id.
    @param young  The elastic modulus.
    @param poisson  The Poisson's ratio.
    @param area The cross section area (only for 1D elements).
    @return  An instance of the Property class initialized.
    """
    self.id: int = id
    self.young: float = young
    self.area: float = area
    poisson = max(min(poisson, .4_999_999), 0.)
    self.poisson: float = poisson
  # ---------------------------------------------------------------------------
  def get_el_const_mat(self) -> np.ndarray:
    """! Elastic constitutive matrix definition in Voig notation (in a 3D space)
    @return Nothig
    """
    E: float = self.young
    nu: float = self.poisson
    l: float = E * nu / (( 1. + nu) * (1. - 2. * nu))
    m: float  = E / (2. * (1. + nu))

    D = np.array([
      [l + 2. * m, l         , l         , 0., 0., 0.],
      [l         , l + 2. * m, l         , 0., 0., 0.],
      [l         , l         , l + 2. * m, 0., 0., 0.],
      [0.        , 0.        , 0.        , m , 0., 0.],
      [0.        , 0.        , 0.        , 0., m , 0.],
      [0.        , 0.        , 0.        , 0., 0., m ]
    ])
    return D
  # ---------------------------------------------------------------------------
  # example of linear elastic isotropic material
  # 
  def get_const_mat(self, ostrain: np.ndarray = np.zeros(DIM_TENSOR), dstrain: np.ndarray = np.zeros(DIM_TENSOR), 
                    stress: np.ndarray = np.zeros(DIM_TENSOR), 
                    statev: np.ndarray = None) -> tuple[np.ndarray, np.ndarray]:
    """! Function to compute the stress vector and the constitutive tangent operator in Voigt notation at increment n+1
    @param ostrain  Strain vector at increment n
    @param dstrain  Strain increment
    @param stress   Stress vector at increment n
    @param statev   State variables stored at increment n
    @return Nothing
    """
    strain: np.ndarray = ostrain + dstrain
    D = self.get_el_const_mat()
    stress: np.ndarray = D @ strain
    I1 = (stress[0] + stress[1] + stress[2]) / 3.0 
    if statev is not None:
      statev[0] = I1
    return (stress, D)
  # ---------------------------------------------------------------------------
  # ---------------------------------------------------------------------------