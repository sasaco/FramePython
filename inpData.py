
import numpy as np

class inpData:

    def __init__(self, fnameR):
        f=open(fnameR,'r')
        self.setdata(f)
        f.close()

    def setdata(self, f):
        text=f.readline()
        text=text.strip()
        text=text.split()
        self.npoin=int(text[0]) # Number of nodes
        self.nele =int(text[1]) # Number of elements
        self.nsec =int(text[2]) # Number of sections
        self.npfix=int(text[3]) # Number of restricted nodes
        self.nlod =int(text[4]) # Number of loaded nodes

        self.nod=2              # Number of nodes per element
        self.nfree=6            # Degree of freedom per node
        self.n12=self.nod*self.nfree            
        self.n  = self.nfree*self.npoin

        self.x     =np.zeros([3, self.npoin], dtype=np.float64)         # Coordinates of nodes
        self.deltaT=np.zeros(self.npoin, dtype=np.float64)             # Temperature change of nodes
        self.ae    =np.zeros([12, self.nsec], dtype=np.float64)   # Section characteristics
        self.node  =np.zeros([self.nod+1, self.nele], dtype=np.int)    # Node-element relationship
        self.fp    =np.zeros(self.nfree*self.npoin,dtype=np.float64)       # External force vector
        self.mpfix =np.zeros([self.nfree, self.npoin],dtype=np.int)         # Ristrict conditions
        self.rdis  =np.zeros([self.nfree, self.npoin],dtype=np.float64)     # Ristricted displacement

        # section characteristics
        for i in range(0, self.nsec):
            text=f.readline()
            text=text.strip()
            text=text.split()
            self.ae[0,i] =float(text[0])  # E     : elastic modulus
            self.ae[1,i] =float(text[1])  # po    : Poisson's ratio
            self.ae[2,i] =float(text[2])  # aa    : section area
            self.ae[3,i] =float(text[3])  # aix   : tortional constant
            self.ae[4,i] =float(text[4])  # aiy   : moment of inertia aroutd y-axis
            self.ae[5,i] =float(text[5])  # aiz   : moment of inertia around z-axis
            self.ae[6,i] =float(text[6])  # theta : chord angle
            self.ae[7,i] =float(text[7])  # alpha : thermal expansion coefficient
            self.ae[8,i] =float(text[8])  # gamma : unit weight of material
            self.ae[9,i] =float(text[9])  # gkX   : acceleration in X-direction
            self.ae[10,i]=float(text[10]) # gkY   : acceleration in Y-direction
            self.ae[11,i]=float(text[11]) # gkZ   : acceleration in Z-direction

        # element-node
        for i in range(0, self.nele):
            text=f.readline()
            text=text.strip()
            text=text.split()
            self.node[0,i]=int(text[0]) #node_1
            self.node[1,i]=int(text[1]) #node_2
            self.node[2,i]=int(text[2]) #section characteristic number

        # node coordinates
        for i in range(0, self.npoin):
            text=f.readline()
            text=text.strip()
            text=text.split()
            self.x[0,i]=float(text[0])    # x-coordinate
            self.x[1,i]=float(text[1])    # y-coordinate
            self.x[2,i]=float(text[2])    # z-coordinate
            self.deltaT[i]=float(text[3]) # Temperature change

        # boundary conditions (0:free, 1:restricted)
        for i in range(0, self.npfix):
            text=f.readline()
            text=text.strip()
            text=text.split()
            lp=int(text[0])              #fixed node
            self.mpfix[0,lp-1]=int(text[1])   #fixed in x-direction
            self.mpfix[1,lp-1]=int(text[2])   #fixed in y-direction
            self.mpfix[2,lp-1]=int(text[3])   #fixed in z-direction
            self.mpfix[3,lp-1]=int(text[4])   #fixed in rotation around x-axis
            self.mpfix[4,lp-1]=int(text[5])   #fixed in rotation around y-axis
            self.mpfix[5,lp-1]=int(text[6])   #fixed in rotation around z-axis
            self.rdis[0,lp-1]=float(text[7])  #fixed displacement in x-direction
            self.rdis[1,lp-1]=float(text[8])  #fixed displacement in y-direction
            self.rdis[2,lp-1]=float(text[9])  #fixed displacement in z-direction
            self.rdis[3,lp-1]=float(text[10]) #fixed rotation around x-axis
            self.rdis[4,lp-1]=float(text[11]) #fixed rotation around y-axis
            self.rdis[5,lp-1]=float(text[12]) #fixed rotation around z-axis

        # load
        if 0<self.nlod:
            for i in range(0, self.nlod):
                text=f.readline()
                text=text.strip()
                text=text.split()
                lp=int(text[0])           #loaded node
                self.fp[6*lp-6]=float(text[1]) #load in x-direction
                self.fp[6*lp-5]=float(text[2]) #load in y-direction
                self.fp[6*lp-4]=float(text[3]) #load in z-direction
                self.fp[6*lp-3]=float(text[4]) #moment around x-axis
                self.fp[6*lp-2]=float(text[5]) #moment around y-axis
                self.fp[6*lp-1]=float(text[6]) #moment around z-axis

    def PRINP_3DFRM(self):

        fnameW= 'out_grid.txt'
        fout=open(fnameW,'w')

        # print out of input data
        print('{0:>5s} {1:>5s} {2:>5s} {3:>5s} {4:>5s}'.format('npoin','nele','nsec','npfix','nlod'),file=fout)
        print('{0:5d} {1:5d} {2:5d} {3:5d} {4:5d}'.format(self.npoin,self.nele,self.nsec,self.npfix,self.nlod),file=fout)

        print('{0:>5s} {1:>15s} {2:>15s} {3:>15s} {4:>15s} {5:>15s} {6:>15s} {7:>15s}'
        .format('sec','E','po','A','J','Iy','Iz','theta'),file=fout)
        print('{0:>5s} {1:>15s} {2:>15s} {3:>15s} {4:>15s} {5:>15s}'
        .format('sec','alpha','gamma','gkX','gkY','gkZ'),file=fout)
        for i in range(0,self.nsec):
            print('{0:5d} {1:15.7e} {2:15.7e} {3:15.7e} {4:15.7e} {5:15.7e} {6:15.7e} {7:15.7e}'
            .format(i+1,self.ae[0,i],self.ae[1,i],self.ae[2,i],self.ae[3,i],self.ae[4,i],self.ae[5,i],self.ae[6,i]),file=fout)
            print('{0:5d} {1:15.7e} {2:15.7e} {3:15.7e} {4:15.7e} {5:15.7e}'
            .format(i+1,self.ae[7,i],self.ae[8,i],self.ae[9,i],self.ae[10,i],self.ae[11,i]),file=fout)

        print('{0:>5s} {1:>15s} {2:>15s} {3:>15s} {4:>15s} {5:>15s} {6:>15s} {7:>15s} {8:>15s} {9:>15s} {10:>15s}'
        .format('node','x','y','z','fx','fy','fz','mx','my','mz','deltaT'),file=fout)
        for i in range(0,self.npoin):
            lp=i+1
            print('{0:5d} {1:15.7e} {2:15.7e} {3:15.7e} {4:15.7e} {5:15.7e} {6:15.7e} {7:15.7e} {8:15.7e} {9:15.7e} {10:15.7e}'
            .format(lp,self.x[0,i],self.x[1,i],self.x[2,i],self.fp[6*lp-6],self.fp[6*lp-5],self.fp[6*lp-4],self.fp[6*lp-3],self.fp[6*lp-2],self.fp[6*lp-1],self.deltaT[i]),file=fout)

        print('{0:>5s} {1:>5s} {2:>5s} {3:>5s} {4:>5s} {5:>5s} {6:>5s} {7:>15s} {8:>15s} {9:>15s} {10:>15s} {11:>15s} {12:>15s}'
        .format('node','kox','koy','koz','kmx','kmy','kmz','rdis_x','rdis_y','rdis_z','rrot_x','rrot_y','rrot_z'),file=fout)
        for i in range(0,self.npoin):
            if 0<self.mpfix[0,i]+self.mpfix[1,i]+self.mpfix[2,i]+self.mpfix[3,i]+self.mpfix[4,i]+self.mpfix[5,i]:
                lp=i+1
                print('{0:5d} {1:5d} {2:5d} {3:5d} {4:5d} {5:5d} {6:5d} {7:15.7e} {8:15.7e} {9:15.7e} {10:15.7e} {11:15.7e} {12:15.7e}'
                .format(lp,self.mpfix[0,i],self.mpfix[1,i],self.mpfix[2,i],self.mpfix[3,i],self.mpfix[4,i],self.mpfix[5,i],self.rdis[0,i],self.rdis[1,i],self.rdis[2,i],self.rdis[3,i],self.rdis[4,i],self.rdis[5,i]),file=fout)

        print('{0:>5s} {1:>5s} {2:>5s} {3:>5s}'.format('elem','i','j','sec'),file=fout)
        for ne in range(0,self.nele):
            print('{0:5d} {1:5d} {2:5d} {3:5d}'.format(ne+1,self.node[0,ne],self.node[1,ne],self.node[2,ne]),file=fout)

        fout.close()
