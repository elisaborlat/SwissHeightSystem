from python.compute_normal_height import compute_normal_height_from_pot

def test_compute_normal_height_from_pot():
    # Données d'entrée (point UELN 100026 ou GR 3489, BlattEVRF2019_final_update.csv)
    geopotential_kgal_m_EVRF2019_zero_tide = 1037.6342
    latitude_degre_ETRS89 = 46.929883

    # Résultat attendu (en mètres)
    expected_height_m = 1058.1288

    # Appel de la fonction
    Hnorm = compute_normal_height_from_pot(geopotential_kgal_m_EVRF2019_zero_tide * 10.0, latitude_degre_ETRS89)

    # Vérification avec tolérance (float)
    assert abs(Hnorm - expected_height_m) < 1e-4


