import numpy as np

def elastic_ddsdde_3D(E, nu):
    lam = E * nu / ((1 + nu) * (1 - 2 * nu))
    G  = E / (2 * (1 + nu))
    ddsdde = np.zeros((6, 6))
    
    # Normal components
    for i in range(3):
        for j in range(3):
            ddsdde[i, j] = lam
        ddsdde[i, i] += 2 * G  # Add 2μ to diagonal terms

    # Shear components
    for i in range(3, 6):
        ddsdde[i, i] = G

    return ddsdde