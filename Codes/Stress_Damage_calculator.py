import numpy as np
from UMAT_Exponential import umat_Exponential
from UMAT_Power_law import umat_Power_law

def stress_Damage_calculator(X_total , su , material):
    
    Y_total = [None] * su
    
    for m in range(su):
        X = X_total[m]  # shape: (6, 100)
        R = np.zeros((100, 8))  # 6 stress, 1 damage, 1 DLANDA

        DAMAGE = 0.0
        PS = 0.0
        STRESS = np.zeros(6)
        DLANDA = 0.0
        ck = False

        for i in range(99):
            E1 = X[:, i]
            E2 = X[:, i + 1]
            dE = E2 - E1
            
            if material == 'Steel' or material == 'Aluminum_AA7075_T6':
                stress, damage, ps, LANDA, DLANDA, ck = umat_Exponential(dE, STRESS, DAMAGE, PS, material)
            
            elif material == 'Aluminum_notched_bar' or material == 'Aluminum_flat_grooved':
                stress, damage, ps, LANDA, DLANDA, ck = umat_Power_law(dE, STRESS, DAMAGE, PS , material)
            
            R[i + 1, 0:3] = stress[0:3] / 1e9
            R[i + 1, 3:6] = stress[3:6] / 1e8
            R[i + 1, 6] = damage
            R[i + 1, 7] = DLANDA *100

            STRESS = stress
            DAMAGE = damage
            PS = ps

            if ck == True:
                R[i+1:, 0:3] = stress[0:3] / 1e9
                R[i+1:, 3:6] = stress[3:6] / 1e8
                R[i+1:, 6] = damage
                break

        Y_total[m] = R.T  # shape: (8, 100)
        
    return Y_total