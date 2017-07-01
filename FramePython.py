# ======================
# 3D Frame Analysis
# ======================
import numpy as np

from inpData import inpData
from kMatrix import kMatrix
from gMatrix import gMatrix
from fMatrix import fMatrix
from outData import outData

class FramePython:


    def Nonlinear3D(self, input):
        inp = input

        gmat = gMatrix(inp.n)
        fmat = fMatrix(inp)

        for ID in inp.member:
            k=kMatrix(inp, ID)
            gmat.set_kMatrix(k) # assembly of stiffness matrix
            fmat.set_fMatrix(k) # assembly of load vectors


        # treatment of boundary conditions
        keys = list(inp.node)
        for ID in inp.mpfix:
            fix = inp.mpfix[ID]
            i = keys.index(ID)
            for j in range(0,inp.nfree):
                value = fix[j]
                if value == 1:
                    # 固定支点の場合荷重を削除し剛性を...どうにかする
                    iz=i*inp.nfree+j
                    fmat.fp[iz]=0.0
                    for k in range(0,inp.n):
                        gmat.gk[k,iz]=0.0
                    gmat.gk[iz,iz]=1.0
                elif value != 0:
                    # バネ値がある場合対角成分にバネ剛性を加算する
                    iz=i*inp.nfree+j
                    gmat.gk[iz,iz] += value

        # solution of simultaneous linear equations
        result = np.linalg.solve(gmat.gk, fmat.fp)

        out = outData(inp, result, gmat)
        return out

