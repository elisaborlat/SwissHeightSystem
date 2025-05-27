from lib.compute_htrans import Grid

def test_chklm95():
   # Grid data
    Kinematik = Grid()
    Kinematik.import_file_DSAA_grid('rcm0406_ascii.grd')
    
    east_grid_pos, north_grid_pos = Kinematik.get_grid_pos(750532.0,155532.0)
    velocity = Kinematik.biquadratic(east_grid_pos, north_grid_pos) #mm/yr

    assert abs(velocity - 1.029769) < 1e-4