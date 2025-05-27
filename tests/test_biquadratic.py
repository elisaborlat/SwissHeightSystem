
from lib.biquadtratic import get_grid_pos, biquadratic
import numpy as np

def test_biquadtatic():
   # Grid data
    grid = np.array([[5, 0.2, 13],
                     [2, 2, 0.2],
                     [0.2, 5, 25]])
    
    east_min, east_max = 1,10  # Coordonnées x de la grille
    north_min, north_max = 9,10   # Coordonnées y de la grille
    
    # Coordinates
    north_pos = 9.1
    east_pos = 2.5

    # Appeler la fonction d'interpolation
    east_grid_pos, north_grid_pos = get_grid_pos(east_pos, north_pos, east_min, east_max, north_min, north_max, 3, 3)
    result = biquadratic(grid, east_grid_pos, north_grid_pos, 3, 3)

    assert abs(result - 1.8231) < 1e-4