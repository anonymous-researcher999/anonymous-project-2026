import numpy as np
import random

def strain_curve_generator(domain , component):

    P0 = np.array([0.0, 0.0, 0.0])
    
    if component == 'normal' :
        # Generate random P1 in the domain, with possible sign flips
        P1 = np.array([
            random.uniform(0.0, domain),
            random.uniform(0.0, domain),
            random.uniform(0.0, domain)
        ])
        for k in range(3):
            if random.randint(0, 1) == 1:
                P1[k] = -P1[k]

    elif component == 'shear' :
        # Generate random P1 in the domain, with possible sign flips
        P1 = np.array([
            random.uniform(0.0, domain),
            random.uniform(0.0, domain),
            random.uniform(0.0, domain)
        ])
        max_index = np.argmax(P1)
        for i in range(3):
            if i != max_index:
                P1[i] /= 10
        
        for k in range(3):
            if random.randint(0, 1) == 1:
                P1[k] = -P1[k]


    # Generate middle control point P2 with random perturbation
    # curve controler
    alpha = random.uniform(0.7, 0.9)
    betta = 0.15
    
    P2 = np.array([
        P1[0] * alpha + random.uniform(0, betta * abs(P1[0])),
        P1[1] * alpha + random.uniform(0, betta * abs(P1[1])),
        P1[2] * alpha + random.uniform(0, betta * abs(P1[2]))
    ])
    for k in range(3):
        if random.randint(0, 1) == 1:
            P2[k] = -P2[k]



    # Bézier curve
    t = np.linspace(0, 1, 100)
    A = (1 - t) ** 2
    B = 2 * (1 - t) * t
    C = t ** 2

    out0 = A * P0[0] + B * P2[0] + C * P1[0]
    out1 = A * P0[1] + B * P2[1] + C * P1[1]
    out2 = A * P0[2] + B * P2[2] + C * P1[2]

    return out0, out1, out2     
