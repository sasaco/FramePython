
import numpy as np
from inpData import inpData

class kMatrix:

    def __init__(self, ne, input):
        self.ne = ne
        self.inp = input

        self.iNo = self.inp.node[0,self.ne]
        self.jNo = self.inp.node[1,self.ne]
        self.eNo = self.inp.node[2,self.ne]
        i = self.iNo-1
        j = self.jNo-1
        self.x1= self.inp.x[0,i]
        self.y1= self.inp.x[1,i]
        self.z1= self.inp.x[2,i]
        self.x2= self.inp.x[0,j]
        self.y2= self.inp.x[1,j]
        self.z2= self.inp.x[2,j]

        xx = self.x2-self.x1
        yy = self.y2-self.y1
        zz = self.z2-self.z1
        self.el = np.sqrt(xx**2+yy**2+zz**2)
        m  = self.eNo-1
        self.ee    = self.inp.ae[0,m]  # elastic modulus
        self.po    = self.inp.ae[1,m]  # Poisson's ratio
        self.aa    = self.inp.ae[2,m]  # section area
        self.aix   = self.inp.ae[3,m]  # tortional constant
        self.aiy   = self.inp.ae[4,m]  # moment of inertia around y-axis
        self.aiz   = self.inp.ae[5,m]  # moment of inertia around z-axis
        self.theta = self.inp.ae[6,m]  # theta : chord angle
        self.alpha = self.inp.ae[7,m]  # alpha : thermal expansion coefficient
        self.gamma = self.inp.ae[8,m]  # gamma : unit weight of material
        self.gkX   = self.inp.ae[9,m]  # gkX   : acceleration in X-direction
        self.gkY   = self.inp.ae[10,m] # gkY   : acceleration in Y-direction
        self.gkZ   = self.inp.ae[11,m] # gkZ   : acceleration in Z-direction

        self.GJ=self.ee/2/(1+self.po)*self.aix
        self.EA=self.ee*self.aa
        self.EIy=self.ee*self.aiy
        self.EIz=self.ee*self.aiz

        # Work vector for matrix assembly
        ir = np.zeros(12, dtype=np.int)             
        ir[11]=6*j+5; ir[10]=ir[11]-1; ir[9]=ir[10]-1; ir[8]=ir[9]-1; ir[7]=ir[8]-1; ir[6]=ir[7]-1
        ir[5] =6*i+5; ir[4] =ir[5]-1 ; ir[3]=ir[4]-1 ; ir[2]=ir[3]-1; ir[1]=ir[2]-1; ir[0]=ir[1]-1
        self.ir = ir

        self.ek = self.SM_3DFRM()
        self.tt = self.TM_3DFRM()


    def SM_3DFRM(self):
        ek = np.zeros([12,12],dtype=np.float64) # local stiffness matrix
        ek[ 0, 0]= self.EA/self.el
        ek[ 0, 6]=-self.EA/self.el
        ek[ 1, 1]= 12*self.EIz/self.el**3
        ek[ 1, 5]=  6*self.EIz/self.el**2
        ek[ 1, 7]=-12*self.EIz/self.el**3
        ek[ 1,11]=  6*self.EIz/self.el**2
        ek[ 2, 2]= 12*self.EIy/self.el**3
        ek[ 2, 4]= -6*self.EIy/self.el**2
        ek[ 2, 8]=-12*self.EIy/self.el**3
        ek[ 2,10]= -6*self.EIy/self.el**2
        ek[ 3, 3]= self.GJ/self.el
        ek[ 3, 9]=-self.GJ/self.el
        ek[ 4, 2]= -6*self.EIy/self.el**2
        ek[ 4, 4]=  4*self.EIy/self.el
        ek[ 4, 8]=  6*self.EIy/self.el**2
        ek[ 4,10]=  2*self.EIy/self.el
        ek[ 5, 1]=  6*self.EIz/self.el**2
        ek[ 5, 5]=  4*self.EIz/self.el
        ek[ 5, 7]= -6*self.EIz/self.el**2
        ek[ 5,11]=  2*self.EIz/self.el
        ek[ 6, 0]=-self.EA/self.el
        ek[ 6, 6]= self.EA/self.el
        ek[ 7, 1]=-12*self.EIz/self.el**3
        ek[ 7, 5]= -6*self.EIz/self.el**2
        ek[ 7, 7]= 12*self.EIz/self.el**3
        ek[ 7,11]= -6*self.EIz/self.el**2
        ek[ 8, 2]=-12*self.EIy/self.el**3
        ek[ 8, 4]=  6*self.EIy/self.el**2
        ek[ 8, 8]= 12*self.EIy/self.el**3
        ek[ 8,10]=  6*self.EIy/self.el**2
        ek[ 9, 3]=-self.GJ/self.el
        ek[ 9, 9]= self.GJ/self.el
        ek[10, 2]= -6*self.EIy/self.el**2
        ek[10, 4]=  2*self.EIy/self.el
        ek[10, 8]=  6*self.EIy/self.el**2
        ek[10,10]=  4*self.EIy/self.el
        ek[11, 1]=  6*self.EIz/self.el**2
        ek[11, 5]=  2*self.EIz/self.el
        ek[11, 7]= -6*self.EIz/self.el**2
        ek[11,11]=  4*self.EIz/self.el
        return ek


    def TM_3DFRM(self):
        tt=np.zeros([12,12],dtype=np.float64) # transformation matrix
        t1=np.zeros([3,3],dtype=np.float64)
        t2=np.zeros([3,3],dtype=np.float64)
        theta=np.radians(self.theta)#(self.inp.ae[6,m]) # chord angle
        t1[0,0]=1
        t1[1,1]= np.cos(theta)
        t1[1,2]= np.sin(theta)
        t1[2,1]=-np.sin(theta)
        t1[2,2]= np.cos(theta)
        ll=(self.x2-self.x1)/self.el
        mm=(self.y2-self.y1)/self.el
        nn=(self.z2-self.z1)/self.el
        if self.x2-self.x1==0.0 and self.y2-self.y1==0.0:
            t2[0,2]=nn
            t2[1,0]=nn
            t2[2,1]=1.0
        else:
            qq=np.sqrt(ll**2+mm**2)
            t2[0,0]=ll
            t2[0,1]=mm
            t2[0,2]=nn
            t2[1,0]=-mm/qq
            t2[1,1]= ll/qq
            t2[2,0]=-ll*nn/qq
            t2[2,1]=-mm*nn/qq
            t2[2,2]=qq
        t3=np.dot(t1,t2)
        tt[0:3,0:3]  =t3[0:3,0:3]
        tt[3:6,3:6]  =t3[0:3,0:3]
        tt[6:9,6:9]  =t3[0:3,0:3]
        tt[9:12,9:12]=t3[0:3,0:3]
        return tt

    def ck(self):
        return np.dot(np.dot(self.tt.T,self.ek),self.tt)                # Stiffness matrix in global coordinate

