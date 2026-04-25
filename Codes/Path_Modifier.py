import numpy as np
from Stress_Damage_calculator import stress_Damage_calculator


def modifier_PINN(X_pinn , du, material):


    Y_pinn = stress_Damage_calculator(X_pinn , du , material)


    n = 0
    N = []

    for i in range(du):
        if Y_pinn[i][6, 98] < Y_pinn[i][6, 99]:  
            n += 1
            N.append(i)

    q = len(N) - len(N) % 1000
    print('N =', len(N))
    print('num_collocation =', q)
    
    Y_pinn_mod = [None] * q
    X_pinn_mod = [None] * q

    for i in range(q):
        idx = N[i]
        Y_pinn_mod[i] = Y_pinn[idx][0:7, :].copy()  # 7*100

        X_temp = np.zeros((7, X_pinn[idx].shape[1]))
        X_temp[0:6, :] = X_pinn[idx]               
        X_temp[6, :] = Y_pinn[idx][7, :].copy()

        X_pinn_mod[i] = X_temp


    return X_pinn_mod , Y_pinn_mod , q





def modifier_default(X_total , su, material):

    Y_total = stress_Damage_calculator(X_total , su , material)
    
    n = 0
    N = []

    for i in range(su):
        if Y_total[i][6, 98] < Y_total[i][6, 99]:  
            n += 1
            N.append(i)

    q = len(N) - len(N) % 1000

    print('N =', len(N))
    print('num_total_data =', q)
    
    Y_total_mod = [None] * q
    X_total_mod = [None] * q

    for i in range(q):
        idx = N[i]
        Y_total_mod[i] = Y_total[idx][0:7, :].copy()  # 7*100

        X_temp = np.zeros((7, X_total[idx].shape[1]))
        X_temp[0:6, :] = X_total[idx]               
        X_temp[6, :] = Y_total[idx][7, :].copy()

        X_total_mod[i] = X_temp
        
    return X_total_mod , Y_total_mod , q