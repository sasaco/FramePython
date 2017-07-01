
import numpy as np
import json
from collections import OrderedDict
import copy
from tMatrix import tMatrix

class inpData:

    def rText(self):
        fnameR= 'inp_grid.json'
        f = open(fnameR)
        fstr = f.read()  # ファイル終端まで全て読んだデータを返す
        f.close()
        self.setJSON(fstr)


    def setJSON(self, fstr):

        js = json.loads(fstr, object_pairs_hook=OrderedDict) 

        self.node        = js['node']
        self.member      = js['member']
        for ID in self.member:
            m = self.member[ID]
            m['ni'] = str(m['ni'])
            m['nj'] = str(m['nj'])
            m['e'] = str(m['e'])
            L = self.GetLength(ID)  
            m['L'] = L
           
        self.element     = js['element']

        if 'fix_node' in js:
            self.fix_node = js['fix_node'] 
            for fn in self.fix_node:
                fn['n'] = str(fn['n'])
        else:
            self.fix_node = []

        if 'fix_member' in js:
            self.fix_member = js['fix_member']
            for fm in self.fix_member:
                fm['m'] = str(fm['m'])
        else:
           self.fix_member  = []  
           
        if 'load_node' in js:
           self.load_node = js['load_node']
           for ln in self.load_node:
                ln['n'] = str(ln['n'])
        else:
           self.load_node = [] 
           
        if 'load_member' in js:
           self.load_member = js['load_member']
           for lm in self.load_member:
                lm['m'] = str(lm['m'])
        else:
           self.load_member = []

        #解析用変数をセット
        self.nod  = 2   # Number of nodes per member
        self.nfree= 6   # Degree of freedom per node

        # 支点条件を整理し解析用変数にセットする
        self.mpfix = OrderedDict()
        self.set_node_fix()

        # 要素荷重を整理し解析用変数にセットする
        self.fe = OrderedDict()
        self.set_load_member()


        #解析用変数をセット
        self.nnode   = len(self.node)            # Number of nodes
        self.nmember = len(self.member)       # Number of elements

        self.n    = self.nfree*self.nnode


    def set_node_fix(self):
        # treatment of boundary conditions
        for ID in self.node:
            fix = np.zeros([self.nfree], dtype = np.float64)
            for text in self.fix_node:
                if ID == text['n']:
                    fix[0] += float(text['tx']) if 'tx' in text else 0  #fixed in x-direction
                    fix[1] += float(text['ty']) if 'ty' in text else 0  #fixed in y-direction
                    fix[2] += float(text['tz']) if 'tz' in text else 0  #fixed in z-direction
                    fix[3] += float(text['rx']) if 'rx' in text else 0  #fixed in rotation around x-axis
                    fix[4] += float(text['ry']) if 'ry' in text else 0  #fixed in rotation around y-axis
                    fix[5] += float(text['rz']) if 'rz' in text else 0  #fixed in rotation around z-axis
            self.mpfix[ID] = fix
 

    def set_load_member(self):
        if len(self.load_member) < 1: 
            return

        mo = {}
        for load in self.load_member:
            ID = load['m']        
            if not ID in mo:
                mo[ID] = []
            mo[ID].append(load)

        # 部材単位で、分割点を決定し、各荷重が子部材
        for ID in mo:
            parent_member = self.member[ID]
            L = parent_member['L']

            # 同じ部材 に載荷する全ての分布荷重 分割点 を登録-------------------------------------------
            new_distance = []
            for load in mo[ID]:
                L1 = float(load['L1'])
                L2 = float(load['L2'])

                if  L1 >0:
                    if not L1 in new_distance:
                        new_distance.append(L1)
                elif  L1 <0: 
                    raise Exception('Member Load L1 as Negative number')

                if  L2 >0:
                    L3 = L-L2                     
                    if  L3 <0: 
                        raise Exception('Member Load L2 as Negative number')
                    if not L3 in new_distance:
                        new_distance.append(L3)

            if len( new_distance)==0:

                # 部材に対して荷重を載せる -------------------------------------------
                for load in mo[ID]:
                    mk = int(load['mark'])
                    L1 = float(load['L1'])
                    L2 = float(load['L2'])

                    if mk == 1:
                        IDi   = parent_member['ni']
                        IDj   = parent_member['nj']
                        pID = IDi if L1==0 else IDj
                        self.set_load_mk1_node(pID, load['direction'], load['P1'], parent_member)
                        pID = IDi if L2==0 else IDj
                        self.set_load_mk1_node(pID, load['direction'], load['P2'], parent_member)

                    elif mk == 2:
                        if L1+L2 < L:
                            self.set_load_mk2(ID, load['direction'], load['P1'], load['P2'], parent_member)
                        
                    elif mk == 9:
                        self.set_load_mk9(ID, load['P1'])


            else:
                new_distance.sort()  

                # 各分割部材 における 分布荷重値 -------------------------------------------
                new_members = OrderedDict()
                IDi   = parent_member['ni']
                pi = self.node[IDi]
                i = 1
                for pos in new_distance:
                    new_memberID = str(ID) + 'w' + str(i)

                    # 新しい j端 を用意する
                    IDj  = new_memberID
                    pj = self.GetMidPoint(ID, pos)
                    self.node[IDj] = pj

                    # 部材を作成
                    new_member = copy.copy(parent_member)
                    new_member['ni'] = IDi
                    new_member['nj'] = IDj
                    new_member['L'] = self.GetDistance(pi, pj)
                    new_members[new_memberID] = new_member
                    # 
                    IDi = IDj   
                    pi = pj
                    i += 1

                else: 
                    IDj = parent_member['nj']
                    pj = self.node[IDj]
                    new_memberID = ID + 'w' + str(i)
                    new_member = copy.copy(parent_member)
                    new_member['ni'] = IDi
                    new_member['nj'] = IDj
                    new_member['L'] = self.GetDistance(pi, pj)
                    new_members[new_memberID] = new_member
 

                # 新しい部材に対して荷重を載せる -------------------------------------------
                for load in mo[ID]:
                    mk = int(load['mark'])

                    if mk == 1:
                        self.set_load_mk1(parent_member, load, new_members)

                    elif mk == 2:
                        self.set_load_mk29(parent_member, load, new_members)
                        
                    elif mk == 9:
                        self.set_load_mk29(parent_member, load, new_members)

                # 前の部材を削除して新しい部材を登録する -------------------------------------------
                if len(new_members) > 0:
                    # 要素バネの入力をコピー登録
                    if ID in self.fix_member:
                        mefix = self.fix_member[ID]
                        for new_memberID in new_members:
                            self.fix_member[new_memberID] = mefix
                        del self.fix_member[ID]

                    # 要素を登録
                    for new_memberID in new_members:
                        new_member = new_members[new_memberID]
                        self.member[new_memberID] = new_member
                    del self.member[ID]


    def set_load_mk29(self, parent_member, load, new_members):

        mk = int(load['mark'])

        L =  parent_member['L']
        L1 = load['L1']
        L2 = load['L2']
        L3 = L-L2 
        Lo =  L-(L1+L2)

        load_direct = str(load['direction'])
        P1 = float(load['P1'])
        P2 = float(load['P2'])
        # 単位長さ当りの荷重
        Pd = (P2-P1)/Lo

        targets = OrderedDict()

        # 同じ位置の節点を探す
        Length = 0
        key = 0
        for new_memberID in new_members:
            new_member = new_members[new_memberID]                        

            if key == 0:
                if Length >= L1:
                    new_member['ID'] = new_memberID
                    targets['start'] = new_member
                    key == 1

            Length += new_member['L']

            if Length >= L3:
                st = targets['start']
                if new_memberID != st['ID']:
                    new_member['ID'] = new_memberID
                    targets['end'] = new_member
                break
            elif key > 0:
                new_member['ID'] = new_memberID
                targets[str(key)] = new_member
                key += 1

        else:
            if not 'end' in targets:
                keys = list(new_members.keys)
                new_memberID = keys[-1]
                new_member = new_members[new_memberID]
                new_member['ID'] = new_memberID
                targets['end'] = new_member


        # 荷重を入力する
        if mk == 2:
            Pi = P1
            Lj = 0
            for target_memberID in targets:
                target_member = targets[target_memberID]
                Lj += target_member['L']
                Pj = P1 + Pd * Lj
                ID = target_member['ID']
                self.set_load_mk2(ID, load_direct, Pi, Pj, target_member)
                Pi = Pj

        elif mk == 9:
            for target_memberID in targets:
                target_member = targets[target_memberID]
                ID = target_member['ID']
                self.set_load_mk9(ID, P1)

    def set_load_mk1(self, parent_member, load, new_members):

        L =  parent_member['L']
        L1 = load['L1']
        L2 = load['L2']
        L3 = L-L2 

        direct = str(load['direction'])
        P1 = float(load['P1'])
        P2 = float(load['P2'])

        targets = {}

        if L1 == 0:
            IDi = str(parent_member['ni'])
            # IDi に節点荷重を追加する
            self.set_load_mk1_node(IDi, direct, P1, parent_member)
        elif L1 == L:
            IDj = str(parent_member['nj'])
            # IDj に節点荷重を追加する
            self.set_load_mk1_node(IDj, direct, P1, parent_member)
        else:
            targets[L1] = P1

        if L2 == 0:
            IDj = str(parent_member['nj'])
            # IDj に節点荷重を追加する
            self.set_load_mk1_node(IDj, direct, P2, parent_member)
        elif L2 == L:
            IDi = str(parent_member['ni'])
            # IDi に節点荷重を追加する
            self.set_load_mk1_node(IDi, direct, P1, parent_member)
        else:
            targets[L3] = P2

        # 同じ位置の節点を探す
        Length = 0
        for new_memberID in new_members:
            new_member = new_members[new_memberID]                        
            Length += new_member['L']
            for pos in targets:
                if pos == Length:
                    IDj = str(new_member['nj'])
                    P = targets[pos]
                    # IDj に節点荷重を追加する
                    self.set_load_mk1_node(IDj, direct, P, parent_member)
                    break

    def set_load_mk1_node(self, target_node_ID, load_direct, load_value, target_member):

        if load_value == 0:
            return

        if load_direct == "gx":
            self.fp[target_node_ID][0] += load_value
        elif load_direct == "gy":
            self.fp[target_node_ID][1] += load_value
        elif load_direct == "gz":
            self.fp[target_node_ID][2] += load_value
        else:
            IDi   = str(target_member['ni'])
            IDj   = str(target_member['nj'])
            pi = self.node[IDi]
            pj = self.node[IDj]
            t = tMatrix([pi['x'],pi['y'],pi['z']],[pj['x'],pj['y'],pj['z']],target['cg'])

            if load_direct == "x":
                re = t.world_vector([load_value,0,0])
            elif load_direct == "y":
                re = t.world_vector([0,load_value,0])
            elif load_direct == "z":
                re = t.world_vector([0,0,load_value])
            self.fp[target_node_ID][0] += re[0]
            self.fp[target_node_ID][1] += re[1]
            self.fp[target_node_ID][2] += re[2]



    def GetLength(self, ID):
        target = self.member[ID]
        IDi   = target['ni']
        IDj   = target['nj']
        pi = self.node[IDi]
        pj = self.node[IDj]

        return self.GetDistance(pi, pj)

    def GetDistance(self, pi, pj):
        xx = pj['x']-pi['x']
        yy = pj['y']-pi['y']
        zz = pj['z']-pi['z']
        return np.sqrt(xx**2+yy**2+zz**2)

    def GetMidPoint(self, ID, L1):
        target = self.member[ID]
        IDi   = target['ni']
        IDj   = target['nj']
        pi = self.node[IDi]
        pj = self.node[IDj]

        x1 = pi['x']
        y1 = pi['y']
        z1 = pi['z']

        x2 = pj['x']
        y2 = pj['y']
        z2 = pj['z']

        xx = x2-x1
        yy = y2-y1
        zz = z2-z1
        L= np.sqrt(xx**2+yy**2+zz**2)

        result = OrderedDict()
        n = L1 / L

        result['x'] = x1 + (x2 - x1) * n
        result['y'] = y1 + (y2 - y1) * n
        result['z'] = z1 + (z2 - z1) * n

        return result

    def set_load_mk9(self, ID, P1):

        le =  self.fe[ID] if ID in self.fe else np.zeros([9], dtype=np.float64) 
        le[8] += P1 # Temperature change of element
        self.fe[ID] = le

    def set_load_mk2(self, ID, load_direct, Pi, Pj, target_member):

        le =  self.fe[ID] if ID in self.fe else np.zeros([9], dtype=np.float64) 

        if load_direct == "x" or str(load_direct) == "1":
            le[0] += Pi # wxi
            le[1] += Pj # wxj 
        elif load_direct == "y" or str(load_direct) == "2":
            le[2] += Pi # wyi
            le[3] += Pj # wyj 
        elif load_direct == "z" or str(load_direct) == "3":
            le[4] += Pi # wzi
            le[5] += Pj # wzj 
        elif load_direct == "r" or str(load_direct) == "4":
            le[6] += Pi # wri
            le[7] += Pj # wrj 
        else:
            IDi   = target_member['ni']
            IDj   = target_member['nj']
            pi = self.node[IDi]
            pj = self.node[IDj]
            t = tMatrix([pi['x'],pi['y'],pi['z']],[pj['x'],pj['y'],pj['z']], target_member['cg'])

            if load_direct == "gx" or str(load_direct) == "5":
                Pii = t.get_member_vector([Pi,0,0])
                Pjj = t.get_member_vector([Pj,0,0])
            elif load_direct == "gy" or str(load_direct) == "6":
                Pii = t.get_member_vector([0,Pi,0])
                Pjj = t.get_member_vector([0,Pj,0])
            elif load_direct == "gz" or str(load_direct) == "7":
                Pii = t.get_member_vector([0,0,Pi])
                Pjj = t.get_member_vector([0,0,Pj])

            le[0] += Pii[0] # wxi
            le[1] += Pjj[0] # wxj 
            le[2] += Pii[1] # wyi
            le[3] += Pjj[1] # wyj 
            le[4] += Pii[2] # wzi
            le[5] += Pjj[2] # wzj 

        self.fe[ID] = le