
import numpy as np
from inpData import inpData
from kMatrix   import kMatrix


class gMatrix:

    def __init__(self, n):
        self.gk = np.zeros([n,n], dtype=np.float64)             # Global stiffness matrix
        self.kmat = {}

    def set_kMatrix(self, k):
        self.kmat[k.ne] = k

        ck = k.ck()

        for i in range(0,12):
            it=k.ir[i]
            for j in range(0,12):
                jt=k.ir[j]
                self.gk[it,jt]=self.gk[it,jt]+ck[i,j]

