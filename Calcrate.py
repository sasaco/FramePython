import csv

class Calcrate:



    def __init__(self):

        self.入力シート名1 = "入力1"
        self.入力シート名2 = "入力2"
        self.出力シート名 = "計算・出力"

        self.配列上限 = 1285200
        self.MAX節点 = 100
        self.MAX材料 = 100
        self.MAX要素 = 100
        self.MAX集中荷重 = 600
        self.MAX分布荷重 = 100
        self.MAX拘束条件 = 100

        self.節点数       = 0
        self.節点X        = [0.0] * self.MAX節点
        self.節点Y        = [0.0] * self.MAX節点
        self.節点Z        = [0.0] * self.MAX節点

        self.材料数       = 0
        self.弾性係数     = [0.0] * self.MAX材料
        self.gk           = [0.0] * self.MAX材料
        self.断面積       = [0.0] * self.MAX材料
        self.yi           = [0.0] * self.MAX材料
        self.zi           = [0.0] * self.MAX材料

        self.要素数       = 0
        self.要素節点     = [[0]  * self.MAX要素] * 2
        self.要素材料     = [0]   * self.MAX要素
        self.fai          = [0.0] * self.MAX要素

        self.集中荷重数   = 0
        self.集中荷重節点 = [0]   * self.MAX集中荷重
        self.fx           = [0.0] * self.MAX集中荷重
        self.fy           = [0.0] * self.MAX集中荷重
        self.fz           = [0.0] * self.MAX集中荷重
        self.fmx          = [0.0] * self.MAX集中荷重
        self.fmy          = [0.0] * self.MAX集中荷重
        self.fmz          = [0.0] * self.MAX集中荷重

        self.拘束条件数   = 0
        self.拘束条件節点 = [0]   * self.MAX拘束条件
        self.nxfx         = [0]   * self.MAX拘束条件
        self.nyfx         = [0]   * self.MAX拘束条件
        self.nzfx         = [0]   * self.MAX拘束条件
        self.mxfx         = [0]   * self.MAX拘束条件
        self.myfx         = [0]   * self.MAX拘束条件
        self.mzfx         = [0]   * self.MAX拘束条件

        self.分布荷重数   = 0
        self.分布荷重節点 = [[0]  * self.MAX分布荷重] * 2
        self.wx           = [0.0] * self.MAX分布荷重
        self.wy           = [0.0] * self.MAX分布荷重
        self.wz           = [0.0] * self.MAX分布荷重

        self.ID           = [[0]  * 6] * self.MAX節点
        self.SE           = [0.0] * 78
        self.AJCB         = [0.0] * self.配列上限
        self.変位         = [[0.0]* self.MAX節点] * 6
        self.FORCE        = [0.0] * ( 6 * self.MAX節点 )
        self.MHT          = [0]   * ( 6 * self.MAX節点 )
        self.MAXA         = [0]   * ( 6 * self.MAX節点 + 1 )
        self.EK           = [[0.0]* 12] * 12
        self.KTR1         = [0]   * self.MAX要素
        self.KTR2         = [0]   * self.MAX要素


    ############################################################
    ##     ３次元　手動入力作成データよりデータを読み込む     ##
    ##          　　　  ** INPUTX.for **                      ##
    ############################################################
    def データ入力(self):

        f = open(self.入力シート名1+'.csv', 'rb')
        csv_obj = csv.render(f)
        Range = [ v for v in csv_obj]

        self.節点数 = Range[2][1]
        self.材料数 = Range[2][5]
        self.要素数 = Range[2][11]

        for i in range(self.節点数):
            self.節点X[i]       = Range[6+i][0]
            self.節点Y[i]       = Range[6+i][1]
            self.節点Z[i]       = Range[6+i][2]

        for i in range(self.材料数):
            self.弾性係数[i]    = Range[6+i][4]
            self.gk[i]          = Range[6+i][5]
            self.断面積[i]      = Range[6+i][6]
            self.yi[i]          = Range[6+i][7]
            self.zi[i]          = Range[6+i][8]

        for i in range(self.要素数):
            self.要素節点[i][0] = Range[6+i][10]
            self.要素節点[i][1] = Range[6+i][11]
            self.要素材料[i]    = Range[6+i][12]
            k1x = Range[6+i][13]
            k1y = Range[6+i][14]
            k1z = Range[6+i][15]
            k2x = Range[6+i][16]
            k2y = Range[6+i][17]
            k2z = Range[6+i][18]
            self.fai[i]         = Range[6+i][19]

            k1 = k1x + k1y + k1z
            k2 = k2x + k2y + k2z

            if k1 == 0:
                self.KTR1[i] = 0
            elif k1 == 1:
                if k1x == 1: self.KTR1[i] = 1 
                if k1y == 1: self.KTR1[i] = 2
                if k1z == 1: self.KTR1[i] = 3
            elif k1 == 2:
                if k1x == 1 and k1y == 1: self.KTR1[i] = 4
                if k1y == 1 and k1z == 1: self.KTR1[i] = 5
                if k1z == 1 and k1x == 1: self.KTR1[i] = 6
            elif k1 == 3:
                self.KTR1[i] = 7

            if k2 == 0:
                self.KTR2[i] = 0
            elif k2 == 1:
                if k2x == 1: self.KTR2[i] = 1
                if k2y == 1: self.KTR2[i] = 2
                if k2z == 1: self.KTR2[i] = 3
            elif k2 == 2:
                if k2x == 1 and k2y == 1: self.KTR2[i] = 4
                if k2y == 1 and k2z == 1: self.KTR2[i] = 5
                if k2z == 1 and k2x == 1: self.KTR2[i] = 6
            elif k2 == 3:
                self.KTR2[i] = 7



        f = open(self.入力シート名2+'.csv', 'rb')
        csv_obj = csv.render(f)
        Range = [ v for v in csv_obj]
    
 
        self.拘束条件数 = Range[2][1]
        self.集中荷重数 = Range[2][9]
        self.分布荷重数 = Range[2][17]

        for i in range(self.拘束条件数):
            self.拘束条件節点[i]    = Range[7+i][1]
            self.nxfx[i]            = Range[7+i][2]
            self.nyfx[i]            = Range[7+i][3]
            self.nzfx[i]            = Range[7+i][4]
            self.mxfx[i]            = Range[7+i][5]
            self.myfx[i]            = Range[7+i][6]
            self.mzfx[i]            = Range[7+i][7]
        

        for i in range(self.集中荷重数):
            self.集中荷重節点[i]    = Range[7+i][9]
            self.fx[i]              = Range[7+i][10]
            self.fy[i]              = Range[7+i][11]
            self.fz[i]              = Range[7+i][12]
            self.fmx[i]             = Range[7+i][13]
            self.fmy[i]             = Range[7+i][14]
            self.fmz[i]             = Range[7+i][15]
        

        for i in range(self.分布荷重数):
            self.分布荷重節点[i][0] = Range[7+i][17]
            self.分布荷重節点[i][1] = Range[7+i][18]
            self.wx[i]              = Range[7+i][19]
            self.wy[i]              = Range[7+i][20]
            self.wz[i]              = Range[7+i][21]
        


    ##################################
    ##     ３次元　外力を加える     ##
    ##       ** ADDFW.for **        ##
    ##################################
    def 外力add(self):

        for i in range(self.集中荷重数):
            if self.fx[i] != 0:
                ii = self.ID[0][self.集中荷重節点[i]]
                self.FORCE[ii] += self.fx[i]

            if self.fy[i] != 0:
                ii = self.ID[1][self.集中荷重節点[i]]
                self.FORCE[ii] += self.fy[i]

            if self.fz[i] != 0:
                ii = self.ID[2][self.集中荷重節点[i]]
                self.FORCE[ii] += self.fz[i]

            if self.fmx[i] != 0:
                ii = self.ID[3][self.集中荷重節点[i]]
                self.FORCE[ii] += self.fmx[i]

            if self.fmy[i] != 0:
                ii = self.ID[4][self.集中荷重節点[i]]
                self.FORCE[ii] += self.fmy[i]

            if self.fmz[i] != 0:
                ii = self.ID[5][self.集中荷重節点[i]]
                self.FORCE[ii] += self.fmz[i]
        



    ####################################################
    ##     トラス（０）　ラーメン（１）の結合状態     ##
    ##                  self.KTR1[i] - ktr2(j)             ##
    ##                    x,y,z - x,y,z               ##
    ##             jj=4  (0,1,1 - 1,1,1)              ##
    ##             jj=5  (1,0,1 - 1,1,1)              ##
    ##     ３次元  jj=6  (1,1,0 - 1,1,1)              ##
    ##             jj=10 (1,1,1 - 0,1,1)              ##
    ##             jj=11 (1,1,1 - 1,0,1)              ##
    ##             jj=12 (1,1,1 - 1,1,0)              ##
    ##                ** ELKA1.for **                 ##
    ####################################################
    def elka1(self, JJ):
        b1  = self.EK[JJ][0]  / self.EK[JJ][JJ]
        b2  = self.EK[JJ][1]  / self.EK[JJ][JJ]
        b3  = self.EK[JJ][2]  / self.EK[JJ][JJ]
        b4  = self.EK[JJ][3]  / self.EK[JJ][JJ]
        b5  = self.EK[JJ][4]  / self.EK[JJ][JJ]
        b6  = self.EK[JJ][5]  / self.EK[JJ][JJ]
        b7  = self.EK[JJ][6]  / self.EK[JJ][JJ]
        b8  = self.EK[JJ][7]  / self.EK[JJ][JJ]
        b9  = self.EK[JJ][8]  / self.EK[JJ][JJ]
        b10 = self.EK[JJ][9]  / self.EK[JJ][JJ]
        b11 = self.EK[JJ][10] / self.EK[JJ][JJ]
        b12 = self.EK[JJ][11] / self.EK[JJ][JJ]

        for i in range(12):
            ekk = self.EK[I][JJ]
            self.EK[I, 1) = self.EK[I, 1) - ekk * b1
            self.EK[I, 2) = self.EK[I, 2) - ekk * b2
            self.EK[I, 3) = self.EK[I, 3) - ekk * b3
            self.EK[I, 4) = self.EK[I, 4) - ekk * b4
            self.EK[I, 5) = self.EK[I, 5) - ekk * b5
            self.EK[I, 6) = self.EK[I, 6) - ekk * b6
            self.EK[I, 7) = self.EK[I, 7) - ekk * b7
            self.EK[I, 8) = self.EK[I, 8) - ekk * b8
            self.EK[I, 9) = self.EK[I, 9) - ekk * b9
            self.EK[I, 10) = self.EK[I, 10) - ekk * b10
            self.EK[I, 11) = self.EK[I, 11) - ekk * b11
            self.EK[I, 12) = self.EK[I, 12) - ekk * b12
        


    ####################################################
    ##     トラス（０）　ラーメン（１）の結合状態     ##
    ##                  self.KTR1[i] - ktr2(j)             ##
    ##                    x,y,z - x,y,z               ##
    ##             j1=4  (0,1,1 - 0,1,1)              ##
    ##     ３次元  j1=5  (1,0,1 - 1,0,1)              ##
    ##             j1=6  (1,1,0 - 1,1,0)              ##
    ##                ** ELKA2.for **                 ##
    ####################################################
    def elka2(j1):
        j2 = j1 + 6
        bunbo1 = EK(j1, j1) * EK(j2, j2) - EK(j2, j1) * EK(j1, j2)
        bunbo2 = -bunbo1
        b11 = (EK(j1, j2) * EK(j2, 1) - EK(j2, j2) * EK(j1, 1)) / bunbo1
        b12 = (EK(j1, j2) * EK(j2, 2) - EK(j2, j2) * EK(j1, 2)) / bunbo1
        b13 = (EK(j1, j2) * EK(j2, 3) - EK(j2, j2) * EK(j1, 3)) / bunbo1
        b14 = (EK(j1, j2) * EK(j2, 4) - EK(j2, j2) * EK(j1, 4)) / bunbo1
        b15 = (EK(j1, j2) * EK(j2, 5) - EK(j2, j2) * EK(j1, 5)) / bunbo1
        b16 = (EK(j1, j2) * EK(j2, 6) - EK(j2, j2) * EK(j1, 6)) / bunbo1
        b17 = (EK(j1, j2) * EK(j2, 7) - EK(j2, j2) * EK(j1, 7)) / bunbo1
        b18 = (EK(j1, j2) * EK(j2, 8) - EK(j2, j2) * EK(j1, 8)) / bunbo1
        b19 = (EK(j1, j2) * EK(j2, 9) - EK(j2, j2) * EK(j1, 9)) / bunbo1
        b110 = (EK(j1, j2) * EK(j2, 10) - EK(j2, j2) * EK(j1, 10)) / bunbo1
        b111 = (EK(j1, j2) * EK(j2, 11) - EK(j2, j2) * EK(j1, 11)) / bunbo1
        b112 = (EK(j1, j2) * EK(j2, 12) - EK(j2, j2) * EK(j1, 12)) / bunbo1

        b21 = (EK(j1, j1) * EK(j2, 1) - EK(j2, j1) * EK(j1, 1)) / bunbo2
        b22 = (EK(j1, j1) * EK(j2, 2) - EK(j2, j1) * EK(j1, 2)) / bunbo2
        b23 = (EK(j1, j1) * EK(j2, 3) - EK(j2, j1) * EK(j1, 3)) / bunbo2
        b24 = (EK(j1, j1) * EK(j2, 4) - EK(j2, j1) * EK(j1, 4)) / bunbo2
        b25 = (EK(j1, j1) * EK(j2, 5) - EK(j2, j1) * EK(j1, 5)) / bunbo2
        b26 = (EK(j1, j1) * EK(j2, 6) - EK(j2, j1) * EK(j1, 6)) / bunbo2
        b27 = (EK(j1, j1) * EK(j2, 7) - EK(j2, j1) * EK(j1, 7)) / bunbo2
        b28 = (EK(j1, j1) * EK(j2, 8) - EK(j2, j1) * EK(j1, 8)) / bunbo2
        b29 = (EK(j1, j1) * EK(j2, 9) - EK(j2, j1) * EK(j1, 9)) / bunbo2
        b210 = (EK(j1, j1) * EK(j2, 10) - EK(j2, j1) * EK(j1, 10)) / bunbo2
        b211 = (EK(j1, j1) * EK(j2, 11) - EK(j2, j1) * EK(j1, 11)) / bunbo2
        b212 = (EK(j1, j1) * EK(j2, 12) - EK(j2, j1) * EK(j1, 12)) / bunbo2

        for i in range(12
            ek1 = EK(I, j1)
            ek2 = EK(I, j2)
            EK(I, 1) = EK(I, 1) + ek1 * b11 + ek2 * b21
            EK(I, 2) = EK(I, 2) + ek1 * b12 + ek2 * b22
            EK(I, 3) = EK(I, 3) + ek1 * b13 + ek2 * b23
            EK(I, 4) = EK(I, 4) + ek1 * b14 + ek2 * b24
            EK(I, 5) = EK(I, 5) + ek1 * b15 + ek2 * b25
            EK(I, 6) = EK(I, 6) + ek1 * b16 + ek2 * b26
            EK(I, 7) = EK(I, 7) + ek1 * b17 + ek2 * b27
            EK(I, 8) = EK(I, 8) + ek1 * b18 + ek2 * b28
            EK(I, 9) = EK(I, 9) + ek1 * b19 + ek2 * b29
            EK(I, 10) = EK(I, 10) + ek1 * b110 + ek2 * b210
            EK(I, 11) = EK(I, 11) + ek1 * b111 + ek2 * b211
            EK(I, 12) = EK(I, 12) + ek1 * b112 + ek2 * b212
        


    ####################################################
    ##     トラス（０）　ラーメン（１）の結合状態     ##
    ##                  self.KTR1[i] - ktr2(j)             ##
    ##                    x,y,z - x,y,z               ##
    ##             jj=6  (0,0,1 - 1,1,1)              ##
    ##             jj=5  (0,1,0 - 1,1,1)              ##
    ##             jj=4  (1,0,0 - 1,1,1)              ##
    ##     ３次元  jj=12 (1,1,1 - 0,0,1)              ##
    ##             jj=11 (1,1,1 - 0,1,0)              ##
    ##             jj=10 (1,1,1 - 1,0,0)              ##
    ##                ** ELKA3.for **                 ##
    ####################################################
    def elka3(JJ):
        if (JJ = 6): j1 = 4
        if (JJ = 6): j2 = 5
        if (JJ = 5): j1 = 4
        if (JJ = 5): j2 = 6
        if (JJ = 4): j1 = 5
        if (JJ = 4): j2 = 6
        if (JJ = 12): j1 = 10
        if (JJ = 12): j2 = 11
        if (JJ = 11): j1 = 10
        if (JJ = 11): j2 = 12
        if (JJ = 10): j1 = 11
        if (JJ = 10): j2 = 12
        bunbo1 = EK(j1, j1) * EK(j2, j2) - EK(j2, j1) * EK(j1, j2)
        bunbo2 = -bunbo1
        b11 = (EK(j1, j2) * EK(j2, 1) - EK(j2, j2) * EK(j1, 1)) / bunbo1
        b12 = (EK(j1, j2) * EK(j2, 2) - EK(j2, j2) * EK(j1, 2)) / bunbo1
        b13 = (EK(j1, j2) * EK(j2, 3) - EK(j2, j2) * EK(j1, 3)) / bunbo1
        b14 = (EK(j1, j2) * EK(j2, 4) - EK(j2, j2) * EK(j1, 4)) / bunbo1
        b15 = (EK(j1, j2) * EK(j2, 5) - EK(j2, j2) * EK(j1, 5)) / bunbo1
        b16 = (EK(j1, j2) * EK(j2, 6) - EK(j2, j2) * EK(j1, 6)) / bunbo1
        b17 = (EK(j1, j2) * EK(j2, 7) - EK(j2, j2) * EK(j1, 7)) / bunbo1
        b18 = (EK(j1, j2) * EK(j2, 8) - EK(j2, j2) * EK(j1, 8)) / bunbo1
        b19 = (EK(j1, j2) * EK(j2, 9) - EK(j2, j2) * EK(j1, 9)) / bunbo1
        b110 = (EK(j1, j2) * EK(j2, 10) - EK(j2, j2) * EK(j1, 10)) / bunbo1
        b111 = (EK(j1, j2) * EK(j2, 11) - EK(j2, j2) * EK(j1, 11)) / bunbo1
        b112 = (EK(j1, j2) * EK(j2, 12) - EK(j2, j2) * EK(j1, 12)) / bunbo1

        b21 = (EK(j1, j1) * EK(j2, 1) - EK(j2, j1) * EK(j1, 1)) / bunbo2
        b22 = (EK(j1, j1) * EK(j2, 2) - EK(j2, j1) * EK(j1, 2)) / bunbo2
        b23 = (EK(j1, j1) * EK(j2, 3) - EK(j2, j1) * EK(j1, 3)) / bunbo2
        b24 = (EK(j1, j1) * EK(j2, 4) - EK(j2, j1) * EK(j1, 4)) / bunbo2
        b25 = (EK(j1, j1) * EK(j2, 5) - EK(j2, j1) * EK(j1, 5)) / bunbo2
        b26 = (EK(j1, j1) * EK(j2, 6) - EK(j2, j1) * EK(j1, 6)) / bunbo2
        b27 = (EK(j1, j1) * EK(j2, 7) - EK(j2, j1) * EK(j1, 7)) / bunbo2
        b28 = (EK(j1, j1) * EK(j2, 8) - EK(j2, j1) * EK(j1, 8)) / bunbo2
        b29 = (EK(j1, j1) * EK(j2, 9) - EK(j2, j1) * EK(j1, 9)) / bunbo2
        b210 = (EK(j1, j1) * EK(j2, 10) - EK(j2, j1) * EK(j1, 10)) / bunbo2
        b211 = (EK(j1, j1) * EK(j2, 11) - EK(j2, j1) * EK(j1, 11)) / bunbo2
        b212 = (EK(j1, j1) * EK(j2, 12) - EK(j2, j1) * EK(j1, 12)) / bunbo2

        for i in range(12
            ek1 = EK(I, j1)
            ek2 = EK(I, j2)
            EK(I, 1) = EK(I, 1) + ek1 * b11 + ek2 * b21
            EK(I, 2) = EK(I, 2) + ek1 * b12 + ek2 * b22
            EK(I, 3) = EK(I, 3) + ek1 * b13 + ek2 * b23
            EK(I, 4) = EK(I, 4) + ek1 * b14 + ek2 * b24
            EK(I, 5) = EK(I, 5) + ek1 * b15 + ek2 * b25
            EK(I, 6) = EK(I, 6) + ek1 * b16 + ek2 * b26
            EK(I, 7) = EK(I, 7) + ek1 * b17 + ek2 * b27
            EK(I, 8) = EK(I, 8) + ek1 * b18 + ek2 * b28
            EK(I, 9) = EK(I, 9) + ek1 * b19 + ek2 * b29
            EK(I, 10) = EK(I, 10) + ek1 * b110 + ek2 * b210
            EK(I, 11) = EK(I, 11) + ek1 * b111 + ek2 * b211
            EK(I, 12) = EK(I, 12) + ek1 * b112 + ek2 * b212
        


    ####################################################
    ##     トラス（０）　ラーメン（１）の結合状態     ##
    ##                  self.KTR1[i] - ktr2(j)             ##
    ##                    x,y,z - x,y,z               ##
    ##     ３次元  j=4   (0,0,0 - 1,1,1)              ##
    ##             j=10  (1,1,1 - 0,0,0)              ##
    ##                ** ELKA4.for **                 ##
    ####################################################
    def elka4(J):
        j1 = J
        j2 = J + 1
        j3 = J + 2
        b1 = EK(j1, j1)
        b2 = EK(j1, j2)
        b3 = EK(j1, j3)
        b4 = EK(j2, j1)
        b5 = EK(j2, j2)
        b6 = EK(j2, j3)
        b7 = EK(j3, j1)
        b8 = EK(j3, j2)
        b9 = EK(j3, j3)

        bb1 = 1# / b9
        am1 = b1 - b3 * b7 * bb1
        am2 = b2 - b3 * b8 * bb1
        am3 = b4 - b6 * b7 * bb1
        am4 = b5 - b6 * b8 * bb1
        am = 1# / (am1 * am4 - am3 * am2)
        s1 = -am4 * am
        s2 = am2 * am
        s3 = b3 * am4 * bb1 * am - b6 * am2 * bb1 * am

        am = 1# / (am2 * am3 - am4 * am1)
        t1 = -am3 * am
        T2 = am1 * am
        t3 = b3 * am3 * bb1 * am - b6 * am1 * bb1 * am

        am = 1# / (am2 * am3 - am4 * am1)
        bm = -am
        r1 = b8 * am3 * bb1 * am + b7 * am4 * bb1 * bm
        r2 = -b7 * am2 * bb1 * bm - b8 * am1 * bb1 * am
        bb2 = bb1 / b9
        rr1 = bb1 + b3 * b7 * bb2 * am4 * bm
        rr2 = b6 * b7 * bb2 * am2 * bm
        rr3 = b3 * b8 * bb2 * am3 * am
        rr4 = b6 * b8 * bb2 * am1 * am
        r3 = -rr1 + rr2 - rr3 + rr4

        bx1 = s1 * EK(j1, 1) + s2 * EK(j2, 1) + s3 * EK(j3, 1)
        bx2 = s1 * EK(j1, 2) + s2 * EK(j2, 2) + s3 * EK(j3, 2)
        bx3 = s1 * EK(j1, 3) + s2 * EK(j2, 3) + s3 * EK(j3, 3)
        bx4 = s1 * EK(j1, 4) + s2 * EK(j2, 4) + s3 * EK(j3, 4)
        bx5 = s1 * EK(j1, 5) + s2 * EK(j2, 5) + s3 * EK(j3, 5)
        bx6 = s1 * EK(j1, 6) + s2 * EK(j2, 6) + s3 * EK(j3, 6)
        bx7 = s1 * EK(j1, 7) + s2 * EK(j2, 7) + s3 * EK(j3, 7)
        bx8 = s1 * EK(j1, 8) + s2 * EK(j2, 8) + s3 * EK(j3, 8)
        bx9 = s1 * EK(j1, 9) + s2 * EK(j2, 9) + s3 * EK(j3, 9)
        bx10 = s1 * EK(j1, 10) + s2 * EK(j2, 10) + s3 * EK(j3, 10)
        bx11 = s1 * EK(j1, 11) + s2 * EK(j2, 11) + s3 * EK(j3, 11)
        bx12 = s1 * EK(j1, 12) + s2 * EK(j2, 12) + s3 * EK(j3, 12)

        by1 = t1 * EK(j1, 1) + T2 * EK(j2, 1) + t3 * EK(j3, 1)
        by2 = t1 * EK(j1, 2) + T2 * EK(j2, 2) + t3 * EK(j3, 2)
        by3 = t1 * EK(j1, 3) + T2 * EK(j2, 3) + t3 * EK(j3, 3)
        by4 = t1 * EK(j1, 4) + T2 * EK(j2, 4) + t3 * EK(j3, 4)
        by5 = t1 * EK(j1, 5) + T2 * EK(j2, 5) + t3 * EK(j3, 5)
        by6 = t1 * EK(j1, 6) + T2 * EK(j2, 6) + t3 * EK(j3, 6)
        by7 = t1 * EK(j1, 7) + T2 * EK(j2, 7) + t3 * EK(j3, 7)
        by8 = t1 * EK(j1, 8) + T2 * EK(j2, 8) + t3 * EK(j3, 8)
        by9 = t1 * EK(j1, 9) + T2 * EK(j2, 9) + t3 * EK(j3, 9)
        by10 = t1 * EK(j1, 10) + T2 * EK(j2, 10) + t3 * EK(j3, 10)
        by11 = t1 * EK(j1, 11) + T2 * EK(j2, 11) + t3 * EK(j3, 11)
        by12 = t1 * EK(j1, 12) + T2 * EK(j2, 12) + t3 * EK(j3, 12)

        bz1 = r1 * EK(j1, 1) + r2 * EK(j2, 1) + r3 * EK(j3, 1)
        bz2 = r1 * EK(j1, 2) + r2 * EK(j2, 2) + r3 * EK(j3, 2)
        bz3 = r1 * EK(j1, 3) + r2 * EK(j2, 3) + r3 * EK(j3, 3)
        bz4 = r1 * EK(j1, 4) + r2 * EK(j2, 4) + r3 * EK(j3, 4)
        bz5 = r1 * EK(j1, 5) + r2 * EK(j2, 5) + r3 * EK(j3, 5)
        bz6 = r1 * EK(j1, 6) + r2 * EK(j2, 6) + r3 * EK(j3, 6)
        bz7 = r1 * EK(j1, 7) + r2 * EK(j2, 7) + r3 * EK(j3, 7)
        bz8 = r1 * EK(j1, 8) + r2 * EK(j2, 8) + r3 * EK(j3, 8)
        bz9 = r1 * EK(j1, 9) + r2 * EK(j2, 9) + r3 * EK(j3, 9)
        bz10 = r1 * EK(j1, 10) + r2 * EK(j2, 10) + r3 * EK(j3, 10)
        bz11 = r1 * EK(j1, 11) + r2 * EK(j2, 11) + r3 * EK(j3, 11)
        bz12 = r1 * EK(j1, 12) + r2 * EK(j2, 12) + r3 * EK(j3, 12)

        for i in range(12
            EK(I, 1) = EK(I, 1) _
                        + EK(I, j1) * bx1 + EK(I, j2) * by1 + EK(I, j3) * bz1
            EK(I, 2) = EK(I, 2) _
                        + EK(I, j1) * bx2 + EK(I, j2) * by2 + EK(I, j3) * bz2
            EK(I, 3) = EK(I, 3) _
                        + EK(I, j1) * bx3 + EK(I, j2) * by3 + EK(I, j3) * bz3
            EK(I, 4) = EK(I, 4) _
                        + EK(I, j1) * bx4 + EK(I, j2) * by4 + EK(I, j3) * bz4
            EK(I, 5) = EK(I, 5) _
                        + EK(I, j1) * bx5 + EK(I, j2) * by5 + EK(I, j3) * bz5
            EK(I, 6) = EK(I, 6) _
                        + EK(I, j1) * bx6 + EK(I, j2) * by6 + EK(I, j3) * bz6
            EK(I, 7) = EK(I, 7) _
                        + EK(I, j1) * bx7 + EK(I, j2) * by7 + EK(I, j3) * bz7
            EK(I, 8) = EK(I, 8) _
                        + EK(I, j1) * bx8 + EK(I, j2) * by8 + EK(I, j3) * bz8
            EK(I, 9) = EK(I, 9) _
                        + EK(I, j1) * bx9 + EK(I, j2) * by9 + EK(I, j3) * bz9
            EK(I, 10) = EK(I, 10) _
                        + EK(I, j1) * bx10 + EK(I, j2) * by10 + EK(I, j3) * bz10
            EK(I, 11) = EK(I, 11) _
                        + EK(I, j1) * bx11 + EK(I, j2) * by11 + EK(I, j3) * bz11
            EK(I, 12) = EK(I, 12) _
                        + EK(I, j1) * bx12 + EK(I, j2) * by12 + EK(I, j3) * bz12
        


    ####################################################
    ##     トラス（０）　ラーメン（１）の結合状態     ##
    ##                  self.KTR1[i] - ktr2(j)             ##
    ##                    x,y,z - x,y,z               ##
    ##     ３次元   j=1  (0,0,1 - 0,0,1)              ##
    ##              j=2  (0,1,0 - 0,1,0)              ##
    ##              j=3  (1,0,0 - 1,0,0)              ##
    ##                ** ELKA5.for **                 ##
    ####################################################
    def elka5(J):
        if J = 1:
            j1 = 4
            j2 = 5
            j3 = 10
            j4 = 11
        End if
        if J = 2:
            j1 = 4
            j2 = 6
            j3 = 10
            j4 = 12
        End if
        if J = 3:
            j1 = 5
            j2 = 6
            j3 = 11
            j4 = 12
        End if

        s1 = 1# / (EK(j1, j1) * EK(j2, j2) - EK(j2, j1) * EK(j1, j2))
        t5 = (EK(j1, j2) * EK(j2, 1) - EK(j2, j2) * EK(j1, 1)) * s1
        t6 = (EK(j1, j2) * EK(j2, 2) - EK(j2, j2) * EK(j1, 2)) * s1
        t7 = (EK(j1, j2) * EK(j2, 3) - EK(j2, j2) * EK(j1, 3)) * s1
        if J = 1: t8 = (EK(j1, j2) * EK(j2, 6) - EK(j2, j2) * EK(j1, 6)) * s1
        if J = 2: t8 = (EK(j1, j2) * EK(j2, 5) - EK(j2, j2) * EK(j1, 5)) * s1
        if J = 3: t8 = (EK(j1, j2) * EK(j2, 4) - EK(j2, j2) * EK(j1, 4)) * s1
        t9 = (EK(j1, j2) * EK(j2, 7) - EK(j2, j2) * EK(j1, 7)) * s1
        t10 = (EK(j1, j2) * EK(j2, 8) - EK(j2, j2) * EK(j1, 8)) * s1
        t11 = (EK(j1, j2) * EK(j2, 9) - EK(j2, j2) * EK(j1, 9)) * s1
        if J = 1: t12 = (EK(j1, j2) * EK(j2, 12) - EK(j2, j2) * EK(j1, 12)) * s1
        if J = 2: t12 = (EK(j1, j2) * EK(j2, 11) - EK(j2, j2) * EK(j1, 11)) * s1
        if J = 3: t12 = (EK(j1, j2) * EK(j2, 10) - EK(j2, j2) * EK(j1, 10)) * s1

        v5 = (EK(j2, j1) * EK(j1, 1) - EK(j1, j1) * EK(j2, 1)) * s1
        v6 = (EK(j2, j1) * EK(j1, 2) - EK(j1, j1) * EK(j2, 2)) * s1
        v7 = (EK(j2, j1) * EK(j1, 3) - EK(j1, j1) * EK(j2, 3)) * s1
        if J = 1: v8 = (EK(j2, j1) * EK(j1, 6) - EK(j1, j1) * EK(j2, 6)) * s1
        if J = 2: v8 = (EK(j2, j1) * EK(j1, 5) - EK(j1, j1) * EK(j2, 5)) * s1
        if J = 3: v8 = (EK(j2, j1) * EK(j1, 4) - EK(j1, j1) * EK(j2, 4)) * s1
        v9 = (EK(j2, j1) * EK(j1, 7) - EK(j1, j1) * EK(j2, 7)) * s1
        v10 = (EK(j2, j1) * EK(j1, 8) - EK(j1, j1) * EK(j2, 8)) * s1
        v11 = (EK(j2, j1) * EK(j1, 9) - EK(j1, j1) * EK(j2, 9)) * s1
        if J = 1: v12 = (EK(j2, j1) * EK(j1, 12) - EK(j1, j1) * EK(j2, 12)) * s1
        if J = 2: v12 = (EK(j2, j1) * EK(j1, 11) - EK(j1, j1) * EK(j2, 11)) * s1
        if J = 3: v12 = (EK(j2, j1) * EK(j1, 10) - EK(j1, j1) * EK(j2, 10)) * s1

        smx5 = EK(j3, 1) + EK(j3, j1) * t5 + EK(j3, j2) * v5
        smx6 = EK(j3, 2) + EK(j3, j1) * t6 + EK(j3, j2) * v6
        smx7 = EK(j3, 3) + EK(j3, j1) * t7 + EK(j3, j2) * v7
        if J = 1: smx8 = EK(j3, 6) + EK(j3, j1) * t8 + EK(j3, j2) * v8
        if J = 2: smx8 = EK(j3, 5) + EK(j3, j1) * t8 + EK(j3, j2) * v8
        if J = 3: smx8 = EK(j3, 4) + EK(j3, j1) * t8 + EK(j3, j2) * v8
        smx9 = EK(j3, 7) + EK(j3, j1) * t9 + EK(j3, j2) * v9
        smx10 = EK(j3, 8) + EK(j3, j1) * t10 + EK(j3, j2) * v10
        smx11 = EK(j3, 9) + EK(j3, j1) * t11 + EK(j3, j2) * v11
        if J = 1: smx12 = EK(j3, 12) + EK(j3, j1) * t12 + EK(j3, j2) * v12
        if J = 2: smx12 = EK(j3, 11) + EK(j3, j1) * t12 + EK(j3, j2) * v12
        if J = 3: smx12 = EK(j3, 10) + EK(j3, j1) * t12 + EK(j3, j2) * v12

        smy5 = EK(j4, 1) + EK(j4, j1) * t5 + EK(j4, j2) * v5
        smy6 = EK(j4, 2) + EK(j4, j1) * t6 + EK(j4, j2) * v6
        smy7 = EK(j4, 3) + EK(j4, j1) * t7 + EK(j4, j2) * v7
        if J = 1: smy8 = EK(j4, 6) + EK(j4, j1) * t8 + EK(j4, j2) * v8
        if J = 2: smy8 = EK(j4, 5) + EK(j4, j1) * t8 + EK(j4, j2) * v8
        if J = 3: smy8 = EK(j4, 4) + EK(j4, j1) * t8 + EK(j4, j2) * v8
        smy9 = EK(j4, 7) + EK(j4, j1) * t9 + EK(j4, j2) * v9
        smy10 = EK(j4, 8) + EK(j4, j1) * t10 + EK(j4, j2) * v10
        smy11 = EK(j4, 9) + EK(j4, j1) * t11 + EK(j4, j2) * v11
        if J = 1: smy12 = EK(j4, 12) + EK(j4, j1) * t12 + EK(j4, j2) * v12
        if J = 2: smy12 = EK(j4, 11) + EK(j4, j1) * t12 + EK(j4, j2) * v12
        if J = 3: smy12 = EK(j4, 10) + EK(j4, j1) * t12 + EK(j4, j2) * v12

        c2 = (-EK(j2, j2) * EK(j1, j3) + EK(j1, j2) * EK(j2, j3)) * s1
        c3 = (-EK(j2, j2) * EK(j1, j4) + EK(j1, j2) * EK(j2, j4)) * s1
        d2 = (EK(j2, j1) * EK(j1, j3) - EK(j1, j1) * EK(j2, j3)) * s1
        d3 = (EK(j2, j1) * EK(j1, j4) - EK(j1, j1) * EK(j2, j4)) * s1
        sk11 = EK(j3, j1) * c2 + EK(j3, j2) * d2 + EK(j3, j3)
        sk12 = EK(j3, j1) * c3 + EK(j3, j2) * d3 + EK(j3, j4)
        sk21 = EK(j4, j1) * c2 + EK(j4, j2) * d2 + EK(j4, j3)
        sk22 = EK(j4, j1) * c3 + EK(j4, j2) * d3 + EK(j4, j4)
        skk = 1# / (sk11 * sk22 - sk21 * sk12)

        x35 = (sk12 * smy5 - sk22 * smx5) * skk
        x36 = (sk12 * smy6 - sk22 * smx6) * skk
        x37 = (sk12 * smy7 - sk22 * smx7) * skk
        x38 = (sk12 * smy8 - sk22 * smx8) * skk
        x39 = (sk12 * smy9 - sk22 * smx9) * skk
        x310 = (sk12 * smy10 - sk22 * smx10) * skk
        x311 = (sk12 * smy11 - sk22 * smx11) * skk
        x312 = (sk12 * smy12 - sk22 * smx12) * skk

        x45 = (sk21 * smx5 - sk11 * smy5) * skk
        x46 = (sk21 * smx6 - sk11 * smy6) * skk
        x47 = (sk21 * smx7 - sk11 * smy7) * skk
        x48 = (sk21 * smx8 - sk11 * smy8) * skk
        x49 = (sk21 * smx9 - sk11 * smy9) * skk
        x410 = (sk21 * smx10 - sk11 * smy10) * skk
        x411 = (sk21 * smx11 - sk11 * smy11) * skk
        x412 = (sk21 * smx12 - sk11 * smy12) * skk

        x15 = t5 + c2 * x35 + c3 * x45
        x16 = t6 + c2 * x36 + c3 * x46
        x17 = t7 + c2 * x37 + c3 * x47
        x18 = t8 + c2 * x38 + c3 * x48
        x19 = t9 + c2 * x39 + c3 * x49
        x110 = t10 + c2 * x310 + c3 * x410
        x111 = t11 + c2 * x311 + c3 * x411
        x112 = t12 + c2 * x312 + c3 * x412

        x25 = v5 + d2 * x35 + d3 * x45
        x26 = v6 + d2 * x36 + d3 * x46
        x27 = v7 + d2 * x37 + d3 * x47
        x28 = v8 + d2 * x38 + d3 * x48
        x29 = v9 + d2 * x39 + d3 * x49
        x210 = v10 + d2 * x310 + d3 * x410
        x211 = v11 + d2 * x311 + d3 * x411
        x212 = v12 + d2 * x312 + d3 * x412

        for i in range(12
            if Not (J = 1 and I = 4) and Not (J = 1 and I = 5) and _
                    Not (J = 2 and I = 4) and Not (J = 2 and I = 6) and _
                    Not (J = 3 and I = 5) and Not (J = 3 and I = 6) and _
                    Not (J = 1 and I = 10) and Not (J = 1 and I = 11) and _
                    Not (J = 2 and I = 10) and Not (J = 2 and I = 12) and _
                    Not (J = 3 and I = 11) and Not (J = 3 and I = 12):
                ek1 = EK(I, 1) + EK(I, j1) * x15 _
                    + EK(I, j2) * x25 + EK(I, j3) * x35 + EK(I, j4) * x45
                ek2 = EK(I, 2) + EK(I, j1) * x16 _
                    + EK(I, j2) * x26 + EK(I, j3) * x36 + EK(I, j4) * x46
                ek3 = EK(I, 3) + EK(I, j1) * x17 _
                    + EK(I, j2) * x27 + EK(I, j3) * x37 + EK(I, j4) * x47
                if (J = 1):
                    ek6 = EK(I, 6) + EK(I, j1) * x18 _
                        + EK(I, j2) * x28 + EK(I, j3) * x38 + EK(I, j4) * x48
                End if
                if (J = 2):
                    ek5 = EK(I, 5) + EK(I, j1) * x18 _
                        + EK(I, j2) * x28 + EK(I, j3) * x38 + EK(I, j4) * x48
                End if
                if (J = 3):
                    ek4 = EK(I, 4) + EK(I, j1) * x18 _
                        + EK(I, j2) * x28 + EK(I, j3) * x38 + EK(I, j4) * x48
                End if
                ek7 = EK(I, 7) + EK(I, j1) * x19 _
                    + EK(I, j2) * x29 + EK(I, j3) * x39 + EK(I, j4) * x49
                ek8 = EK(I, 8) + EK(I, j1) * x110 _
                    + EK(I, j2) * x210 + EK(I, j3) * x310 + EK(I, j4) * x410
                ek9 = EK(I, 9) + EK(I, j1) * x111 _
                    + EK(I, j2) * x211 + EK(I, j3) * x311 + EK(I, j4) * x411
                if (J = 1):
                    ek12 = EK(I, 12) + EK(I, j1) * x112 _
                        + EK(I, j2) * x212 + EK(I, j3) * x312 + EK(I, j4) * x412
                End if
                if (J = 2):
                    ek11 = EK(I, 11) + EK(I, j1) * x112 _
                        + EK(I, j2) * x212 + EK(I, j3) * x312 + EK(I, j4) * x412
                End if
                if (J = 3):
                    ek10 = EK(I, 10) + EK(I, j1) * x112 _
                        + EK(I, j2) * x212 + EK(I, j3) * x312 + EK(I, j4) * x412
                End if
                EK(I, 1) = ek1
                EK(I, 2) = ek2
                EK(I, 3) = ek3
                EK(I, 4) = ek4
                EK(I, 5) = ek5
                EK(I, 6) = ek6
                EK(I, 7) = ek7
                EK(I, 8) = ek8
                EK(I, 9) = ek9
                EK(I, 10) = ek10
                EK(I, 11) = ek11
                EK(I, 12) = ek12
            End if
        
        for i in range(12
            EK(j1, I) = 0#
            EK(j2, I) = 0#
            EK(j3, I) = 0#
            EK(j4, I) = 0#
            EK(I, j1) = 0#
            EK(I, j2) = 0#
            EK(I, j3) = 0#
            EK(I, j4) = 0#
        


    ##############################################################
    ##     ３次元　小軸力｛ｆ’｝＝［Ｋ’］＊［Ｔ］＊｛ｕ｝     ##
    ##                 　 ** FBUZAI.for **                      ##
    ##############################################################
    def fbuzai(JEL):

        Dim ts(3, 3), tf(3, 3), te(3, 3), t(12, 12), ek2(12, 12)
        Dim I As Integer, J As Integer, K As Integer, M As Integer
        Dim FAII As Double, DX As Double, DY As Double, DZ As Double, EL As Double
        Dim xl As Double, XM As Double, XN As Double, xlm As Double, S As Double
        Dim G As Double, YYI As Double, ZZI As Double
        Dim EE As Double, EL2 As Double, EL3 As Double, GKL As Double
        Dim Y2 As Double, Y4 As Double, Y6 As Double, Y12 As Double
        Dim Z2 As Double, Z4 As Double, Z6 As Double, Z12 As Double

        I = 要素節点(JEL, 1)
        J = 要素節点(JEL, 2)
        M = 要素材料(JEL)
        FAII = fai(JEL)
        DX = 節点X(J) - 節点X[i]
        DY = 節点Y(J) - 節点Y[i]
        DZ = 節点Z(J) - 節点Z[i]
        EL = Sqr(DX * DX + DY * DY + DZ * DZ)

        if (DX = 0 and DY = 0):
            te(1, 1) = 0#
            te(1, 2) = 0#
            te(1, 3) = 1#
            te(2, 1) = Cos(FAII)
            te(2, 2) = Sin(FAII)
            te(2, 3) = 0#
            te(3, 1) = -Sin(FAII)
            te(3, 2) = Cos(FAII)
            te(3, 3) = 0#
        Else
            xl = DX / EL
            XM = DY / EL
            XN = DZ / EL
            xlm = Sqr(xl * xl + XM * XM)
            ts(1, 1) = xl
            ts(1, 2) = XM
            ts(1, 3) = XN
            ts(2, 1) = -XM / xlm
            ts(2, 2) = xl / xlm
            ts(2, 3) = 0
            ts(3, 1) = -XN * xl / xlm
            ts(3, 2) = -XM * XN / xlm
            ts(3, 3) = xlm
            tf(1, 1) = 1
            tf(1, 2) = 0
            tf(1, 3) = 0
            tf(2, 1) = 0
            tf(2, 2) = Cos(FAII)
            tf(2, 3) = Sin(FAII)
            tf(3, 1) = 0
            tf(3, 2) = -Sin(FAII)
            tf(3, 3) = Cos(FAII)
            for i in range(3
                for J = 1 To 3
                    S = 0
                    for K = 1 To 3
                        S = S + tf(I, K) * ts(K, J)
                    Next K
                    te(I, J) = S
                Next J
            
        End if

        G = 弾性係数(M) * 断面積(M) / EL
        YYI = yi(M)
        ZZI = zi(M)
        if (KTR1(JEL) = 0 and KTR2(JEL) = 0): YYI = 0#
        if (KTR1(JEL) = 0 and KTR2(JEL) = 0): ZZI = 0#

        EE = 弾性係数(M)
        EL2 = EL * EL
        EL3 = EL * EL2
        Z6 = 6# * EE * ZZI / EL2
        Z12 = 2# * Z6 / EL
        Y6 = 6# * EE * YYI / EL2
        Y12 = 2# * Y6 / EL
        GKL = gk(M) / EL
        Y2 = 2# * EE * YYI / EL
        Y4 = 2# * Y2
        Z2 = 2# * EE * ZZI / EL
        Z4 = 2# * Z2
        for i in range(12
            for J = I To 12
                ek2(I, J) = 0#
            Next J
        
        ek2(1, 1) = G
        ek2(1, 7) = -G
        ek2(2, 2) = Z12
        ek2(2, 6) = Z6
        ek2(2, 8) = -Z12
        ek2(2, 12) = Z6
        ek2(3, 3) = Y12
        ek2(3, 5) = -Y6
        ek2(3, 9) = -Y12
        ek2(3, 11) = -Y6
        ek2(4, 4) = GKL
        ek2(4, 10) = -GKL
        ek2(5, 5) = Y4
        ek2(5, 9) = Y6
        ek2(5, 11) = Y2
        ek2(6, 6) = Z4
        ek2(6, 8) = -Z6
        ek2(6, 12) = Z2
        ek2(7, 7) = G
        ek2(8, 8) = Z12
        ek2(8, 12) = -Z6
        ek2(9, 9) = Y12
        ek2(9, 11) = Y6
        ek2(10, 10) = GKL
        ek2(11, 11) = Y4
        ek2(12, 12) = Z4
        for i in range(11
            for J = I + 1 To 12
                ek2(J, I) = ek2(I, J)
            Next J
        

        for i in range(12
            for J = 1 To 12
                t(I, J) = 0
            Next J
        
        for i in range(3
            for J = 1 To 3
                t(I, J) = te(I, J)
                t(3 + I, 3 + J) = te(I, J)
                t(6 + I, 6 + J) = te(I, J)
                t(9 + I, 9 + J) = te(I, J)
            Next J
        

        for i in range(12
            for J = 1 To 12
                S = 0
                for K = 1 To 12
                    S = ek2(I, K) * t(K, J) + S
                Next K
                EK(I, J) = S
            Next J
        


    ####################################
    ##     ３次元　変 位 の 計 算     ##
    ##        ** HENIKS.for **        ##
    ####################################
    def 変位計算():

        Dim I As Integer, J As Integer, K As Integer
        Dim FLOAD(6) As Double

        for i in range(節点数
            for J = 1 To 6
                K = ID(J, I)
                if (K != 0): FLOAD(J) = FORCE(K)
            Next J
            変位(I, 1) = FLOAD(1)
            変位(I, 2) = FLOAD(2)
            変位(I, 3) = FLOAD(3)
            変位(I, 4) = FLOAD(4)
            変位(I, 5) = FLOAD(5)
            変位(I, 6) = FLOAD(6)
        
        for i in range(拘束条件数
            J = 拘束条件節点[i]
            if (1 = nxfx[i]): 変位(J, 1) = 0#
            if (1 = nyfx[i]): 変位(J, 2) = 0#
            if (1 = nzfx[i]): 変位(J, 3) = 0#
            if (1 = mxfx[i]): 変位(J, 4) = 0#
            if (1 = myfx[i]): 変位(J, 5) = 0#
            if (1 = mzfx[i]): 変位(J, 6) = 0#
        



    ####################################################
    ##     ３次元の全体座標系における節点にかかる     ##
    ##     Ｘ、Ｙ、Ｚ方向の力とモーメントの計算       ##
    ##                 ** POWER1.for **               ##
    ##                (** XYFORC.for **)              ##
    ####################################################
    def 力とモーメントの計算():
    
        Dim gforce(12), gdisp(12)
        Dim I As Integer, J As Integer, M As Integer, N As Integer, JEL As Integer
        Dim S As Double

        for i in range(6 * 節点数
            FORCE[i] = 0#
        
        for JEL = 1 To 要素数
            Call 小剛性マトリックス作成(JEL)
            I = 要素節点(JEL, 1)
            J = 要素節点(JEL, 2)
            gdisp(1) = 変位(I, 1)
            gdisp(2) = 変位(I, 2)
            gdisp(3) = 変位(I, 3)
            gdisp(4) = 変位(I, 4)
            gdisp(5) = 変位(I, 5)
            gdisp(6) = 変位(I, 6)
            gdisp(7) = 変位(J, 1)
            gdisp(8) = 変位(J, 2)
            gdisp(9) = 変位(J, 3)
            gdisp(10) = 変位(J, 4)
            gdisp(11) = 変位(J, 5)
            gdisp(12) = 変位(J, 6)
            for M = 1 To 12
                S = 0
                for N = 1 To 12
                    S = S + EK(M, N) * gdisp(N)
                Next N
                gforce(M) = S
            Next M
            FORCE[i] = FORCE[i] + gforce(1)
            FORCE(節点数 + I) = FORCE(節点数 + I) + gforce(2)
            FORCE(2 * 節点数 + I) = FORCE(2 * 節点数 + I) + gforce(3)
            FORCE(3 * 節点数 + I) = FORCE(3 * 節点数 + I) + gforce(4)
            FORCE(4 * 節点数 + I) = FORCE(4 * 節点数 + I) + gforce(5)
            FORCE(5 * 節点数 + I) = FORCE(5 * 節点数 + I) + gforce(6)
            FORCE(J) = FORCE(J) + gforce(7)
            FORCE(節点数 + J) = FORCE(節点数 + J) + gforce(8)
            FORCE(2 * 節点数 + J) = FORCE(2 * 節点数 + J) + gforce(9)
            FORCE(3 * 節点数 + J) = FORCE(3 * 節点数 + J) + gforce(10)
            FORCE(4 * 節点数 + J) = FORCE(4 * 節点数 + J) + gforce(11)
            FORCE(5 * 節点数 + J) = FORCE(5 * 節点数 + J) + gforce(12)
        Next JEL



    ##########################################################
    ##     ３次元の軸力，せん断力，曲げモーメントの計算     ##
    ##                 ** POWER2.for **                     ##
    ##########################################################
    def 結果出力():
    
        Dim gforce(12), gdisp(12)
        Dim I As Integer, J As Integer, M As Integer, N As Integer, K As Integer
        Dim R As Integer, S As Double

        With Worksheets(出力シート名)
            for i in range(節点数
                Range("_変位番号").Offset(I, 0) = I
                Range("_変位X").Offset(I, 0) = 変位(I, 1)
                Range("_変位Y").Offset(I, 0) = 変位(I, 2)
                Range("_変位Z").Offset(I, 0) = 変位(I, 3)
                Range("F6").Offset(I, 0) = 変位(I, 4)
                Range("G6").Offset(I, 0) = 変位(I, 5)
                Range("H6").Offset(I, 0) = 変位(I, 6)
            

            for i in range(節点数
                Range("J6").Offset(I, 0).Value = I
                Range("K6").Offset(I, 0).Value = FORCE[i]
                Range("L6").Offset(I, 0).Value = FORCE(節点数 + I)
                Range("M6").Offset(I, 0).Value = FORCE(2 * 節点数 + I)
                Range("N6").Offset(I, 0).Value = FORCE(3 * 節点数 + I)
                Range("O6").Offset(I, 0).Value = FORCE(4 * 節点数 + I)
                Range("P6").Offset(I, 0).Value = FORCE(5 * 節点数 + I)
            

            for K = 1 To 要素数
                Range("_要素番号").Offset(K * 2 - 1, 0) = K
                Call fbuzai(K)
                I = 要素節点(K, 1)
                J = 要素節点(K, 2)
                gdisp(1) = 変位(I, 1)
                gdisp(2) = 変位(I, 2)
                gdisp(3) = 変位(I, 3)
                gdisp(4) = 変位(I, 4)
                gdisp(5) = 変位(I, 5)
                gdisp(6) = 変位(I, 6)
                gdisp(7) = 変位(J, 1)
                gdisp(8) = 変位(J, 2)
                gdisp(9) = 変位(J, 3)
                gdisp(10) = 変位(J, 4)
                gdisp(11) = 変位(J, 5)
                gdisp(12) = 変位(J, 6)
                for M = 1 To 12
                    S = 0
                    for N = 1 To 12
                        S = S + EK(M, N) * gdisp(N)
                    Next N
                    gforce(M) = S
                Next M
                Range("S6").Offset(K * 2 - 1, 0).Value = I
                Range("T6").Offset(K * 2 - 1, 0).Value = gforce(1)
                Range("U6").Offset(K * 2 - 1, 0).Value = gforce(2)
                Range("V6").Offset(K * 2 - 1, 0).Value = gforce(3)
                Range("W6").Offset(K * 2 - 1, 0).Value = gforce(4)
                Range("X6").Offset(K * 2 - 1, 0).Value = gforce(5)
                Range("Y6").Offset(K * 2 - 1, 0).Value = gforce(6)
                Range("S6").Offset(K * 2, 0).Value = J
                Range("T6").Offset(K * 2, 0).Value = gforce(7)
                Range("U6").Offset(K * 2, 0).Value = gforce(8)
                Range("V6").Offset(K * 2, 0).Value = gforce(9)
                Range("W6").Offset(K * 2, 0).Value = gforce(10)
                Range("X6").Offset(K * 2, 0).Value = gforce(11)
                Range("Y6").Offset(K * 2, 0).Value = gforce(12)
            Next K
        End With



    #########################################
    ##     ３次元　skyline  of  matrix     ##
    ##          ** SKYMAT.for **           ##
    #########################################
    def SKYマトリックス(NEQ):

        Dim NBC As Integer
        Dim LM(12) As Integer, ND As Integer
        Dim I As Integer, J As Integer, JEL As Integer
        Dim LS As Long, II As Integer, MEE As Integer, NDI As Integer, KS As Integer
        Dim IJ As Integer, JJ As Integer, NEC As Integer, KSS As Integer

        NBC = 0
        for i in range(拘束条件数
            if (1 = nxfx[i]): NBC = NBC + 1
            if (1 = nyfx[i]): NBC = NBC + 1
            if (1 = nzfx[i]): NBC = NBC + 1
            if (1 = mxfx[i]): NBC = NBC + 1
            if (1 = myfx[i]): NBC = NBC + 1
            if (1 = mzfx[i]): NBC = NBC + 1
        
        NEQ = 6 * 節点数 - NBC
        for i in range(節点数
            ID(1, I) = 1
            ID(2, I) = 1
            ID(3, I) = 1
            ID(4, I) = 1
            ID(5, I) = 1
            ID(6, I) = 1
        
        for i in range(拘束条件数
            J = 拘束条件節点[i]
            if (1 = nxfx[i]): ID(1, J) = 0
            if (1 = nyfx[i]): ID(2, J) = 0
            if (1 = nzfx[i]): ID(3, J) = 0
            if (1 = mxfx[i]): ID(4, J) = 0
            if (1 = myfx[i]): ID(5, J) = 0
            if (1 = mzfx[i]): ID(6, J) = 0
        
        J = 0
        for i in range(節点数
            if (ID(1, I) = 1):
                J = J + 1
                ID(1, I) = J
            End if
            if (ID(2, I) = 1):
                J = J + 1
                ID(2, I) = J
            End if
            if (ID(3, I) = 1):
                J = J + 1
                ID(3, I) = J
            End if
            if (ID(4, I) = 1):
                J = J + 1
                ID(4, I) = J
            End if
            if (ID(5, I) = 1):
                J = J + 1
                ID(5, I) = J
            End if
            if (ID(6, I) = 1):
                J = J + 1
                ID(6, I) = J
            End if
        

        ND = 12
        for i in range(NEQ
            MHT[i] = 0
        
        for JEL = 1 To 要素数
            for i in range(ND
                LM[i] = 0
            
            J = 要素節点(JEL, 1)
            LM(1) = ID(1, J)
            LM(2) = ID(2, J)
            LM(3) = ID(3, J)
            LM(4) = ID(4, J)
            LM(5) = ID(5, J)
            LM(6) = ID(6, J)
            J = 要素節点(JEL, 2)
            LM(7) = ID(1, J)
            LM(8) = ID(2, J)
            LM(9) = ID(3, J)
            LM(10) = ID(4, J)
            LM(11) = ID(5, J)
            LM(12) = ID(6, J)
            LS = 10000000
            for i in range(ND
                if (LM[i] != 0 and (LM[i] < LS)):
                    LS = LM[i]
                End if
            
            for i in range(ND
                II = LM[i]
                if (II != 0):
                    MEE = II - LS
                    if (MEE > MHT(II)): MHT(II) = MEE
                End if
            
        Next JEL

        for i in range(NEQ + 1
            MAXA[i] = 0
        
        MAXA(1) = 1
        MAXA(2) = 2
        for I = 2 To NEQ
            MAXA(I + 1) = MAXA[i] + MHT[i] + 1
        
        if (MAXA(NEQ + 1) - MAXA(1) > 配列上限):
            MsgBox "メモリオーバーしました", vbCritical + vbOKOnly
            End
        End if

        for JEL = 1 To 要素数
            Call 小剛性マトリックス作成(JEL)
            for i in range(ND
                LM[i] = 0
            
            J = 要素節点(JEL, 1)
            LM(1) = ID(1, J)
            LM(2) = ID(2, J)
            LM(3) = ID(3, J)
            LM(4) = ID(4, J)
            LM(5) = ID(5, J)
            LM(6) = ID(6, J)
            J = 要素節点(JEL, 2)
            LM(7) = ID(1, J)
            LM(8) = ID(2, J)
            LM(9) = ID(3, J)
            LM(10) = ID(4, J)
            LM(11) = ID(5, J)
            LM(12) = ID(6, J)
            NDI = 0
            for i in range(ND
                II = LM[i]
                if (II > 0):
                    KS = I
                    for J = 1 To ND
                        JJ = LM(J)
                        if (JJ > 0):
                            IJ = II - JJ
                            if (IJ >= 0):
                                NEC = MAXA(II) + IJ
                                KSS = KS
                                if (J >= I): KSS = J + NDI
                                AJCB(NEC) = AJCB(NEC) + SE(KSS)
                            End if
                        End if
                        KS = KS + ND - J
                    Next J
                End if
                NDI = NDI + ND - I
            
        Next JEL



    ############################################
    ##     ３次元　小剛性マトリックス作成     ##
    ##        selm(12,12)---> se(78)          ##
    ##            ** STIMAS.for **            ##
    ############################################
    def 小剛性マトリックス作成(JEL):

        Dim ts(3, 3), tf(3, 3), te(3, 3), t(12, 12), ek2(12, 12)
        Dim I As Integer, J As Integer, K As Integer, M As Integer
        Dim FAII As Double, DX As Double, DY As Double, DZ As Double, EL As Double
        Dim xl As Double, XM As Double, XN As Double, xlm As Double, S As Double
        Dim G As Double, YYI As Double, ZZI As Double
        Dim EE As Double, EL2 As Double, EL3 As Double, GKL As Double
        Dim Y2 As Double, Y4 As Double, Y6 As Double, Y12 As Double
        Dim Z2 As Double, Z4 As Double, Z6 As Double, Z12 As Double

        M = 要素材料(JEL)
        FAII = fai(JEL)
        DX = 節点X(要素節点(JEL, 2)) - 節点X(要素節点(JEL, 1))
        DY = 節点Y(要素節点(JEL, 2)) - 節点Y(要素節点(JEL, 1))
        DZ = 節点Z(要素節点(JEL, 2)) - 節点Z(要素節点(JEL, 1))
        EL = Sqr(DX * DX + DY * DY + DZ * DZ)

        if (DX = 0 and DY = 0):
            te(1, 1) = 0#
            te(1, 2) = 0#
            te(1, 3) = 1#
            te(2, 1) = Cos(FAII)
            te(2, 2) = Sin(FAII)
            te(2, 3) = 0#
            te(3, 1) = -Sin(FAII)
            te(3, 2) = Cos(FAII)
            te(3, 3) = 0#
        Else
            xl = DX / EL
            XM = DY / EL
            XN = DZ / EL
            xlm = Sqr(xl * xl + XM * XM)
            ts(1, 1) = xl
            ts(1, 2) = XM
            ts(1, 3) = XN
            ts(2, 1) = -XM / xlm
            ts(2, 2) = xl / xlm
            ts(2, 3) = 0#
            ts(3, 1) = -XN * xl / xlm
            ts(3, 2) = -XM * XN / xlm
            ts(3, 3) = xlm
            tf(1, 1) = 1#
            tf(1, 2) = 0#
            tf(1, 3) = 0#
            tf(2, 1) = 0#
            tf(2, 2) = Cos(FAII)
            tf(2, 3) = Sin(FAII)
            tf(3, 1) = 0#
            tf(3, 2) = -Sin(FAII)
            tf(3, 3) = Cos(FAII)
            for i in range(3
                for J = 1 To 3
                    S = 0
                    for K = 1 To 3
                        S = S + tf(I, K) * ts(K, J)
                    Next K
                    te(I, J) = S
                Next J
            
        End if

        G = 弾性係数(M) * 断面積(M) / EL
        YYI = yi(M)
        ZZI = zi(M)
        if (KTR1(JEL) = 0 and KTR2(JEL) = 0): YYI = 0#
        if (KTR1(JEL) = 0 and KTR2(JEL) = 0): ZZI = 0#

        EE = 弾性係数(M)
        EL2 = EL * EL
        EL3 = EL * EL2
        Z6 = 6# * EE * ZZI / EL2
        Z12 = 2# * Z6 / EL
        Y6 = 6# * EE * YYI / EL2
        Y12 = 2# * Y6 / EL
        GKL = gk(M) / EL
        Y2 = 2# * EE * YYI / EL
        Y4 = 2# * Y2
        Z2 = 2# * EE * ZZI / EL
        Z4 = 2# * Z2
        for i in range(12
            for J = I To 12
                EK(I, J) = 0#
            Next J
        
        EK(1, 1) = G
        EK(1, 7) = -G
        EK(2, 2) = Z12
        EK(2, 6) = Z6
        EK(2, 8) = -Z12
        EK(2, 12) = Z6
        EK(3, 3) = Y12
        EK(3, 5) = -Y6
        EK(3, 9) = -Y12
        EK(3, 11) = -Y6
        EK(4, 4) = GKL
        EK(4, 10) = -GKL
        EK(5, 5) = Y4
        EK(5, 9) = Y6
        EK(5, 11) = Y2
        EK(6, 6) = Z4
        EK(6, 8) = -Z6
        EK(6, 12) = Z2
        EK(7, 7) = G
        EK(8, 8) = Z12
        EK(8, 12) = -Z6
        EK(9, 9) = Y12
        EK(9, 11) = Y6
        EK(10, 10) = GKL
        EK(11, 11) = Y4
        EK(12, 12) = Z4
        for i in range(11
            for J = I + 1 To 12
                EK(J, I) = EK(I, J)
            Next J
        

        for i in range(12
            for J = 1 To 12
                t(I, J) = 0#
            Next J
        
        for i in range(3
            for J = 1 To 3
                t(I, J) = te(I, J)
                t(3 + I, 3 + J) = te(I, J)
                t(6 + I, 6 + J) = te(I, J)
                t(9 + I, 9 + J) = te(I, J)
            Next J
        

        for i in range(12
            for J = 1 To 12
                S = 0
                for K = 1 To 12
                    S = t(K, I) * EK(K, J) + S
                Next K
                ek2(I, J) = S
            Next J
        
        for i in range(12
            for J = 1 To 12
                S = 0#
                for K = 1 To 12
                    S = ek2(I, K) * t(K, J) + S
                Next K
                EK(I, J) = S
            Next J
        

        if (KTR1(JEL) = 5 and KTR2(JEL) = 7): Call elka1(4)
        if (KTR1(JEL) = 6 and KTR2(JEL) = 7): Call elka1(5)
        if (KTR1(JEL) = 4 and KTR2(JEL) = 7): Call elka1(6)
        if (KTR1(JEL) = 7 and KTR2(JEL) = 5): Call elka1(10)
        if (KTR1(JEL) = 7 and KTR2(JEL) = 6): Call elka1(11)
        if (KTR1(JEL) = 7 and KTR2(JEL) = 4): Call elka1(12)

        if (KTR1(JEL) = 5 and KTR2(JEL) = 5): Call elka2(4)
        if (KTR1(JEL) = 6 and KTR2(JEL) = 6): Call elka2(5)
        if (KTR1(JEL) = 4 and KTR2(JEL) = 4): Call elka2(6)

        if (KTR1(JEL) = 3 and KTR2(JEL) = 7): Call elka3(6)
        if (KTR1(JEL) = 2 and KTR2(JEL) = 7): Call elka3(5)
        if (KTR1(JEL) = 1 and KTR2(JEL) = 7): Call elka3(4)
        if (KTR1(JEL) = 7 and KTR2(JEL) = 3): Call elka3(12)
        if (KTR1(JEL) = 7 and KTR2(JEL) = 2): Call elka3(11)
        if (KTR1(JEL) = 7 and KTR2(JEL) = 1): Call elka3(10)

        if (KTR1(JEL) = 0 and KTR2(JEL) = 7): Call elka4(4)
        if (KTR1(JEL) = 7 and KTR2(JEL) = 0): Call elka4(10)

        if (KTR1(JEL) = 3 and KTR2(JEL) = 3): Call elka5(1)
        if (KTR1(JEL) = 2 and KTR2(JEL) = 2): Call elka5(2)
        if (KTR1(JEL) = 1 and KTR2(JEL) = 1): Call elka5(3)

        K = 0
        for i in range(12
            for J = I To 12
                K = K + 1
                SE(K) = EK(I, J)
            Next J
        



    ###########################################
    ##    ３次元  [A] ----> [L]*[D]*[L]t     ##
    ##           ** SUBDEC.for **            ##
    ###########################################
    def decomp(NN):

        Dim N As Integer, J As Integer, K As Integer, L As Integer
        Dim IC As Integer, KLT As Integer, KI As Integer, KK As Integer
        Dim KN As Integer, KL As Integer, KU As Integer, KH As Integer
        Dim ND As Integer, B As Double, C As Double

        for N = 1 To NN
            KN = MAXA(N)
            KL = KN + 1
            KU = MAXA(N + 1) - 1
            KH = KU - KL
            if (KH > 0):
                K = N - KH
                IC = 0
                KLT = KU
                for J = 1 To KH
                    IC = IC + 1
                    KLT = KLT - 1
                    KI = MAXA(K)
                    ND = MAXA(K + 1) - KI - 1
                    if (ND > 0):
                        if (IC < ND):
                            KK = IC
                        Else
                            KK = ND
                        End if
                        C = 0
                        for L = 1 To KK
                            C = C + AJCB(KI + L) * AJCB(KLT + L)
                        Next L
                        AJCB(KLT) = AJCB(KLT) - C
                    End if
                    K = K + 1
                Next J
            End if
            if (KH >= 0):
                K = N
                B = 0#
                for KK = KL To KU
                    K = K - 1
                    KI = MAXA(K)
                    C = AJCB(KK) / AJCB(KI)
                    if (Abs(C) >= 10000000#):
                        MsgBox "計算エラー", vbCritical + vbOKOnly
                        End
                    End if
                    B = B + C * AJCB(KK)
                    AJCB(KK) = C
                Next KK
                AJCB(KN) = AJCB(KN) - B
            End if
            if (AJCB(KN) = 0): AJCB(KN) = -1E-16
        Next N



    ################################################################
    ##    ３次元　reduce and back-substitute iteration vectors    ##
    ##                    ** SUBRED.for **                        ##
    ################################################################
    def redbak(NN):

        Dim N As Integer, K As Integer, KK As Integer, L As Integer
        Dim KL As Integer, KU As Integer
        Dim C As Double

        for N = 1 To NN
            KL = MAXA(N) + 1
            KU = MAXA(N + 1) - 1
            if (KU - KL >= 0):
                K = N
                C = 0
                for KK = KL To KU
                    K = K - 1
                    C = C + AJCB(KK) * FORCE(K)
                Next KK
                FORCE(N) = FORCE(N) - C
            End if
        Next N
        for N = 1 To NN
            K = MAXA(N)
            FORCE(N) = FORCE(N) / AJCB(K)
        Next N
        N = NN
        for L = 2 To NN
            KL = MAXA(N) + 1
            KU = MAXA(N + 1) - 1
            if (KU - KL >= 0):
                K = N
                for KK = KL To KU
                    K = K - 1
                    FORCE(K) = FORCE(K) - AJCB(KK) * FORCE(N)
                Next KK
            End if
            N = N - 1
        Next L



    ##################################################################
    #      ３次元 節点に分布荷重を集中荷重とモーメントに等価する     #
    #                     ** WBUNPU.for **                           #
    ##################################################################
    def 分布荷重振り分け():

        Dim I As Integer, J As Integer
        Dim N1 As Integer, N2 As Integer, M1 As Integer, M2 As Integer
        Dim X1 As Double, Y1 As Double, Z1 As Double, DL As Double
        Dim X2 As Double, Y2 As Double, Z2 As Double
        Dim XFM1 As Double, YFM1 As Double, YFM2 As Double
        Dim ZFM2 As Double, XFM3 As Double, ZFM3 As Double
        Dim XFM As Double, YFM As Double, ZFM As Double

        for i in range(分布荷重数
            N1 = 分布荷重節点(I, 1)
            N2 = 分布荷重節点(I, 2)
            for J = 1 To 要素数
                M1 = 要素節点(J, 1)
                M2 = 要素節点(J, 2)
                if (N1 = M1 and N2 = M2 Or N1 = M2 and N2 = M1):
                    if (KTR1(J) = 0 and KTR2(J) = 0):
                        X1 = 節点X(N1)
                        Y1 = 節点Y(N1)
                        Z1 = 節点Z(N1)
                        X2 = 節点X(N2)
                        Y2 = 節点Y(N2)
                        Z2 = 節点Z(N2)
                        DL = Sqr((X2 - X1) * (X2 - X1) _
                            + (Y2 - Y1) * (Y2 - Y1) + (Z2 - Z1) * (Z2 - Z1))
                        集中荷重数 = 集中荷重数 + 1
                        集中荷重節点(集中荷重数) = N1
                        fx(集中荷重数) = 0.5 * DL * wx[i]
                        fy(集中荷重数) = 0.5 * DL * wy[i]
                        fz(集中荷重数) = 0.5 * DL * wz[i]
                        fmx(集中荷重数) = 0
                        fmy(集中荷重数) = 0
                        fmz(集中荷重数) = 0
                        集中荷重数 = 集中荷重数 + 1
                        集中荷重節点(集中荷重数) = N2
                        fx(集中荷重数) = 0.5 * DL * wx[i]
                        fy(集中荷重数) = 0.5 * DL * wy[i]
                        fz(集中荷重数) = 0.5 * DL * wz[i]
                        fmx(集中荷重数) = 0
                        fmy(集中荷重数) = 0
                        fmz(集中荷重数) = 0
                    End if
                    if (KTR1(J) = 7 and KTR2(J) = 7):
                        X1 = 節点X(N1)
                        Y1 = 節点Y(N1)
                        Z1 = 節点Z(N1)
                        X2 = 節点X(N2)
                        Y2 = 節点Y(N2)
                        Z2 = 節点Z(N2)
                        DL = Sqr((X2 - X1) * (X2 - X1) _
                            + (Y2 - Y1) * (Y2 - Y1) + (Z2 - Z1) * (Z2 - Z1))

                        YFM1 = Abs(wz[i]) * (X2 - X1) * (X2 - X1) / 12
                        if ((X2 - X1) * wz[i] > 0#):
                            YFM1 = -YFM1
                        Else
                            YFM1 = YFM1
                        End if

                        XFM1 = Abs(wz[i]) * (Y2 - Y1) * (Y2 - Y1) / 12
                        if ((Y2 - Y1) * wz[i] > 0#):
                            XFM1 = XFM1
                        Else
                            XFM1 = -XFM1
                        End if

                        ZFM2 = Abs(wx[i]) * (Y2 - Y1) * (Y2 - Y1) / 12#
                        if ((Y2 - Y1) * wx[i] > 0#):
                            ZFM2 = -ZFM2
                        Else
                            ZFM2 = ZFM2
                        End if

                        YFM2 = Abs(wx[i]) * (Z2 - Z1) * (Z2 - Z1) / 12#
                        if ((Z2 - Z1) * wx[i] > 0#):
                            YFM2 = YFM2
                        Else
                            YFM2 = -YFM2
                        End if

                        ZFM3 = Abs(wy[i]) * (X2 - X1) * (X2 - X1) / 12#
                        if ((X2 - X1) * wy[i] > 0#):
                            ZFM3 = ZFM3
                        Else
                            ZFM3 = -ZFM3
                        End if

                        XFM3 = Abs(wy[i]) * (Z2 - Z1) * (Z2 - Z1) / 12#
                        if ((Z2 - Z1) * wy[i] > 0#):
                            XFM3 = -XFM3
                        Else
                            XFM3 = XFM3
                        End if

                        XFM = XFM1 + XFM3
                        YFM = YFM1 + YFM2
                        ZFM = ZFM2 + ZFM3
                        集中荷重数 = 集中荷重数 + 1
                        集中荷重節点(集中荷重数) = N1
                        fx(集中荷重数) = 0.5 * DL * wx[i]
                        fy(集中荷重数) = 0.5 * DL * wy[i]
                        fz(集中荷重数) = 0.5 * DL * wz[i]
                        fmx(集中荷重数) = XFM
                        fmy(集中荷重数) = YFM
                        fmz(集中荷重数) = ZFM
                        集中荷重数 = 集中荷重数 + 1
                        集中荷重節点(集中荷重数) = N2
                        fx(集中荷重数) = 0.5 * DL * wx[i]
                        fy(集中荷重数) = 0.5 * DL * wy[i]
                        fz(集中荷重数) = 0.5 * DL * wz[i]
                        fmx(集中荷重数) = -XFM
                        fmy(集中荷重数) = -YFM
                        fmz(集中荷重数) = -ZFM
                    End if
                End if
            Next J
        




