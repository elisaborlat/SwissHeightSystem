import numpy as np

class Grid : 
    def __init__(self):
        self.data = None
        self.ncols = None
        self.nrows = None
        self.Xmin = None
        self.Xmax = None
        self.Ymin = None
        self.Ymax = None
        self.cellsize = None

    def __repr__(self):
        return (f"Grid(ncols={self.ncols}, nrows={self.nrows}, "
                f"Xmin={self.Xmin}, Xmax={self.Xmax}, "
                f"Ymin={self.Ymin}, Ymax={self.Ymax})")
    
    def coord_is_in_bbox(self, east, north): 
        if (self.Ymin <= east <= self.Ymax) and (self.Xmin <= north <= self.Xmax) : 
            return True
        else :
            return False
        
    
    def get_grid_points(self):
        Egrid = np.linspace(self.Ymin, self.Ymax, self.ncols)
        Ngrid = np.linspace(self.Xmin, self.Xmax, self.nrows)
        grid_X, grid_Y = np.meshgrid(Egrid, Ngrid)
        return grid_X, grid_Y
        
    def import_ascii_raster(self, file_path, mode=''):
    
        with open(file_path, 'r') as file:
            # Read header
            self.ncols = int(file.readline().split()[1])
            self.nrows = int(file.readline().split()[1])
            xllcorner = float(file.readline().split()[1])
            yllcorner = float(file.readline().split()[1])
            self.cellsize = float(file.readline().split()[1])
            nodata_value = float(file.readline().split()[1])

            data = np.loadtxt(file_path, skiprows=6)  # Skip the header rows
            self.data = np.array(data)
            self.Xmin = xllcorner
            self.Xmax = xllcorner + self.cellsize * (self.nrows-1)
            self.Ymin = yllcorner
            self.Ymax = yllcorner + self.cellsize * (self.ncols-1) 


    def biquadratic(self, east_grid_pos, north_grid_pos):

        points = np.zeros(9)
        coef = np.zeros(9)
        result = 0.0
        
        ix = int(np.round(north_grid_pos))
        iy = int(np.round(east_grid_pos))
        
        # Limiter les indices aux bords de la grille pour éviter les erreurs
        if ix == 0:
            ix = 1
        if ix == self.nrows - 1:
            ix = self.nrows - 2
        if iy == 0:
            iy = 1
        if iy == self.ncols - 1:
            iy = self.ncols - 2

        # Calculer les distances entre la position et les indices de la grille
        rx = north_grid_pos - ix
        ry = east_grid_pos - iy

        
        try:
            # Récupérer les 9 points voisins
            points[0] = self.data[ix][iy]
            points[1] = self.data[ix - 1][iy]
            points[2] = self.data[ix - 1][iy + 1]
            points[3] = self.data[ix][iy + 1]
            points[4] = self.data[ix + 1][iy + 1]
            points[5] = self.data[ix + 1][iy]
            points[6] = self.data[ix + 1][iy - 1]
            points[7] = self.data[ix][iy - 1]
            points[8] = self.data[ix - 1][iy - 1]
            
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
            
    def get_grid_pos(self, east_pos, north_pos):
        """
        Calculate the grid position (east, north) based on geographic coordinates and grid dimensions.

        Parameters:
        east_pos (float): Easting position (x-coordinate) of the point.
        north_pos (float): Northing position (y-coordinate) of the point.

        Returns:
        tuple: (east_grid_pos, north_grid_pos) representing the position in the grid coordinates.
        """
        
        east_grid_pos = (east_pos - self.Ymin) / self.cellsize
        north_grid_pos = (self.Xmax - north_pos) / self.cellsize
        return east_grid_pos, north_grid_pos

def compute_htrans(bougan, korrektor, norm_ln02, east_grid_pos, north_grid_pos, height, corfac='to_lhn95'):

    """
    Computes the height transformation based on Bouguer anomalies, corrections, 
    and normalization factors.

    Parameters
    ----------
    bougan : object
        An object representing Bouguer anomalies with a `bi_quadratic` method 
        for grid interpolation.
    korrektor : object
        An object representing correction values with a `bi_quadratic` method 
        for grid interpolation.
    norm_ln02 : object
        An object representing normalization factors in LN02 with a 
        `bi_quadratic` method for grid interpolation.
    corfac : str, optional
        Specifies the transformation direction. If set to 'to_lhn95', the 
        computed transformation is directed to LHN95; if 'to_ln02', it is directed 
        to LN02. Default is 'to_lhn95'.

    Returns
    -------
    float
        The transformed height value, adjusted based on the selected direction.
    """

    # Set correction factor based on the specified transformation direction
    corfac = 1 if corfac == 'to_lhn95' else -1 if corfac == 'to_ln02' else corfac

    boug = bougan.biquadratic(east_grid_pos, north_grid_pos)
    # print('Bougan : ', boug)
    korr = korrektor.biquadratic(east_grid_pos, north_grid_pos)
    # print('Korr : ', korr)
    norm = norm_ln02.biquadratic(east_grid_pos, north_grid_pos)
    # print('Norm : ', norm)

    total = norm - korr - boug * height / 980000.0
    
    return corfac * total
