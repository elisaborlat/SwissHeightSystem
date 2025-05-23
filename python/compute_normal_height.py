import numpy as np

# Définition des constantes exactes GRS80, IUGG Resolution No. 7
CONSTANT_a = 6378137  # semimajeur axe, equatorial radius
# CONSTANT_GM = 3986005e8  # constante gravitationnelle géocentrique
# CONSTANT_J2 = 108263e-8  # facteur de forme dynamique
# CONSTANT_omega = 7292115e-11  # vitesse angulaire, angular velocity

# Dérivation des constantes géométriques
# DCONSTANT_b = 6356752.3141  # semimineur axe
DCONSTANT_e2 = 0.00669438002290  # carré de l'excentricité première (e)
DCONSTANT_f = 0.00335281068118  # aplatissement
# DCONSTANT_f_inv = 298.257222101  # inverse de l'aplatissement
# DCONSTANT_Q = 10001965.7293  # quart de méridien
# DCONSTANT_R1 = 6371008.7714  # rayon moyen
# DCONSTANT_R2 = 6371007.1810  # rayon d'une sphère de même surface
# DCONSTANT_R3 = 6371000.7900  # rayon d'une sphère de même volume

# Définition des constantes physiques dérivées
# DCONSTANT_U0 = 6263686.0850e2  # potentiel normal à l'ellipsoïde
# DCONSTANT_J4 = -0.00000023709122  # coefficients harmoniques sphériques
# DCONSTANT_J6 = 0.0000000000608347  # coefficients harmoniques sphériques
DCONSTANT_m = 0.00344978600308  # gravité normale à l'équateur
DCONSTANT_gamma_e = 9.7803267715  # gravité normale au pôle
# DCONSTANT_f_star = 0.005302440112  # facteur d'aplatissement
DCONSTANT_k = 0.001931851353  # facteur de courbure

def compute_mean_normal_gravity(gamma0, latitude_rad, height):
    gamma = gamma0 * (1 - (1 + DCONSTANT_f + DCONSTANT_m - 2 * DCONSTANT_f * np.sin(latitude_rad) ** 2) * 
                      height / CONSTANT_a + height ** 2 / CONSTANT_a ** 2)
    return gamma

def compute_normal_height_from_pot(potential, latitude_deg, log=True):
    """
    Compute the normal height from the given potential and latitude.

    Parameters
    ----------
    potential : float
        The potential value in m2/s2
    latitude_deg : float
        The latitude in degrees.

    Returns
    -------
    float
        The computed normal height. 
    """

    # Convert latitude to radians
    latitude_rad = np.deg2rad(latitude_deg)
    
    # Constants (Moritz, 1980)
    gamma0 = DCONSTANT_gamma_e * (1 + DCONSTANT_k * np.sin(latitude_rad) ** 2) / \
             np.sqrt(1 - DCONSTANT_e2 * np.sin(latitude_rad) ** 2)    

    # Initial height estimate
    height = potential / gamma0
    previous_gamma = 0

    # Compute mean normal gravity along the plumb line
    gamma = compute_mean_normal_gravity(gamma0,latitude_rad, height)
    
    if log : 
        print("---------------------")
        print("Compute normal height")
        print("---------------------")
        print("gamma0: ", gamma0)
        print("Iter 0")
        print("Height : ", height)
        print("Gamma : ", gamma)

    tolerance = 1e-8

    # Iteratively compute normal height
    nbr_iter = 1
    while abs(gamma - previous_gamma) > tolerance: 
        height = potential / gamma        
        previous_gamma = gamma
        # Normal potential (Heiskanen & Moritz, 1967)
        gamma = gamma0 * (1 - (1 + DCONSTANT_f + DCONSTANT_m - 2 * DCONSTANT_f * np.sin(latitude_rad) ** 2) * 
                          height / CONSTANT_a + height ** 2 / CONSTANT_a ** 2)

        if log : 
            print("Iter ", nbr_iter)
            print("Height :", height)
            print("Gamma : ", gamma)

        nbr_iter += 1

    if log: 
        print("---------------------")
        print(f"Critère de convergence : {tolerance} m")
        print(f'Nbr iteration : {nbr_iter}')
        print(f'Geopotential value (input) : {potential} m2/s2')
        print(f"Latitude degre (input) : {latitude_deg} deg")
        print(f'Normal height (output) : {height:.4f} m')

    return height



