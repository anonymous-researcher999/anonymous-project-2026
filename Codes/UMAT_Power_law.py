import numpy as np
import torch

vars = {}

def umat_Power_law(DSTRAN, STRESS, DAMAGE, PS, material):

    
    # DSTRAN = E(n) - E(n-1)
    NDI = 3
    NTENS = 6
    
    # Parameters
    ZERO = 0.0
    HALF = 0.5
    ONE = 1.0
    TWO = 2.0
    THREE = 3.0
    SIX = 6.0
    TOL = 1.0E-6

    # properties
    if material == 'Aluminum_notched_bar' :
        # Elastic properties
        EMOD = 69.004E9
        XNU = 0.3
        # Plastic properties
        XK = 589.0E6
        XM = 0.0001
        XN = 0.216
        # Damage properties
        XR = 1.25E6
        XS = ONE
    
    elif material == 'Aluminum_flat_grooved' :
        # Elastic properties
        EMOD = 71.154E9
        XNU = 0.3
        # Plastic properties
        XK = 908.0E6
        XM = 0.0058
        XN = 0.1742
        # Damage properties
        XR = 1.7E6
        XS = ONE
    
    
    GMOD = EMOD / (TWO * (ONE + XNU))
    G2 = TWO * GMOD
    G3 = THREE * GMOD
    G6 = SIX * GMOD
    BULK = EMOD / (THREE * (ONE - TWO * XNU))
    BULK2 = TWO * BULK
    BULK3 = THREE * BULK
    ELAM = (BULK3 - G2) / THREE


    
    vars['EMOD'] = EMOD
    vars['XNU'] = XNU
    vars['GMOD'] = GMOD
    vars['XK'] = XK
    vars['XM'] = XM
    vars['XN'] = XN
    vars['XR'] = XR
    vars['XS'] = XS
    
    


    # Extract variables
    P = PS
    DN = DAMAGE

    OMEGAN = ONE - DN
    LANDA = OMEGAN * P
    R = XK * (XM + LANDA) ** XN

    # Elastic tensor
    DDSDDE = np.zeros((NTENS, NTENS))
    for k1 in range(NDI):
        for k2 in range(NDI):
            DDSDDE[k1, k2] = OMEGAN * ELAM
        DDSDDE[k1, k1] = OMEGAN * (G2 + ELAM)
    
    for k in range(NDI, NTENS):
        DDSDDE[k, k] = OMEGAN * GMOD

    # Calculate elastic trial stress
    DSTRESSTR = np.dot(DDSDDE, DSTRAN)
    STRESSTR = STRESS + DSTRESSTR  # Important: STRESS must be accumulated during increments

    # Calculate elastic trial deviatoric stress
    HYDSTRESSTR = np.sum(STRESSTR[:NDI]) / THREE
    EFFHYDSTRESSTR = HYDSTRESSTR / OMEGAN
    DEVSTRESSTR = np.zeros(NTENS)
    
    for k in range(NDI):
        DEVSTRESSTR[k] = STRESSTR[k] - HYDSTRESSTR
    
    for k in range(NDI, NTENS):
        DEVSTRESSTR[k] = STRESSTR[k]

    # Calculate trial von Mises equivalent stress
    XJ2TR = ZERO
    for K in range(NDI):
        XJ2TR += HALF * DEVSTRESSTR[K] ** 2
    
    for K in range(NDI, NTENS):
        XJ2TR += DEVSTRESSTR[K] ** 2

    EQSTRESSTR = np.sqrt(3 * XJ2TR)
    EFFEQSTRESSTR = EQSTRESSTR / OMEGAN

    # Check for plastic admissibility
    SIGMAY = R
    PHI = EFFEQSTRESSTR - SIGMAY
    check = False
    
    DLANDA = 0.0
    
    if PHI <= ZERO:  # Elastic case
        STRESS = STRESSTR.copy()
    else:  # Plastic case
        # Newton-Raphson to solve the return mapping equation for OMEGA(DLANDA)
        
        DLANDA = PHI * OMEGAN / G3
        
        for I in range(100):  # Max 100 iterations
            R = XK * (XM + LANDA + DLANDA) ** XN
            SIGMAY = R
            C1 = G3 / (EFFEQSTRESSTR - SIGMAY)
            OMEGA = C1 * DLANDA
            Y = -(SIGMAY ** 2) / G6 - (EFFHYDSTRESSTR ** 2) / BULK2
            C2 = -Y / XR
            
            RES = OMEGA - OMEGAN + (C2 ** XS) / C1
            
            if abs(RES) < TOL:
                break
            
            HSLOPE = XK * XN * (XM + (LANDA + DLANDA)) ** (XN - ONE)
            DY = -(SIGMAY * HSLOPE) / G3
            DRES = (C1 + (C1 * DLANDA * HSLOPE / (EFFEQSTRESSTR - SIGMAY)) - 
                   ((HSLOPE / G3) * (C2 ** XS)) - 
                   (XS * DY / (C1 * XR)) * (C2 ** (XS - ONE)))
            
            DDLANDA = -RES / DRES
            DLANDA += DDLANDA
            
            if DLANDA <0:
                DLANDA -= DDLANDA
                check = True
                break
            

        # Update variables according to OMEGA(DLANDA) new value
        HYDSTRESS = OMEGA * EFFHYDSTRESSTR
        EQSTRESS = OMEGA * SIGMAY
        DEVSTRESS = (EQSTRESS / EFFEQSTRESSTR) * DEVSTRESSTR / OMEGAN

        XJ2 = ZERO
        
        # Update stress components
        for K in range(NDI):
            XJ2 += HALF * DEVSTRESS[K] ** TWO
            STRESS[K] = DEVSTRESS[K] + HYDSTRESS
        
        for K in range(NDI, NTENS):
            XJ2 += DEVSTRESS[K] ** TWO
            STRESS[K] = DEVSTRESS[K]

        # Update State Variables
        P = (LANDA + DLANDA) / OMEGA
        DN = ONE - OMEGA
        
        if DN > 1:
            DN = 1
            DLANDA = -DLANDA

        # Verification calculations (commented out as in original MATLAB)
        # F = EQSTRESSTR/OMEGAN - G3*DLANDA/OMEGA - R
        # EFEQSTRESSNEW = EQSTRESSTR/OMEGAN - G3*DLANDA/OMEGA
        
        XJ2TR = 0
        for K in range(NDI):
            XJ2TR += HALF * DEVSTRESS[K] ** 2
        
        for K in range(NDI, NTENS):
            XJ2TR += DEVSTRESS[K] ** 2

        EQSTRESSNEW = np.sqrt(3 * XJ2TR)
        EFEQSTRESSNEW = EQSTRESSNEW / OMEGA
        F2 = EFEQSTRESSNEW - SIGMAY

    return STRESS, DN, P, LANDA, DLANDA , check