
import numpy as np
from kMatrix   import kMatrix

class fMatrix:

    def __init__(self, inp):

        self.fp = np.zeros(inp.n, dtype=np.float64) # External force vector

        lp = 0        
        for ID in inp.node:
            temp = np.zeros([inp.nfree], dtype=np.float64)
    
            for text in inp.load_node:
                if ID == str(text['n']):
                    self.fp[6*lp+0] += float(text['tx']) if 'tx' in text else 0  # load in x-direction
                    self.fp[6*lp+1] += float(text['ty']) if 'ty' in text else 0  # load in y-direction
                    self.fp[6*lp+2] += float(text['tz']) if 'tz' in text else 0  # load in z-direction
                    self.fp[6*lp+3] += float(text['rx']) if 'rx' in text else 0  # moment around x-axis
                    self.fp[6*lp+4] += float(text['ry']) if 'ry' in text else 0  # moment around y-axis
                    self.fp[6*lp+5] += float(text['rz']) if 'rz' in text else 0  # moment around z-axis
            lp += 1


    def set_fMatrix(self, k):
        tt    = k.tt
        wfe_l = self.WBUNPU_3DFRM(k)
        wfe   = np.dot(tt.T,wfe_l)    # Thermal load vector in global coordinate

        tfe_l = self.TFVEC_3DFRM(k)
        tfe   = np.dot(tt.T,tfe_l)    # Thermal load vector in global coordinate

        for i in range(0,12):
            it=k.ir[i]
            self.fp[it]=self.fp[it]+wfe[i]+tfe[i]


    def WBUNPU_3DFRM(self, k):
        wfe_l = np.zeros(12,dtype=np.float64)
        el    = k.el 

        # 軸力（x軸方向力）
        wfe_l[0]  =  el/6 * (2 * k.wxi + k.wxj)
        wfe_l[6]  =  el/6 * (k.wxi + 2 * k.wxj)
        # x軸回りモーメント（ねじりモーメント）
        if k.k1x ==1 and k.k2x ==1:   # 両端剛結合
            wfe_l[3]  =  el/6 * (2 * k.wti + k.wtj)
            wfe_l[9]  =  el/6 * (k.wti + 2 * k.wtj)
        elif k.k1x ==1 and k.k2x ==0: # j端ピン結合
            wfe_l[3]  =  el * (k.wti + k.wtj)/2
            wfe_l[9]  =  0
        elif k.k1x ==0 and k.k2x ==1: # i端ピン結合
            wfe_l[3]  =  0
            wfe_l[9]  =  el * (k.wti + k.wtj)/2

        # y軸方向せん断力
        wfe_l[1]  =  el/20 * (7 * k.wyi + 3 * k.wyj)
        wfe_l[7]  =  el/20 * (3 * k.wyi + 7 * k.wyj)
        # z軸回り曲げモーメント
        if k.k1y ==1 and k.k2y ==1:   # 両端剛結合
            wfe_l[5]  =  (el**2)/60 * (3 * k.wyi + 2 * k.wyj)
            wfe_l[11] = -(el**2)/60 * (2 * k.wyi + 3 * k.wyj)
        elif k.k1y ==1 and k.k2y ==0: # j端ピン結合
            wfe_l[5]  =  (el**2)/6 * (k.wyi + 2 * k.wyj)
            wfe_l[11] = 0
        elif k.k1y ==0 and k.k2y ==1: # i端ピン結合
            wfe_l[5]  = 0
            wfe_l[11] = (el**2)/6 * (2 * k.wyi + k.wyj)

        # z軸方向せん断力
        wfe_l[2]  =  el/20 * (7 * k.wzi + 3 * k.wzj)
        wfe_l[8]  =  el/20 * (3 * k.wzi + 7 * k.wzj)
        # y軸回り曲げモーメント
        if k.k1z ==1 and k.k2z ==1:   # 両端剛結合
            wfe_l[4]  = -(el**2)/60 * (3 * k.wzi + 2 * k.wzj)
            wfe_l[10] =  (el**2)/60 * (2 * k.wzi + 3 * k.wzj)
        elif k.k1z ==1 and k.k2z ==0: # j端ピン結合
            wfe_l[4]  =  (el**2)/6 * (k.wzi + 2 * k.wzj)
            wfe_l[10] = 0
        elif k.k1z ==0 and k.k2z ==1: # i端ピン結合
            wfe_l[4]  = 0
            wfe_l[10] = (el**2)/6 * (2 * k.wzi + k.wzj)

        return wfe_l


    def TFVEC_3DFRM(self, k):
        # Thermal load vector  in local coordinate system
        tfe_l    = np.zeros(12,dtype=np.float64)
        i        = k.iNo  
        j        = k.jNo 
        E        = k.ee    # elastic modulus
        AA       = k.aa    # section area
        alpha    = k.alpha # thermal expansion coefficient
        tempe    = k.wte   # 0.5*(self.inp.deltaT[i]+self.inp.deltaT[j])
        tfe_l[0] =-E*AA*alpha*tempe
        tfe_l[6] = E*AA*alpha*tempe
        return tfe_l



