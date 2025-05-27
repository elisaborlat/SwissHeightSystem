from lib.compute_htrans import Grid, compute_htrans
import numpy as np

def test_compute_htrans():

    Bougan = Grid() 
    Bougan.import_ascii_raster('data/raw/htrans/bougan-ascii.grd')

    Korrektur = Grid() 
    Korrektur.import_ascii_raster('data/raw/htrans/korrektur-ascii.grd')

    NormLN02 = Grid() 
    NormLN02.import_ascii_raster('data/raw/htrans/norm-ln02-ascii.grd')

    east_MN03 = 574911.36985
    north_MN03 = 183345.24126
    height_LN02 = 667.974

    east_grid_pos, north_grid_pos = Bougan.get_grid_pos(east_MN03,north_MN03)
    htransinv = compute_htrans(Bougan,Korrektur,NormLN02,east_grid_pos,north_grid_pos,height_LN02,corfac='to_lhn95')
    
    height_lhn95 = height_LN02 + htransinv
    
    height_lhn95_reframe = 667.9491

    assert abs(height_lhn95 - height_lhn95_reframe) < 1e-4