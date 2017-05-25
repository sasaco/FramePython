# ======================
# 3D Frame Analysis
# ======================
import numpy as np
import sys
import time

from inpData import inpData
from kMatrix import kMatrix
from gMatrix import gMatrix
from fMatrix import fMatrix
from outData import outData

# Main routine
start=time.time()

fnameR= 'inp_grid.txt'
fnameW= 'out_grid.txt'

inp = inpData(fnameR)
inp.PRINP_3DFRM()

gmat = gMatrix(inp.n)
fmat = fMatrix(inp)
for ne in range(0,inp.nele):
    k= kMatrix(ne, inp)
    gmat.set_kMatrix(k) # assembly of stiffness matrix
    fmat.set_fMatrix(k) # assembly of load vectors

# treatment of boundary conditions
for i in range(0,inp.npoin):
    for j in range(0,inp.nfree):
        if inp.mpfix[j,i]==1:
            iz=i*inp.nfree+j
            fmat.fp[iz]=0.0
            for k in range(0,inp.n):
                fmat.fp[k]=fmat.fp[k]-inp.rdis[j,i]*gmat.gk[k,iz]
                gmat.gk[k,iz]=0.0
            gmat.gk[iz,iz]=1.0


# solution of simultaneous linear equations
result = np.linalg.solve(gmat.gk, fmat.fp)

out = outData(inp, result, gmat)
out.PROUT_3DFRM(fnameW)

dtime=time.time()-start
print('n={0}  time={1:.3f}'.format(inp.n,dtime)+' sec')
fout=open(fnameW,'a')
print('n={0}  time={1:.3f}'.format(inp.n,dtime)+' sec',file=fout)
fout.close()
