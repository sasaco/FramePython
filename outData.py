
import numpy as np
import json
from collections import OrderedDict

class outData:

    def __init__(self, inp, result, gmat):

        self.inp = inp
        self.disg = result
        self.reac = np.zeros([self.inp.n], dtype=np.float64)  # Section force vector
        self.fsec = np.zeros([12, self.inp.nmember], dtype=np.float64)  # Section force vector

        # recovery of restricted displacements
        keys = list(inp.node)
        for ID in inp.mpfix:
            fix = inp.mpfix[ID]
            i = keys.index(ID)
            for j in range(0,self.inp.nfree):
                value = fix[j]
                iz=i*self.inp.nfree+j
                if value==1:
                    self.disg[iz]=0
                elif value != 0:
                    # バネ値がある場合
                    self.reac[iz] =self.disg[iz]*value

        # calculation of section force
        work =np.zeros(12, dtype=np.float64)         # work vector for section force calculation
        for ne in range(0,self.inp.nmember):
            k = gmat.kmat[ne]

            i     = k.iNo
            j     = k.jNo 
            ek    = k.ek    # Stiffness matrix in local coordinate
            tt    = k.tt    # Transformation matrix
            E     = k.ee    # elastic modulus
            AA    = k.aa    # section area
            alpha = k.alpha # thermal expansion coefficient
            tempe = k.wte   #0.5*(self.inp.deltaT[i]+self.inp.deltaT[j])

            work[0]=self.disg[6*i]  ; work[1] =self.disg[6*i+1]; work[2]= self.disg[6*i+2]
            work[3]=self.disg[6*i+3]; work[4] =self.disg[6*i+4]; work[5]= self.disg[6*i+5]
            work[6]=self.disg[6*j]  ; work[7] =self.disg[6*j+1]; work[8]= self.disg[6*j+2]
            work[9]=self.disg[6*j+3]; work[10]=self.disg[6*j+4]; work[11]=self.disg[6*j+5]

            self.fsec[:,ne]=np.dot(ek,np.dot(tt,work))
            self.fsec[0,ne]=self.fsec[0,ne]+E*AA*alpha*tempe
            self.fsec[6,ne]=self.fsec[6,ne]-E*AA*alpha*tempe


    def getDictionary(self):

        dict_Json = {}

        # calc state input
        dict_Json['node'] = self.inp.node
        dict_Json['member'] = self.inp.member

        #変位
        dict_disg = OrderedDict()
        keys = list(self.inp.node)
        for i in range(0,self.inp.nnode):

            iz=i*self.inp.nfree
            dict = {
                    "dx":self.disg[iz+0], \
                    "dy":self.disg[iz+1], \
                    "dz":self.disg[iz+2], \
                    "rx":self.disg[iz+3], \
                    "ry":self.disg[iz+4], \
                    "rz":self.disg[iz+5]
                    }
            dict_disg[keys[i]] = dict 

        #反力
        dict_reac = OrderedDict()
        keys = list(self.inp.node)
        for i in range(0,self.inp.nnode):

            iz=i*self.inp.nfree
            dict = {
                    "tx":self.reac[iz+0], \
                    "ty":self.reac[iz+1], \
                    "tz":self.reac[iz+2], \
                    "mx":self.reac[iz+3], \
                    "my":self.reac[iz+4], \
                    "mz":self.reac[iz+5]
                    }
            dict_reac[keys[i]] = dict 

        #断面力
        dict_fsec = OrderedDict()
        keys = list(self.inp.member)
        for ne in range(0,self.inp.nmember):
            dict = {
                    "fxi":self.fsec[ 0,ne], \
                    "fyi":self.fsec[ 1,ne], \
                    "fzi":self.fsec[ 2,ne], \
                    "mxi":self.fsec[ 3,ne], \
                    "myi":self.fsec[ 4,ne], \
                    "mzi":self.fsec[ 5,ne], \
                    "fxj":self.fsec[ 6,ne], \
                    "fyj":self.fsec[ 7,ne], \
                    "fzj":self.fsec[ 8,ne], \
                    "mxj":self.fsec[ 9,ne], \
                    "myj":self.fsec[10,ne], \
                    "mzj":self.fsec[11,ne]
                    }
            dict_fsec[keys[ne]] = dict 

        dict_Json['disg'] = dict_disg
        dict_Json['reac'] = dict_reac
        dict_Json['fsec'] = dict_fsec
        return dict_Json
 
