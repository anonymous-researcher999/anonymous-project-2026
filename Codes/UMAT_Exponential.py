import numpy as np
import torch

vars = {}

def umat_Exponential(DSTRAN, STRESS, DAMAGE, PS, material):
    # Constants
    ZERO, HALF, ONE, TWO, THREE, SIX = 0.0, 0.5, 1.0, 2.0, 3.0, 6.0
    TOL = 1.0e-12
    NDI = 3
    NTENS = 6


    if material == 'Steel' :
        # Elastic properties
        EMOD = 210.0e9
        XNU = 0.3
        # Plastic properties
        SIGY0 = 620.0e6
        XK = 3300e6
        XN = 0.4
        # Damage properties
        XR = 3.5e6
        XS = ONE

    elif material == 'Aluminum_AA7075_T6' :
        # Elastic properties
        EMOD = 71.1e9
        XNU = 0.33
        # Plastic properties
        SIGY0 = 491.5e6
        XK = 500.0e6
        XN = 1.05
        # Damage properties
        XR = 2.175e6
        XS = TWO



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
    vars['SIGY0'] = SIGY0
    vars['XK'] = XK
    vars['XN'] = XN
    vars['XR'] = XR
    vars['XS'] = XS

    # State variables
    P = PS
    DN = DAMAGE

    OMEGAN = ONE - DN
    LANDA = OMEGAN * P
    R = XK * (ONE - np.exp(-XN * LANDA))

    # Elastic tensor DDSDDE
    DDSDDE = np.zeros((NTENS, NTENS))
    for k1 in range(NDI):
        for k2 in range(NDI):
            DDSDDE[k1, k2] = OMEGAN * ELAM
        DDSDDE[k1, k1] = OMEGAN * (G2 + ELAM)
    for k in range(NDI, NTENS):
        DDSDDE[k, k] = OMEGAN * GMOD

    # Trial stress
    DSTRESSTR = DDSDDE @ DSTRAN
    STRESSTR = STRESS + DSTRESSTR

    HYDSTRESSTR = np.sum(STRESSTR[:3]) / THREE
    EFFHYDSTRESSTR = HYDSTRESSTR / OMEGAN

    DEVSTRESSTR = np.zeros(6)
    DEVSTRESSTR[:3] = STRESSTR[:3] - HYDSTRESSTR
    DEVSTRESSTR[3:] = STRESSTR[3:]

    XJ2TR = HALF * np.sum(DEVSTRESSTR[:3]**2) + np.sum(DEVSTRESSTR[3:]**2)
    EQSTRESSTR = np.sqrt(THREE * XJ2TR)
    EFFEQSTRESSTR = EQSTRESSTR / OMEGAN

    SIGMAY = SIGY0 + R
    PHI = EFFEQSTRESSTR - SIGMAY
    check = False
    OMEGA = 0.0
    EQSTRESS = 0.0

    DLANDA = 0.0
    if PHI <= ZERO:
        STRESS = STRESSTR.copy()
    else:
        # Plastic correction

        DLANDA = PHI * OMEGAN / G3
        for _ in range(100):
            R = XK * (ONE - np.exp(-XN * (LANDA + DLANDA)))
            SIGMAY = SIGY0 + R
            C1 = G3 / (EFFEQSTRESSTR - SIGMAY)
            OMEGA = C1 * DLANDA
            Y = -SIGMAY**2 / G6 - EFFHYDSTRESSTR**2 / BULK2
            C2 = -Y / XR
            RES = OMEGA - OMEGAN + (C2**XS) / C1
            if abs(RES) < TOL:
                break
            HSLOPE = XK * XN * np.exp(-XN * (LANDA + DLANDA))
            DY = -(SIGMAY * HSLOPE) / G3
            DRES = C1 + (C1 * DLANDA * HSLOPE / (EFFEQSTRESSTR - SIGMAY)) - \
                   ((HSLOPE / G3) * (C2 ** XS)) - \
                   (XS * DY / (C1 * XR)) * (C2 ** (XS - ONE))
            DDLANDA = -RES / DRES
            DLANDA += DDLANDA

            if DLANDA <0:
                DLANDA -= DDLANDA
                check = True
                break

        # Update stress at trial by knowing D
        # HYDSTRESSTR = 0
        # DEVSTRESSTR = np.zeros(6)
        # EFFDEVSTRESSTR = np.zeros(6)
        # DEVSTRESS = np.zeros(6)
        # EQSTRESSTR = 0
        
        HYDSTRESS  = OMEGA * EFFHYDSTRESSTR 
        EQSTRESS = OMEGA * SIGMAY
        DEVSTRESS = (EQSTRESS / EFFEQSTRESSTR) * DEVSTRESSTR / OMEGAN

        STRESS = np.zeros(6)
        STRESS[:3] = DEVSTRESS[:3] + HYDSTRESS
        STRESS[3:] = DEVSTRESS[3:]

        # Update state variables
        P = (LANDA + DLANDA) / OMEGA
        DN = ONE - OMEGA
        #if check == True:
            #DN = 1
            #DLANDA = -DLANDA

        
        #ckeck
        # sxx , syy , szz ,sxy, sxz, syz = torch.tensor(STRESS).unbind(-1)
        # sigma_eq = torch.sqrt( 0.5*( (sxx-syy)**2 + (syy-szz)**2 + (szz-sxx)**2) + 3*(sxy**2 + syz**2 + sxz**2))
        
        # F0 = sigma_eq/(1-DN)                     - (SIGMAY)
        
        # F3 = EQSTRESSTR/OMEGAN - G3*DLANDA/OMEGA - (SIGMAY)
        
        # C2 = -Y / XR
        # F2 = OMEGA - OMEGAN + C2 ** XS / C1
        
        # از هر دو دسته معادلات میتونی بری. که مثلا برای تسلیم اینجوری میشه و جفتش بر قراره
        
        # DDSDDE
        
        # from DDSDDE import elastic_ddsdde_3D
        # from ddsdde_components import compute_ddsdde_components
        # from devstressbar import calculate_devStressBar_tensors
        # from ddsdde_update import update_ddsdde


        # ddsdde = elastic_ddsdde_3D(EMOD, XNU)  * OMEGAN

        # A ,B,C,D,E = compute_ddsdde_components(G2, G3, HSLOPE, OMEGA, EFFEQSTRESSTR, SIGMAY, Y, XR, XS, HYDSTRESSTR, OMEGAN, BULK, EFFHYDSTRESSTR)

        # devstressbar, xid, xi = calculate_devStressBar_tensors(DEVSTRESS, XJ2TR, NDI, NTENS)

        # DDSDDE_updated = update_ddsdde(A, B, C, D, E, xid, devstressbar, xi, NTENS)
        
        
    return STRESS, DN, P, LANDA, DLANDA , check
