import numpy as np

def biquadratic(grid, east_grid_pos, north_grid_pos, east_dim, north_dim):

    points = np.zeros(9)
    coef = np.zeros(9)
    result = 0.0
    
    ix = np.round(north_grid_pos)
    iy = np.round(east_grid_pos)
    
    # Limiter les indices aux bords de la grille pour éviter les erreurs
    if ix == 0:
        ix = 1
    if ix == north_dim - 1:
        ix = north_dim - 2
    if iy == 0:
        iy = 1
    if iy == east_dim - 1:
        iy = east_dim - 2

    # Calculer les distances entre la position et les indices de la grille
    rx = north_grid_pos - ix
    ry = east_grid_pos - iy

    
    try:
        # Récupérer les 9 points voisins
        points[0] = grid[ix][iy]
        points[1] = grid[ix - 1][iy]
        points[2] = grid[ix - 1][iy + 1]
        points[3] = grid[ix][iy + 1]
        points[4] = grid[ix + 1][iy + 1]
        points[5] = grid[ix + 1][iy]
        points[6] = grid[ix + 1][iy - 1]
        points[7] = grid[ix][iy - 1]
        points[8] = grid[ix - 1][iy - 1]
        
        # Calculer les coefficients pour l'interpolation bi-quadratique
        coef[0] = points[0]
        coef[1] = (points[5] - points[1]) / 2.0
        coef[2] = (points[3] - points[7]) / 2.0
        coef[3] = (points[4] - points[2] + points[8] - points[6]) / 4.0
        coef[4] = (points[1] + points[5]) / 2.0 - points[0]
        coef[5] = (points[3] + points[7]) / 2.0 - points[0]
        coef[6] = (points[1] - points[5]) / 2.0 + (points[4] - points[2] - points[8] + points[6]) / 4.0
        coef[7] = (points[7] - points[3]) / 2.0 + (points[2] + points[4] - points[6] - points[8]) / 4.0
        coef[8] = points[0] - (points[1] + points[3] + points[5] + points[7]) / 2.0 + (points[2] + points[4] + points[6] + points[8]) / 4.0
        
        # Calculer la valeur interpolée en utilisant la formule quadratique
        result = (coef[0] + coef[1] * rx + coef[2] * ry + coef[3] * rx * ry + 
                  coef[4] * rx * rx + coef[5] * ry * ry + 
                  coef[6] * rx * ry * ry + coef[7] * rx * rx * ry + 
                  coef[8] * ry * ry * rx * rx)
        
        return result
    except IndexError:
        raise IndexError("Index out of bounds")
        
def get_grid_pos(east_pos, north_pos, east_min, east_max, north_min, north_max, east_dim, north_dim):
    step_east = (east_max - east_min) / (east_dim - 1.0)
    step_north = (north_max - north_min) / (north_dim - 1.0)
    east_grid_pos =  (east_pos - east_min) / step_east
    north_grid_pos =  (north_pos - north_min) / step_north
    return east_grid_pos, north_grid_pos