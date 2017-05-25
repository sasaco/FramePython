
import numpy as np

class outData:

    def __init__(self, input, result, gmat):
        self.inp = input
        self.disg = result
        self.fsec = np.zeros([self.inp.n12, self.inp.nele], dtype=np.float64)  # Section force vector

        # recovery of restricted displacements
        for i in range(0,self.inp.npoin):
            for j in range(0,self.inp.nfree):
                if self.inp.mpfix[j,i]==1:
                    iz=i*self.inp.nfree+j
                    self.disg[iz]=self.inp.rdis[j,i]

        # calculation of section force
        work =np.zeros(self.inp.n12, dtype=np.float64)         # work vector for section force calculation
        for ne in range(0,self.inp.nele):
            k = gmat.kmat[ne]

            i     = k.iNo-1  
            j     = k.jNo-1 
            ek    = k.ek    # Stiffness matrix in local coordinate
            tt    = k.tt    # Transformation matrix
            E     = k.ee    # elastic modulus
            AA    = k.aa    # section area
            alpha = k.alpha # thermal expansion coefficient
            tempe = 0.5*(self.inp.deltaT[i]+self.inp.deltaT[j])

            work[0]=self.disg[6*i]  ; work[1] =self.disg[6*i+1]; work[2]= self.disg[6*i+2]
            work[3]=self.disg[6*i+3]; work[4] =self.disg[6*i+4]; work[5]= self.disg[6*i+5]
            work[6]=self.disg[6*j]  ; work[7] =self.disg[6*j+1]; work[8]= self.disg[6*j+2]
            work[9]=self.disg[6*j+3]; work[10]=self.disg[6*j+4]; work[11]=self.disg[6*j+5]


            self.fsec[:,ne]=np.dot(ek,np.dot(tt,work))
            self.fsec[0,ne]=self.fsec[0,ne]+E*AA*alpha*tempe
            self.fsec[6,ne]=self.fsec[6,ne]-E*AA*alpha*tempe

    def PROUT_3DFRM(self, fnameW):
        fout=open(fnameW,'a')

        # displacement
        print('{0:>5s} {1:>15s} {2:>15s} {3:>15s} {4:>15s} {5:>15s} {6:>15s}'
              .format('node','dis-x','dis-y','dis-z','rot-x','rot-y','rot-z'),file=fout)
        for i in range(0,self.inp.npoin):
            lp=i+1
            print('{0:5d} {1:15.7e} {2:15.7e} {3:15.7e} {4:15.7e} {5:15.7e} {6:15.7e}'
                  .format(lp,self.disg[6*lp-6],self.disg[6*lp-5],self.disg[6*lp-4],self.disg[6*lp-3],self.disg[6*lp-2],self.disg[6*lp-1]),file=fout)

        # section force
        print('{0:>5s} {1:>5s} {2:>15s} {3:>15s} {4:>15s} {5:>15s} {6:>15s} {7:>15s}'
        .format('elem','nodei','N_i','Sy_i','Sz_i','Mx_i','My_i','Mz_i'),file=fout)
        print('{0:>5s} {1:>5s} {2:>15s} {3:>15s} {4:>15s} {5:>15s} {6:>15s} {7:>15s}'
        .format('elem','nodej','N_j','Sy_j','Sz_j','Mx_j','My_j','Mz_j'),file=fout)
        for ne in range(0,self.inp.nele):
            print('{0:5d} {1:5d} {2:15.7e} {3:15.7e} {4:15.7e} {5:15.7e} {6:15.7e} {7:15.7e}'
            .format(ne+1,self.inp.node[0,ne],self.fsec[0,ne],self.fsec[1,ne],self.fsec[2,ne],self.fsec[3,ne],self.fsec[4,ne],self.fsec[5,ne]),file=fout)
            print('{0:5d} {1:5d} {2:15.7e} {3:15.7e} {4:15.7e} {5:15.7e} {6:15.7e} {7:15.7e}'
            .format(ne+1,self.inp.node[1,ne],self.fsec[6,ne],self.fsec[7,ne],self.fsec[8,ne],self.fsec[9,ne],self.fsec[10,ne],self.fsec[11,ne]),file=fout)

        fout.close()
