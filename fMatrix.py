
import numpy as np
from inpData import inpData

class fMatrix:

    def __init__(self, input):
        self.inp = input
        self.fp = self.inp.fp.copy()

    def set_fMatrix(self, k):
        tfe_l=self.TFVEC_3DFRM(k)
        tt = k.tt
        tfe  =np.dot(tt.T,tfe_l)          # Thermal load vector in global coordinate

        bfe  =self.BFVEC_3DFRM( k)        # Body force vector in global coordinate

        for i in range(0,12):
            it=k.ir[i]
            self.fp[it]=self.fp[it]+tfe[i]+bfe[i]


    def TFVEC_3DFRM(self, k):
        # Thermal load vector  in local coordinate system
        tfe_l=np.zeros(12,dtype=np.float64)
        i= k.iNo-1  
        j= k.jNo-1 
        E     = k.ee    # elastic modulus
        AA    = k.aa    # section area
        alpha = k.alpha # thermal expansion coefficient
        tempe=0.5*(self.inp.deltaT[i]+self.inp.deltaT[j])
        tfe_l[0]=-E*AA*alpha*tempe
        tfe_l[6]= E*AA*alpha*tempe

        return tfe_l

    def BFVEC_3DFRM(self, k):
        # Body force vector in global coordinate system
        bfe_g =np.zeros(12,dtype=np.float64)
        AA    = k.aa    # section area
        gamma = k.gamma # unit weight of material
        gkX   = k.gkX   # seismic coefficient in X-direction
        gkY   = k.gkY   # seismic coefficient in Y-direction
        gkZ   = k.gkZ   # seismic coefficient in Z-direction
        el    = k.el 
        bfe_g[0]=0.5*gamma*AA*el*gkX
        bfe_g[1]=0.5*gamma*AA*el*gkY
        bfe_g[2]=0.5*gamma*AA*el*gkZ
        bfe_g[6]=0.5*gamma*AA*el*gkX
        bfe_g[7]=0.5*gamma*AA*el*gkY
        bfe_g[8]=0.5*gamma*AA*el*gkZ

        return bfe_g



