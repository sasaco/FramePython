import sys
import csv
import math

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

        self.iD           = [[0]  * 6] * self.MAX節点
        self.SE           = [0.0] * 78
        self.AjCB         = [0.0] * self.配列上限
        self.変位         = [[0.0]* self.MAX節点] * 6
        self.FORCE        = [0.0] * ( 6 * self.MAX節点 )
        self.MHT          = [0]   * ( 6 * self.MAX節点 )
        self.MAXA         = [0]   * ( 6 * self.MAX節点 + 1 )
        self.Ek           = [[0.0]* 12] * 12
        self.kTR1         = [0]   * self.MAX要素
        self.kTR2         = [0]   * self.MAX要素


    ############################################################
    ##     ３次元　手動入力作成データよりデータを読み込む     ##
    ##          　　　  ** iNPUTX.for **                      ##
    ############################################################
    def データ入力(self):

        f = open(self.入力シート名1+'.csv', 'rb')
        csv_obj = csv.render(f)
        Range = [ v for v in csv_obj]
        f.close()

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

            if   k1 == 0:
                self.kTR1[i] = 0
            elif k1 == 1:
                if k1x == 1: self.kTR1[i] = 1 
                if k1y == 1: self.kTR1[i] = 2
                if k1z == 1: self.kTR1[i] = 3
            elif k1 == 2:
                if k1x == 1 and k1y == 1: self.kTR1[i] = 4
                if k1y == 1 and k1z == 1: self.kTR1[i] = 5
                if k1z == 1 and k1x == 1: self.kTR1[i] = 6
            elif k1 == 3:
                self.kTR1[i] = 7

            if   k2 == 0:
                self.kTR2[i] = 0
            elif k2 == 1:
                if k2x == 1: self.kTR2[i] = 1
                if k2y == 1: self.kTR2[i] = 2
                if k2z == 1: self.kTR2[i] = 3
            elif k2 == 2:
                if k2x == 1 and k2y == 1: self.kTR2[i] = 4
                if k2y == 1 and k2z == 1: self.kTR2[i] = 5
                if k2z == 1 and k2x == 1: self.kTR2[i] = 6
            elif k2 == 3:
                self.kTR2[i] = 7



        f = open(self.入力シート名2+'.csv', 'rb')
        csv_obj = csv.render(f)
        Range = [ v for v in csv_obj]
        f.close()
 
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
                ii = self.iD[0][self.集中荷重節点[i]]
                self.FORCE[ii] += self.fx[i]

            if self.fy[i] != 0:
                ii = self.iD[1][self.集中荷重節点[i]]
                self.FORCE[ii] += self.fy[i]

            if self.fz[i] != 0:
                ii = self.iD[2][self.集中荷重節点[i]]
                self.FORCE[ii] += self.fz[i]

            if self.fmx[i] != 0:
                ii = self.iD[3][self.集中荷重節点[i]]
                self.FORCE[ii] += self.fmx[i]

            if self.fmy[i] != 0:
                ii = self.iD[4][self.集中荷重節点[i]]
                self.FORCE[ii] += self.fmy[i]

            if self.fmz[i] != 0:
                ii = self.iD[5][self.集中荷重節点[i]]
                self.FORCE[ii] += self.fmz[i]
        



    ####################################################
    ##     トラス（０）　ラーメン（１）の結合状態     ##
    ##             self.kTR1[i] - self.kTR2[j)             ##
    ##                    x,y,z - x,y,z               ##
    ##             jj=4  (0,1,1 - 1,1,1)              ##
    ##             jj=5  (1,0,1 - 1,1,1)              ##
    ##     ３次元  jj=6  (1,1,0 - 1,1,1)              ##
    ##             jj=10 (1,1,1 - 0,1,1)              ##
    ##             jj=11 (1,1,1 - 1,0,1)              ##
    ##             jj=12 (1,1,1 - 1,1,0)              ##
    ##                ** ELkA1.for **                 ##
    ####################################################
    def elka1(self, jj):
        b1  = self.Ek[jj][0]  / self.Ek[jj][jj]
        b2  = self.Ek[jj][1]  / self.Ek[jj][jj]
        b3  = self.Ek[jj][2]  / self.Ek[jj][jj]
        b4  = self.Ek[jj][3]  / self.Ek[jj][jj]
        b5  = self.Ek[jj][4]  / self.Ek[jj][jj]
        b6  = self.Ek[jj][5]  / self.Ek[jj][jj]
        b7  = self.Ek[jj][6]  / self.Ek[jj][jj]
        b8  = self.Ek[jj][7]  / self.Ek[jj][jj]
        b9  = self.Ek[jj][8]  / self.Ek[jj][jj]
        b10 = self.Ek[jj][9]  / self.Ek[jj][jj]
        b11 = self.Ek[jj][10] / self.Ek[jj][jj]
        b12 = self.Ek[jj][11] / self.Ek[jj][jj]

        for i in range(12):
            ekk = self.Ek[i][jj]
            self.Ek[i][0]  = self.Ek[i][0]  - ekk * b1
            self.Ek[i][1]  = self.Ek[i][1]  - ekk * b2
            self.Ek[i][2]  = self.Ek[i][2]  - ekk * b3
            self.Ek[i][3]  = self.Ek[i][3]  - ekk * b4
            self.Ek[i][4]  = self.Ek[i][4]  - ekk * b5
            self.Ek[i][5]  = self.Ek[i][5]  - ekk * b6
            self.Ek[i][6]  = self.Ek[i][6]  - ekk * b7
            self.Ek[i][7]  = self.Ek[i][7]  - ekk * b8
            self.Ek[i][8]  = self.Ek[i][8]  - ekk * b9
            self.Ek[i][9]  = self.Ek[i][9]  - ekk * b10
            self.Ek[i][10] = self.Ek[i][10] - ekk * b11
            self.Ek[i][11] = self.Ek[i][11] - ekk * b12
        


    ####################################################
    ##     トラス（０）　ラーメン（１）の結合状態     ##
    ##             self.kTR1[i] - self.kTR2[j)             ##
    ##                    x,y,z - x,y,z               ##
    ##             j1=4  (0,1,1 - 0,1,1)              ##
    ##     ３次元  j1=5  (1,0,1 - 1,0,1)              ##
    ##             j1=6  (1,1,0 - 1,1,0)              ##
    ##                ** ELkA2.for **                 ##
    ####################################################
    def elka2(self, j1):
        j2 = j1 + 6
        bunbo1 = self.Ek[j1][j1] * self.Ek[j2][j2] - self.Ek[j2][j1] * self.Ek[j1][j2]
        bunbo2 = -bunbo1

        b11  = (self.Ek[j1][j2] * self.Ek[j2][0]  - self.Ek[j2][j2] * self.Ek[j1][0])  / bunbo1
        b12  = (self.Ek[j1][j2] * self.Ek[j2][1]  - self.Ek[j2][j2] * self.Ek[j1][1])  / bunbo1
        b13  = (self.Ek[j1][j2] * self.Ek[j2][2]  - self.Ek[j2][j2] * self.Ek[j1][2])  / bunbo1
        b14  = (self.Ek[j1][j2] * self.Ek[j2][3]  - self.Ek[j2][j2] * self.Ek[j1][3])  / bunbo1
        b15  = (self.Ek[j1][j2] * self.Ek[j2][4]  - self.Ek[j2][j2] * self.Ek[j1][4])  / bunbo1
        b16  = (self.Ek[j1][j2] * self.Ek[j2][5]  - self.Ek[j2][j2] * self.Ek[j1][5])  / bunbo1
        b17  = (self.Ek[j1][j2] * self.Ek[j2][6]  - self.Ek[j2][j2] * self.Ek[j1][6])  / bunbo1
        b18  = (self.Ek[j1][j2] * self.Ek[j2][7]  - self.Ek[j2][j2] * self.Ek[j1][7])  / bunbo1
        b19  = (self.Ek[j1][j2] * self.Ek[j2][8]  - self.Ek[j2][j2] * self.Ek[j1][8])  / bunbo1
        b110 = (self.Ek[j1][j2] * self.Ek[j2][9]  - self.Ek[j2][j2] * self.Ek[j1][9])  / bunbo1
        b111 = (self.Ek[j1][j2] * self.Ek[j2][10] - self.Ek[j2][j2] * self.Ek[j1][10]) / bunbo1
        b112 = (self.Ek[j1][j2] * self.Ek[j2][11] - self.Ek[j2][j2] * self.Ek[j1][11]) / bunbo1

        b21  = (self.Ek[j1][j1] * self.Ek[j2][0]  - self.Ek[j2][j1] * self.Ek[j1][0])  / bunbo2
        b22  = (self.Ek[j1][j1] * self.Ek[j2][1]  - self.Ek[j2][j1] * self.Ek[j1][1])  / bunbo2
        b23  = (self.Ek[j1][j1] * self.Ek[j2][2]  - self.Ek[j2][j1] * self.Ek[j1][2])  / bunbo2
        b24  = (self.Ek[j1][j1] * self.Ek[j2][3]  - self.Ek[j2][j1] * self.Ek[j1][3])  / bunbo2
        b25  = (self.Ek[j1][j1] * self.Ek[j2][4]  - self.Ek[j2][j1] * self.Ek[j1][4])  / bunbo2
        b26  = (self.Ek[j1][j1] * self.Ek[j2][5]  - self.Ek[j2][j1] * self.Ek[j1][5])  / bunbo2
        b27  = (self.Ek[j1][j1] * self.Ek[j2][6]  - self.Ek[j2][j1] * self.Ek[j1][6])  / bunbo2
        b28  = (self.Ek[j1][j1] * self.Ek[j2][7]  - self.Ek[j2][j1] * self.Ek[j1][7])  / bunbo2
        b29  = (self.Ek[j1][j1] * self.Ek[j2][8]  - self.Ek[j2][j1] * self.Ek[j1][8])  / bunbo2
        b210 = (self.Ek[j1][j1] * self.Ek[j2][9]  - self.Ek[j2][j1] * self.Ek[j1][9])  / bunbo2
        b211 = (self.Ek[j1][j1] * self.Ek[j2][10] - self.Ek[j2][j1] * self.Ek[j1][10]) / bunbo2
        b212 = (self.Ek[j1][j1] * self.Ek[j2][11] - self.Ek[j2][j1] * self.Ek[j1][11]) / bunbo2

        for i in range(12):
            ek1 = self.Ek[i][j1]
            ek2 = self.Ek[i][j2]
            self.Ek[i][0]  = self.Ek[i][0]  + ek1 * b11  + ek2 * b21
            self.Ek[i][1]  = self.Ek[i][1]  + ek1 * b12  + ek2 * b22
            self.Ek[i][2]  = self.Ek[i][2]  + ek1 * b13  + ek2 * b23
            self.Ek[i][3]  = self.Ek[i][3]  + ek1 * b14  + ek2 * b24
            self.Ek[i][4]  = self.Ek[i][4]  + ek1 * b15  + ek2 * b25
            self.Ek[i][5]  = self.Ek[i][5]  + ek1 * b16  + ek2 * b26
            self.Ek[i][6]  = self.Ek[i][6]  + ek1 * b17  + ek2 * b27
            self.Ek[i][7]  = self.Ek[i][7]  + ek1 * b18  + ek2 * b28
            self.Ek[i][8]  = self.Ek[i][8]  + ek1 * b19  + ek2 * b29
            self.Ek[i][9]  = self.Ek[i][9]  + ek1 * b110 + ek2 * b210
            self.Ek[i][10] = self.Ek[i][10] + ek1 * b111 + ek2 * b211
            self.Ek[i][11] = self.Ek[i][11] + ek1 * b112 + ek2 * b212
        


    ####################################################
    ##     トラス（０）　ラーメン（１）の結合状態     ##
    ##             self.kTR1[i] - self.kTR2[j)             ##
    ##                    x,y,z - x,y,z               ##
    ##             jj=6  (0,0,1 - 1,1,1)              ##
    ##             jj=5  (0,1,0 - 1,1,1)              ##
    ##             jj=4  (1,0,0 - 1,1,1)              ##
    ##     ３次元  jj=12 (1,1,1 - 0,0,1)              ##
    ##             jj=11 (1,1,1 - 0,1,0)              ##
    ##             jj=10 (1,1,1 - 1,0,0)              ##
    ##                ** ELkA3.for **                 ##
    ####################################################
    def elka3(self, jj):

        if jj == 5:  
            j1 = 3
            j2 = 4
        elif jj == 4:
            j1 = 3
            j2 = 5
        elif jj == 3:
            j1 = 4
            j2 = 5
        elif jj == 11:
            j1 = 9
            j2 = 10
        elif jj == 10:
            j1 = 9
            j2 = 11
        elif jj == 9: 
            j1 = 10
            j2 = 11
        else:
            return

        bunbo1 = self.Ek[j1][j1] * self.Ek[j2][j2] - self.Ek[j2][j1] * self.Ek[j1][j2]
        bunbo2 = -bunbo1
        b11  = (self.Ek[j1][j2] * self.Ek[j2][0]  - self.Ek[j2][j2] * self.Ek[j1][0])  / bunbo1
        b12  = (self.Ek[j1][j2] * self.Ek[j2][1]  - self.Ek[j2][j2] * self.Ek[j1][1])  / bunbo1
        b13  = (self.Ek[j1][j2] * self.Ek[j2][2]  - self.Ek[j2][j2] * self.Ek[j1][2])  / bunbo1
        b14  = (self.Ek[j1][j2] * self.Ek[j2][3]  - self.Ek[j2][j2] * self.Ek[j1][3])  / bunbo1
        b15  = (self.Ek[j1][j2] * self.Ek[j2][4]  - self.Ek[j2][j2] * self.Ek[j1][4])  / bunbo1
        b16  = (self.Ek[j1][j2] * self.Ek[j2][5]  - self.Ek[j2][j2] * self.Ek[j1][5])  / bunbo1
        b17  = (self.Ek[j1][j2] * self.Ek[j2][6]  - self.Ek[j2][j2] * self.Ek[j1][6])  / bunbo1
        b18  = (self.Ek[j1][j2] * self.Ek[j2][7]  - self.Ek[j2][j2] * self.Ek[j1][7])  / bunbo1
        b19  = (self.Ek[j1][j2] * self.Ek[j2][8]  - self.Ek[j2][j2] * self.Ek[j1][8])  / bunbo1
        b110 = (self.Ek[j1][j2] * self.Ek[j2][9]  - self.Ek[j2][j2] * self.Ek[j1][9])  / bunbo1
        b111 = (self.Ek[j1][j2] * self.Ek[j2][10] - self.Ek[j2][j2] * self.Ek[j1][10]) / bunbo1
        b112 = (self.Ek[j1][j2] * self.Ek[j2][11] - self.Ek[j2][j2] * self.Ek[j1][11]) / bunbo1

        b21  = (self.Ek[j1][j1] * self.Ek[j2][0]  - self.Ek[j2][j1] * self.Ek[j1][0])  / bunbo2
        b22  = (self.Ek[j1][j1] * self.Ek[j2][1]  - self.Ek[j2][j1] * self.Ek[j1][1])  / bunbo2
        b23  = (self.Ek[j1][j1] * self.Ek[j2][2]  - self.Ek[j2][j1] * self.Ek[j1][2])  / bunbo2
        b24  = (self.Ek[j1][j1] * self.Ek[j2][3]  - self.Ek[j2][j1] * self.Ek[j1][3])  / bunbo2
        b25  = (self.Ek[j1][j1] * self.Ek[j2][4]  - self.Ek[j2][j1] * self.Ek[j1][4])  / bunbo2
        b26  = (self.Ek[j1][j1] * self.Ek[j2][5]  - self.Ek[j2][j1] * self.Ek[j1][5])  / bunbo2
        b27  = (self.Ek[j1][j1] * self.Ek[j2][6]  - self.Ek[j2][j1] * self.Ek[j1][6])  / bunbo2
        b28  = (self.Ek[j1][j1] * self.Ek[j2][7]  - self.Ek[j2][j1] * self.Ek[j1][7])  / bunbo2
        b29  = (self.Ek[j1][j1] * self.Ek[j2][8]  - self.Ek[j2][j1] * self.Ek[j1][8])  / bunbo2
        b210 = (self.Ek[j1][j1] * self.Ek[j2][9]  - self.Ek[j2][j1] * self.Ek[j1][9])  / bunbo2
        b211 = (self.Ek[j1][j1] * self.Ek[j2][10] - self.Ek[j2][j1] * self.Ek[j1][10]) / bunbo2
        b212 = (self.Ek[j1][j1] * self.Ek[j2][11] - self.Ek[j2][j1] * self.Ek[j1][11]) / bunbo2

        for i in range(12):
            ek1 = self.Ek[i][j1]
            ek2 = self.Ek[i][j2]
            self.Ek[i][0]  = self.Ek[i][0]  + ek1 * b11  + ek2 * b21
            self.Ek[i][1]  = self.Ek[i][1]  + ek1 * b12  + ek2 * b22
            self.Ek[i][2]  = self.Ek[i][2]  + ek1 * b13  + ek2 * b23
            self.Ek[i][3]  = self.Ek[i][3]  + ek1 * b14  + ek2 * b24
            self.Ek[i][4]  = self.Ek[i][4]  + ek1 * b15  + ek2 * b25
            self.Ek[i][5]  = self.Ek[i][5]  + ek1 * b16  + ek2 * b26
            self.Ek[i][6]  = self.Ek[i][6]  + ek1 * b17  + ek2 * b27
            self.Ek[i][7]  = self.Ek[i][7]  + ek1 * b18  + ek2 * b28
            self.Ek[i][8]  = self.Ek[i][8]  + ek1 * b19  + ek2 * b29
            self.Ek[i][9]  = self.Ek[i][9]  + ek1 * b110 + ek2 * b210
            self.Ek[i][10] = self.Ek[i][10] + ek1 * b111 + ek2 * b211
            self.Ek[i][11] = self.Ek[i][11] + ek1 * b112 + ek2 * b212
        


    ####################################################
    ##     トラス（０）　ラーメン（１）の結合状態     ##
    ##             self.kTR1[i] - self.kTR2[j)             ##
    ##                    x,y,z - x,y,z               ##
    ##     ３次元  j=4   (0,0,0 - 1,1,1)              ##
    ##             j=10  (1,1,1 - 0,0,0)              ##
    ##                ** ELkA4.for **                 ##
    ####################################################
    def elka4(self, j):
        j1  = j
        j2  = j + 1
        j3  = j + 2
        b1  = self.Ek[j1][j1]
        b2  = self.Ek[j1][j2]
        b3  = self.Ek[j1][j3]
        b4  = self.Ek[j2][j1]
        b5  = self.Ek[j2][j2]
        b6  = self.Ek[j2][j3]
        b7  = self.Ek[j3][j1]
        b8  = self.Ek[j3][j2]
        b9  = self.Ek[j3][j3]

        bb1 = 1 / b9
        am1 = b1 - b3 * b7 * bb1
        am2 = b2 - b3 * b8 * bb1
        am3 = b4 - b6 * b7 * bb1
        am4 = b5 - b6 * b8 * bb1
        am  = 1 / (am1 * am4 - am3 * am2)
        s1  = -am4 * am
        s2  = am2 * am
        s3  = b3 * am4 * bb1 * am - b6 * am2 * bb1 * am

        am  = 1 / (am2 * am3 - am4 * am1)
        t1  = -am3 * am
        T2  = am1 * am
        t3  = b3 * am3 * bb1 * am - b6 * am1 * bb1 * am

        am  = 1 / (am2 * am3 - am4 * am1)
        bm  = -am
        r1  = b8 * am3 * bb1 * am + b7 * am4 * bb1 * bm
        r2  = -b7 * am2 * bb1 * bm - b8 * am1 * bb1 * am
        bb2 = bb1 / b9
        rr1 = bb1 + b3 * b7 * bb2 * am4 * bm
        rr2 = b6 * b7 * bb2 * am2 * bm
        rr3 = b3 * b8 * bb2 * am3 * am
        rr4 = b6 * b8 * bb2 * am1 * am
        r3  = -rr1 + rr2 - rr3 + rr4

        bx1  = s1 * self.Ek[j1][0]  + s2 * self.Ek[j2][0]  + s3 * self.Ek[j3][0]
        bx2  = s1 * self.Ek[j1][1]  + s2 * self.Ek[j2][1]  + s3 * self.Ek[j3][1]
        bx3  = s1 * self.Ek[j1][2]  + s2 * self.Ek[j2][2]  + s3 * self.Ek[j3][2]
        bx4  = s1 * self.Ek[j1][3]  + s2 * self.Ek[j2][3]  + s3 * self.Ek[j3][3]
        bx5  = s1 * self.Ek[j1][4]  + s2 * self.Ek[j2][4]  + s3 * self.Ek[j3][4]
        bx6  = s1 * self.Ek[j1][5]  + s2 * self.Ek[j2][5]  + s3 * self.Ek[j3][5]
        bx7  = s1 * self.Ek[j1][6]  + s2 * self.Ek[j2][6]  + s3 * self.Ek[j3][6]
        bx8  = s1 * self.Ek[j1][7]  + s2 * self.Ek[j2][7]  + s3 * self.Ek[j3][7]
        bx9  = s1 * self.Ek[j1][8]  + s2 * self.Ek[j2][8]  + s3 * self.Ek[j3][8]
        bx10 = s1 * self.Ek[j1][9]  + s2 * self.Ek[j2][9]  + s3 * self.Ek[j3][9]
        bx11 = s1 * self.Ek[j1][10] + s2 * self.Ek[j2][10] + s3 * self.Ek[j3][10]
        bx12 = s1 * self.Ek[j1][11] + s2 * self.Ek[j2][11] + s3 * self.Ek[j3][11]

        by1  = t1 * self.Ek[j1][0]  + T2 * self.Ek[j2][0]  + t3 * self.Ek[j3][0]
        by2  = t1 * self.Ek[j1][1]  + T2 * self.Ek[j2][1]  + t3 * self.Ek[j3][1]
        by3  = t1 * self.Ek[j1][2]  + T2 * self.Ek[j2][2]  + t3 * self.Ek[j3][2]
        by4  = t1 * self.Ek[j1][3]  + T2 * self.Ek[j2][3]  + t3 * self.Ek[j3][3]
        by5  = t1 * self.Ek[j1][4]  + T2 * self.Ek[j2][4]  + t3 * self.Ek[j3][4]
        by6  = t1 * self.Ek[j1][5]  + T2 * self.Ek[j2][5]  + t3 * self.Ek[j3][5]
        by7  = t1 * self.Ek[j1][6]  + T2 * self.Ek[j2][6]  + t3 * self.Ek[j3][6]
        by8  = t1 * self.Ek[j1][7]  + T2 * self.Ek[j2][7]  + t3 * self.Ek[j3][7]
        by9  = t1 * self.Ek[j1][8]  + T2 * self.Ek[j2][8]  + t3 * self.Ek[j3][8]
        by10 = t1 * self.Ek[j1][9]  + T2 * self.Ek[j2][9]  + t3 * self.Ek[j3][9]
        by11 = t1 * self.Ek[j1][10] + T2 * self.Ek[j2][10] + t3 * self.Ek[j3][10]
        by12 = t1 * self.Ek[j1][11] + T2 * self.Ek[j2][11] + t3 * self.Ek[j3][11]

        bz1  = r1 * self.Ek[j1][0]  + r2 * self.Ek[j2][0]  + r3 * self.Ek[j3][0]
        bz2  = r1 * self.Ek[j1][1]  + r2 * self.Ek[j2][1]  + r3 * self.Ek[j3][1]
        bz3  = r1 * self.Ek[j1][2]  + r2 * self.Ek[j2][2]  + r3 * self.Ek[j3][2]
        bz4  = r1 * self.Ek[j1][3]  + r2 * self.Ek[j2][3]  + r3 * self.Ek[j3][3]
        bz5  = r1 * self.Ek[j1][4]  + r2 * self.Ek[j2][4]  + r3 * self.Ek[j3][4]
        bz6  = r1 * self.Ek[j1][5]  + r2 * self.Ek[j2][5]  + r3 * self.Ek[j3][5]
        bz7  = r1 * self.Ek[j1][6]  + r2 * self.Ek[j2][6]  + r3 * self.Ek[j3][6]
        bz8  = r1 * self.Ek[j1][7]  + r2 * self.Ek[j2][7]  + r3 * self.Ek[j3][7]
        bz9  = r1 * self.Ek[j1][8]  + r2 * self.Ek[j2][8]  + r3 * self.Ek[j3][8]
        bz10 = r1 * self.Ek[j1][9]  + r2 * self.Ek[j2][9]  + r3 * self.Ek[j3][9]
        bz11 = r1 * self.Ek[j1][10] + r2 * self.Ek[j2][10] + r3 * self.Ek[j3][10]
        bz12 = r1 * self.Ek[j1][11] + r2 * self.Ek[j2][11] + r3 * self.Ek[j3][11]

        for i in range(12):
            self.Ek[i][0]  = self.Ek[i][0] \
                        + self.Ek[i][j1] * bx1  + self.Ek[i][j2] * by1  + self.Ek[i][j3] * bz1
            self.Ek[i][1]  = self.Ek[i][1] \
                        + self.Ek[i][j1] * bx2  + self.Ek[i][j2] * by2  + self.Ek[i][j3] * bz2
            self.Ek[i][2]  = self.Ek[i][2] \
                        + self.Ek[i][j1] * bx3  + self.Ek[i][j2] * by3  + self.Ek[i][j3] * bz3
            self.Ek[i][3]  = self.Ek[i][3] \
                        + self.Ek[i][j1] * bx4  + self.Ek[i][j2] * by4  + self.Ek[i][j3] * bz4
            self.Ek[i][4]  = self.Ek[i][4] \
                        + self.Ek[i][j1] * bx5  + self.Ek[i][j2] * by5  + self.Ek[i][j3] * bz5
            self.Ek[i][5]  = self.Ek[i][5] \
                        + self.Ek[i][j1] * bx6  + self.Ek[i][j2] * by6  + self.Ek[i][j3] * bz6
            self.Ek[i][6]  = self.Ek[i][6] \
                        + self.Ek[i][j1] * bx7  + self.Ek[i][j2] * by7  + self.Ek[i][j3] * bz7
            self.Ek[i][7]  = self.Ek[i][7] \
                        + self.Ek[i][j1] * bx8  + self.Ek[i][j2] * by8  + self.Ek[i][j3] * bz8
            self.Ek[i][8]  = self.Ek[i][8] \
                        + self.Ek[i][j1] * bx9  + self.Ek[i][j2] * by9  + self.Ek[i][j3] * bz9
            self.Ek[i][9]  = self.Ek[i][9] \
                        + self.Ek[i][j1] * bx10 + self.Ek[i][j2] * by10 + self.Ek[i][j3] * bz10
            self.Ek[i][10] = self.Ek[i][10] \
                        + self.Ek[i][j1] * bx11 + self.Ek[i][j2] * by11 + self.Ek[i][j3] * bz11
            self.Ek[i][11] = self.Ek[i][11] \
                        + self.Ek[i][j1] * bx12 + self.Ek[i][j2] * by12 + self.Ek[i][j3] * bz12
        


    ####################################################
    ##     トラス（０）　ラーメン（１）の結合状態     ##
    ##             self.kTR1[i] - self.kTR2[j)             ##
    ##                    x,y,z - x,y,z               ##
    ##     ３次元   j=1  (0,0,1 - 0,0,1)              ##
    ##              j=2  (0,1,0 - 0,1,0)              ##
    ##              j=3  (1,0,0 - 1,0,0)              ##
    ##                ** ELkA5.for **                 ##
    ####################################################
    def elka5(self, j):
        if j == 0:
            j1 = 3
            j2 = 4
            j3 = 9
            j4 = 10
        elif j == 1:
            j1 = 3
            j2 = 5
            j3 = 9
            j4 = 11
        elif j == 2:
            j1 = 4
            j2 = 5
            j3 = 10
            j4 = 11
        else:
            return
        

        s1 = 1 / (self.Ek[j1][j1] * self.Ek[j2][j2] - self.Ek[j2][j1] * self.Ek[j1][j2])

        t5               = (self.Ek[j1][j2] * self.Ek[j2][0]  - self.Ek[j2][j2] * self.Ek[j1][0])  * s1
        t6               = (self.Ek[j1][j2] * self.Ek[j2][1]  - self.Ek[j2][j2] * self.Ek[j1][1])  * s1
        t7               = (self.Ek[j1][j2] * self.Ek[j2][2]  - self.Ek[j2][j2] * self.Ek[j1][2])  * s1
        if j == 0: t8    = (self.Ek[j1][j2] * self.Ek[j2][5]  - self.Ek[j2][j2] * self.Ek[j1][5])  * s1
        if j == 1: t8    = (self.Ek[j1][j2] * self.Ek[j2][4]  - self.Ek[j2][j2] * self.Ek[j1][4])  * s1
        if j == 2: t8    = (self.Ek[j1][j2] * self.Ek[j2][3]  - self.Ek[j2][j2] * self.Ek[j1][3])  * s1
        t9               = (self.Ek[j1][j2] * self.Ek[j2][6]  - self.Ek[j2][j2] * self.Ek[j1][6])  * s1
        t10              = (self.Ek[j1][j2] * self.Ek[j2][7]  - self.Ek[j2][j2] * self.Ek[j1][7])  * s1
        t11              = (self.Ek[j1][j2] * self.Ek[j2][8]  - self.Ek[j2][j2] * self.Ek[j1][8])  * s1
        if j == 0: t12   = (self.Ek[j1][j2] * self.Ek[j2][11] - self.Ek[j2][j2] * self.Ek[j1][11]) * s1
        if j == 1: t12   = (self.Ek[j1][j2] * self.Ek[j2][10] - self.Ek[j2][j2] * self.Ek[j1][10]) * s1
        if j == 2: t12   = (self.Ek[j1][j2] * self.Ek[j2][9]  - self.Ek[j2][j2] * self.Ek[j1][9])  * s1

        v5               = (self.Ek[j2][j1] * self.Ek[j1][0]  - self.Ek[j1][j1] * self.Ek[j2][0])  * s1
        v6               = (self.Ek[j2][j1] * self.Ek[j1][1]  - self.Ek[j1][j1] * self.Ek[j2][1])  * s1
        v7               = (self.Ek[j2][j1] * self.Ek[j1][2]  - self.Ek[j1][j1] * self.Ek[j2][2])  * s1
        if j == 0: v8    = (self.Ek[j2][j1] * self.Ek[j1][5]  - self.Ek[j1][j1] * self.Ek[j2][5])  * s1
        if j == 1: v8    = (self.Ek[j2][j1] * self.Ek[j1][4]  - self.Ek[j1][j1] * self.Ek[j2][4])  * s1
        if j == 2: v8    = (self.Ek[j2][j1] * self.Ek[j1][3]  - self.Ek[j1][j1] * self.Ek[j2][3])  * s1
        v9               = (self.Ek[j2][j1] * self.Ek[j1][6]  - self.Ek[j1][j1] * self.Ek[j2][6])  * s1
        v10              = (self.Ek[j2][j1] * self.Ek[j1][7]  - self.Ek[j1][j1] * self.Ek[j2][7])  * s1
        v11              = (self.Ek[j2][j1] * self.Ek[j1][8]  - self.Ek[j1][j1] * self.Ek[j2][8])  * s1
        if j == 0: v12   = (self.Ek[j2][j1] * self.Ek[j1][11] - self.Ek[j1][j1] * self.Ek[j2][11]) * s1
        if j == 1: v12   = (self.Ek[j2][j1] * self.Ek[j1][10] - self.Ek[j1][j1] * self.Ek[j2][10]) * s1
        if j == 2: v12   = (self.Ek[j2][j1] * self.Ek[j1][9]  - self.Ek[j1][j1] * self.Ek[j2][9])  * s1


        smx5             = self.Ek[j3][0]  + self.Ek[j3][j1] * t5  + self.Ek[j3][j2] * v5
        smx6             = self.Ek[j3][1]  + self.Ek[j3][j1] * t6  + self.Ek[j3][j2] * v6
        smx7             = self.Ek[j3][2]  + self.Ek[j3][j1] * t7  + self.Ek[j3][j2] * v7
        if j == 0: smx8  = self.Ek[j3][5]  + self.Ek[j3][j1] * t8  + self.Ek[j3][j2] * v8
        if j == 1: smx8  = self.Ek[j3][4]  + self.Ek[j3][j1] * t8  + self.Ek[j3][j2] * v8
        if j == 2: smx8  = self.Ek[j3][3]  + self.Ek[j3][j1] * t8  + self.Ek[j3][j2] * v8
        smx9             = self.Ek[j3][6]  + self.Ek[j3][j1] * t9  + self.Ek[j3][j2] * v9
        smx10            = self.Ek[j3][7]  + self.Ek[j3][j1] * t10 + self.Ek[j3][j2] * v10
        smx11            = self.Ek[j3][8]  + self.Ek[j3][j1] * t11 + self.Ek[j3][j2] * v11
        if j == 0: smx12 = self.Ek[j3][11] + self.Ek[j3][j1] * t12 + self.Ek[j3][j2] * v12
        if j == 1: smx12 = self.Ek[j3][10] + self.Ek[j3][j1] * t12 + self.Ek[j3][j2] * v12
        if j == 2: smx12 = self.Ek[j3][9]  + self.Ek[j3][j1] * t12 + self.Ek[j3][j2] * v12

        smy5             = self.Ek[j4][0]  + self.Ek[j4][j1] * t5  + self.Ek[j4][j2] * v5
        smy6             = self.Ek[j4][1]  + self.Ek[j4][j1] * t6  + self.Ek[j4][j2] * v6
        smy7             = self.Ek[j4][2]  + self.Ek[j4][j1] * t7  + self.Ek[j4][j2] * v7
        if j == 0: smy8  = self.Ek[j4][5]  + self.Ek[j4][j1] * t8  + self.Ek[j4][j2] * v8
        if j == 1: smy8  = self.Ek[j4][4]  + self.Ek[j4][j1] * t8  + self.Ek[j4][j2] * v8
        if j == 2: smy8  = self.Ek[j4][3]  + self.Ek[j4][j1] * t8  + self.Ek[j4][j2] * v8
        smy9             = self.Ek[j4][6]  + self.Ek[j4][j1] * t9  + self.Ek[j4][j2] * v9
        smy10            = self.Ek[j4][7]  + self.Ek[j4][j1] * t10 + self.Ek[j4][j2] * v10
        smy11            = self.Ek[j4][8]  + self.Ek[j4][j1] * t11 + self.Ek[j4][j2] * v11
        if j == 0: smy12 = self.Ek[j4][12] + self.Ek[j4][j1] * t12 + self.Ek[j4][j2] * v12
        if j == 1: smy12 = self.Ek[j4][10] + self.Ek[j4][j1] * t12 + self.Ek[j4][j2] * v12
        if j == 2: smy12 = self.Ek[j4][9]  + self.Ek[j4][j1] * t12 + self.Ek[j4][j2] * v12

        c2   = (-self.Ek[j2][j2] * self.Ek[j1][j3] + self.Ek[j1][j2] * self.Ek[j2][j3]) * s1
        c3   = (-self.Ek[j2][j2] * self.Ek[j1][j4] + self.Ek[j1][j2] * self.Ek[j2][j4]) * s1
        d2   = ( self.Ek[j2][j1] * self.Ek[j1][j3] - self.Ek[j1][j1] * self.Ek[j2][j3]) * s1
        d3   = ( self.Ek[j2][j1] * self.Ek[j1][j4] - self.Ek[j1][j1] * self.Ek[j2][j4]) * s1
        sk11 =   self.Ek[j3][j1] * c2 + self.Ek[j3][j2] * d2 + self.Ek[j3][j3]
        sk12 =   self.Ek[j3][j1] * c3 + self.Ek[j3][j2] * d3 + self.Ek[j3][j4]
        sk21 =   self.Ek[j4][j1] * c2 + self.Ek[j4][j2] * d2 + self.Ek[j4][j3]
        sk22 =   self.Ek[j4][j1] * c3 + self.Ek[j4][j2] * d3 + self.Ek[j4][j4]
        skk  = 1 / (sk11 * sk22 - sk21 * sk12)

        x35  = (sk12 * smy5  - sk22 * smx5)  * skk
        x36  = (sk12 * smy6  - sk22 * smx6)  * skk
        x37  = (sk12 * smy7  - sk22 * smx7)  * skk
        x38  = (sk12 * smy8  - sk22 * smx8)  * skk
        x39  = (sk12 * smy9  - sk22 * smx9)  * skk
        x310 = (sk12 * smy10 - sk22 * smx10) * skk
        x311 = (sk12 * smy11 - sk22 * smx11) * skk
        x312 = (sk12 * smy12 - sk22 * smx12) * skk

        x45  = (sk21 * smx5  - sk11 * smy5)  * skk
        x46  = (sk21 * smx6  - sk11 * smy6)  * skk
        x47  = (sk21 * smx7  - sk11 * smy7)  * skk
        x48  = (sk21 * smx8  - sk11 * smy8)  * skk
        x49  = (sk21 * smx9  - sk11 * smy9)  * skk
        x410 = (sk21 * smx10 - sk11 * smy10) * skk
        x411 = (sk21 * smx11 - sk11 * smy11) * skk
        x412 = (sk21 * smx12 - sk11 * smy12) * skk

        x15  = t5  + c2 * x35  + c3 * x45
        x16  = t6  + c2 * x36  + c3 * x46
        x17  = t7  + c2 * x37  + c3 * x47
        x18  = t8  + c2 * x38  + c3 * x48
        x19  = t9  + c2 * x39  + c3 * x49
        x110 = t10 + c2 * x310 + c3 * x410
        x111 = t11 + c2 * x311 + c3 * x411
        x112 = t12 + c2 * x312 + c3 * x412

        x25  = v5  + d2 * x35  + d3 * x45
        x26  = v6  + d2 * x36  + d3 * x46
        x27  = v7  + d2 * x37  + d3 * x47
        x28  = v8  + d2 * x38  + d3 * x48
        x29  = v9  + d2 * x39  + d3 * x49
        x210 = v10 + d2 * x310 + d3 * x410
        x211 = v11 + d2 * x311 + d3 * x411
        x212 = v12 + d2 * x312 + d3 * x412

        for i in range(12):
            if not (j == 0 and i == 3) and  not (j == 0 and i == 4) and  \
               not (j == 1 and i == 3) and  not (j == 1 and i == 5) and  \
               not (j == 2 and i == 4) and  not (j == 2 and i == 5) and  \
               not (j == 0 and i == 9) and  not (j == 0 and i == 10) and \
               not (j == 1 and i == 9) and  not (j == 1 and i == 11) and \
               not (j == 2 and i == 10) and not (j == 2 and i == 11):

                ek1 = self.Ek[i][0]  + self.Ek[i][j1] * x15 \
                    + self.Ek[i][j2] * x25 + self.Ek[i][j3] * x35 + self.Ek[i][j4] * x45
                ek2 = self.Ek[i][1]  + self.Ek[i][j1] * x16 \
                    + self.Ek[i][j2] * x26 + self.Ek[i][j3] * x36 + self.Ek[i][j4] * x46
                ek3 = self.Ek[i][2]  + self.Ek[i][j1] * x17 \
                    + self.Ek[i][j2] * x27 + self.Ek[i][j3] * x37 + self.Ek[i][j4] * x47

                if j == 0:
                    ek6 = self.Ek[i][5]  + self.Ek[i][j1] * x18 \
                        + self.Ek[i][j2] * x28 + self.Ek[i][j3] * x38 + self.Ek[i][j4] * x48
                
                if j == 1:
                    ek5 = self.Ek[i][4]  + self.Ek[i][j1] * x18 \
                        + self.Ek[i][j2] * x28 + self.Ek[i][j3] * x38 + self.Ek[i][j4] * x48
                
                if j == 2:
                    ek4 = self.Ek[i][3]  + self.Ek[i][j1] * x18 \
                        + self.Ek[i][j2] * x28 + self.Ek[i][j3] * x38 + self.Ek[i][j4] * x48
                
                ek7 = self.Ek[i][6]  + self.Ek[i][j1] * x19 \
                    + self.Ek[i][j2] * x29 + self.Ek[i][j3] * x39 + self.Ek[i][j4] * x49

                ek8 = self.Ek[i][7]  + self.Ek[i][j1] * x110 \
                    + self.Ek[i][j2] * x210 + self.Ek[i][j3] * x310 + self.Ek[i][j4] * x410

                ek9 = self.Ek[i][8]  + self.Ek[i][j1] * x111 \
                    + self.Ek[i][j2] * x211 + self.Ek[i][j3] * x311 + self.Ek[i][j4] * x411

                if j == 0:
                    ek12 = self.Ek[i][11] + self.Ek[i][j1] * x112 \
                         + self.Ek[i][j2] * x212 + self.Ek[i][j3] * x312 + self.Ek[i][j4] * x412
                
                if j == 1:
                    ek11 = self.Ek[i][10] + self.Ek[i][j1] * x112 \
                         + self.Ek[i][j2] * x212 + self.Ek[i][j3] * x312 + self.Ek[i][j4] * x412
                
                if j == 2:
                    ek10 = self.Ek[i][9]  + self.Ek[i][j1] * x112 \
                         + self.Ek[i][j2] * x212 + self.Ek[i][j3] * x312 + self.Ek[i][j4] * x412
                

                self.Ek[i][0]  = ek1
                self.Ek[i][1]  = ek2
                self.Ek[i][2]  = ek3
                self.Ek[i][3]  = ek4
                self.Ek[i][4]  = ek5
                self.Ek[i][5]  = ek6
                self.Ek[i][6]  = ek7
                self.Ek[i][7]  = ek8
                self.Ek[i][8]  = ek9
                self.Ek[i][9]  = ek10
                self.Ek[i][10] = ek11
                self.Ek[i][11] = ek12
            
        
        for i in range(12):
            self.Ek[j1][i] = 0
            self.Ek[j2][i] = 0
            self.Ek[j3][i] = 0
            self.Ek[j4][i] = 0
            self.Ek[i][j1] = 0
            self.Ek[i][j2] = 0
            self.Ek[i][j3] = 0
            self.Ek[i][j4] = 0
        


    ##############################################################
    ##     ３次元　小軸力｛ｆ’｝＝［Ｋ’］＊［Ｔ］＊｛ｕ｝     ##
    ##                 　 ** FBUZAi.for **                      ##
    ##############################################################
    def fbuzai(self, jEL):

        ts  = [[0.0] * 3] * 3
        tf  = [[0.0] * 3] * 3
        te  = [[0.0] * 3] * 3
        t   = [[0.0] * 12] * 12
        ek2 = [[0.0] * 12] * 12


        i    = self.要素節点[jEL][0]
        j    = self.要素節点[jEL][1]
        M    = self.要素材料[jEL]
        FAii = self.fai[jEL]
        DX   = self.節点X[j] - self.節点X[i]
        DY   = self.節点Y[j] - self.節点Y[i]
        DZ   = self.節点Z[j] - self.節点Z[i]
        EL   = math.sqrt(DX * DX + DY * DY + DZ * DZ)

        if DX == 0 and DY == 0:
            te[0][0] = 0
            te[0][1] = 0
            te[0][2] = 1
            te[1][0] = math.cos(FAii)
            te[1][1] = math.sin(FAii)
            te[1][2] = 0
            te[2][0] = -math.sin(FAii)
            te[2][1] = math.cos(FAii)
            te[2][2] = 0
        else:
            xl = DX / EL
            XM = DY / EL
            XN = DZ / EL
            xlm = math.sqrt(xl * xl + XM * XM)
            ts[0][0] = xl
            ts[0][1] = XM
            ts[0][2] = XN
            ts[1][0] = -XM / xlm
            ts[1][1] = xl / xlm
            ts[1][2] = 0
            ts[2][0] = -XN * xl / xlm
            ts[2][1] = -XM * XN / xlm
            ts[2][2] = xlm
            tf[0][0] = 1
            tf[0][1] = 0
            tf[0][2] = 0
            tf[1][0] = 0
            tf[1][1] = math.cos(FAii)
            tf[1][2] = math.sin(FAii)
            tf[2][0] = 0
            tf[2][1] = -math.sin(FAii)
            tf[2][2] = math.cos(FAii)

            for i in range(3):
                for j in range(3):
                    S = 0
                    for k in range(3):
                        S = S + tf[i][k] * ts[k][j]
                    te[i][j] = S
            

        G = self.弾性係数[M] * self.断面積[M] / EL
        YYi = self.yi[M]
        ZZi = self.zi[M]
        if self.kTR1[jEL] == 0 and self.kTR2[jEL] == 0:
            YYi = 0
            ZZi = 0

        EE  = self.弾性係数[M]
        EL2 = EL * EL
        EL3 = EL * EL2
        Z6  = 6 * EE * ZZi / EL2
        Z12 = 2 * Z6 / EL
        Y6  = 6 * EE * YYi / EL2
        Y12 = 2 * Y6 / EL
        GkL = self.gk[M] / EL
        Y2  = 2 * EE * YYi / EL
        Y4  = 2 * Y2
        Z2  = 2 * EE * ZZi / EL
        Z4  = 2 * Z2
        for i in range(12):
            for j in range(i, 12):
                ek2[i][j] = 0
        
        ek2[0][0]   = G
        ek2[0][6]   = -G
        ek2[1][1]   = Z12
        ek2[1][5]   = Z6
        ek2[1][7]   = -Z12
        ek2[1][11]  = Z6
        ek2[2][2]   = Y12
        ek2[2][4]   = -Y6
        ek2[2][8]   = -Y12
        ek2[2][10]  = -Y6
        ek2[3][3]   = GkL
        ek2[3][9]   = -GkL
        ek2[4][4]   = Y4
        ek2[4][8]   = Y6
        ek2[4][10]  = Y2
        ek2[5][5]   = Z4
        ek2[5][7]   = -Z6
        ek2[5][11]  = Z2
        ek2[6][6]   = G
        ek2[7][7]   = Z12
        ek2[7][11]  = -Z6
        ek2[8][8]   = Y12
        ek2[8][10]  = Y6
        ek2[9][9]   = GkL
        ek2[10][10] = Y4
        ek2[11][11] = Z4
        for i in range(11):
            for j in range( i + 1 , 12):
                ek2[j][i] = ek2[i][j]

        for i in range(12):
            for j in range(12):
                t[i][j] = 0
        
        for i in range(3):
            for j in range(3):
                t[i][j] = te[i][j]
                t[3 + i][3 + j] = te[i][j]
                t[6 + i][6 + j] = te[i][j]
                t[9 + i][9 + j] = te[i][j]
        

        for i in range(12):
            for j in range(12):
                S = 0
                for k in range(12):
                    S = ek2[i][k] * t[k][j] + S
                self.Ek[i][j] = S
        


    ####################################
    ##     ３次元　変 位 の 計 算     ##
    ##        ** HENikS.for **        ##
    ####################################
    def 変位計算(self):

        FLOAD = [0.0] * 6

        for i in range(self.節点数):
            for j in range(6):
                k = self.iD[j][i]
                if k != 0:
                    FLOAD[j] = self.FORCE[k]

            self.変位[i][0] = FLOAD[0]
            self.変位[i][1] = FLOAD[1]
            self.変位[i][2] = FLOAD[2]
            self.変位[i][3] = FLOAD[3]
            self.変位[i][4] = FLOAD[4]
            self.変位[i][5] = FLOAD[5]
        
        for i in range(self.拘束条件数):
            j = self.拘束条件節点[i]
            if 1 == self.nxfx[i]: self.変位[j][0] = 0
            if 1 == self.nyfx[i]: self.変位[j][1] = 0
            if 1 == self.nzfx[i]: self.変位[j][2] = 0
            if 1 == self.mxfx[i]: self.変位[j][3] = 0
            if 1 == self.myfx[i]: self.変位[j][4] = 0
            if 1 == self.mzfx[i]: self.変位[j][5] = 0
        



    ####################################################
    ##     ３次元の全体座標系における節点にかかる     ##
    ##     Ｘ、Ｙ、Ｚ方向の力とモーメントの計算       ##
    ##                 ** POWER1.for **               ##
    ##                (** XYFORC.for **)              ##
    ####################################################
    def 力とモーメントの計算(self):
    
        gforce = [0.0] * 12
        gdisp  = [0.0] * 12

        for i in range(6 * self.節点数):
            self.FORCE[i] = 0
        
        for jEL in range(self.要素数):
            self.小剛性マトリックス作成(jEL)
            i = self.要素節点[jEL][0]
            j = self.要素節点[jEL][1]
            gdisp[0]  = self.変位[i][0]
            gdisp[1]  = self.変位[i][1]
            gdisp[2]  = self.変位[i][2]
            gdisp[3]  = self.変位[i][3]
            gdisp[4]  = self.変位[i][4]
            gdisp[5]  = self.変位[i][5]
            gdisp[6]  = self.変位[j][0]
            gdisp[7]  = self.変位[j][1]
            gdisp[8]  = self.変位[j][2]
            gdisp[9]  = self.変位[j][3]
            gdisp[10] = self.変位[j][4]
            gdisp[11] = self.変位[j][5]

            for M in range(12):
                S = 0
                for N in range(12):
                    S = S + self.Ek[M][N] * gdisp[N]
                gforce[M] = S

            self.FORCE[i]                   = self.FORCE[i]                   + gforce[0]
            self.FORCE[self.節点数 + i]     = self.FORCE[self.節点数 + i]     + gforce[1]
            self.FORCE[2 * self.節点数 + i] = self.FORCE[2 * self.節点数 + i] + gforce[2]
            self.FORCE[3 * self.節点数 + i] = self.FORCE[3 * self.節点数 + i] + gforce[3]
            self.FORCE[4 * self.節点数 + i] = self.FORCE[4 * self.節点数 + i] + gforce[4]
            self.FORCE[5 * self.節点数 + i] = self.FORCE[5 * self.節点数 + i] + gforce[5]
            self.FORCE[j]                   = self.FORCE[j]                   + gforce[6]
            self.FORCE[self.節点数 + j]     = self.FORCE[self.節点数 + j]     + gforce[7]
            self.FORCE[2 * self.節点数 + j] = self.FORCE[2 * self.節点数 + j] + gforce[8]
            self.FORCE[3 * self.節点数 + j] = self.FORCE[3 * self.節点数 + j] + gforce[9]
            self.FORCE[4 * self.節点数 + j] = self.FORCE[4 * self.節点数 + j] + gforce[10]
            self.FORCE[5 * self.節点数 + j] = self.FORCE[5 * self.節点数 + j] + gforce[11]



    ##########################################################
    ##     ３次元の軸力，せん断力，曲げモーメントの計算     ##
    ##                 ** POWER2.for **                     ##
    ##########################################################
    def 結果出力(self):
    
        gforce = [0.0] * 12
        gdisp = [0.0] * 12

        f = open(self.出力シート名+'.csv')
        csvlist = f.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
        f.close()

        # データをリストに保持
        csv変位list = {}
        csv反力list = {}
        csv要素list = {}

        for i in range(self.節点数):
            line = "{},{},{},{},{},{},{}".format(
                         i, 
                         self.変位[i][0],
                         self.変位[i][1],
                         self.変位[i][2],
                         self.変位[i][3],
                         self.変位[i][4],
                         self.変位[i][5]
                                          )
            csv変位list.append(line)
            

        for i in range(self.節点数):
            line = "{},{},{},{},{},{},{}".format(
                         i, 
                         self.FORCE[0 * self.節点数 + i],
                         self.FORCE[1 * self.節点数 + i],
                         self.FORCE[2 * self.節点数 + i],
                         self.FORCE[3 * self.節点数 + i],
                         self.FORCE[4 * self.節点数 + i],
                         self.FORCE[5 * self.節点数 + i]
                                          )
            csv反力list.append(line)


            
        for k in range(self.要素数):

            self.fbuzai(k)
            i = self.要素節点[k][0]
            j = self.要素節点[k][1]
            gdisp[0]  = self.変位[i][0]
            gdisp[1]  = self.変位[i][1]
            gdisp[2]  = self.変位[i][2]
            gdisp[3]  = self.変位[i][3]
            gdisp[4]  = self.変位[i][4]
            gdisp[5]  = self.変位[i][5]
            gdisp[6]  = self.変位[j][0]
            gdisp[7]  = self.変位[j][1]
            gdisp[8]  = self.変位[j][2]
            gdisp[9]  = self.変位[j][3]
            gdisp[10] = self.変位[j][4]
            gdisp[11] = self.変位[j][5]

            for M in range(12):
                S = 0
                for N in range(12):
                    S = S + self.Ek[M][N] * gdisp[N]
                gforce[M]= S


            line = "{},{},{},{},{},{},{},{}".format(
                         k, 
                         i, 
                         gforce[0],
                         gforce[1],
                         gforce[2],
                         gforce[3],
                         gforce[4],
                         gforce[5]
                         )
            csv要素list.append(line)

            line = ",{},{},{},{},{},{},{}".format(
                         j, 
                         gforce[6],
                         gforce[7],
                         gforce[8],
                         gforce[9],
                         gforce[10],
                         gforce[11]
                         )
            csv要素list.append(line)

        row = max(len(csv変位list), len(csv反力list), len(csv要素list))
        for r in range(row):
            line = ""

            if row < len(csv変位list):
                line += csv変位list[r] + ","
            else:
                line += ",,,,,,,"

            if row < len(csv反力list):
                line += csv反力list[r] + ","
            else:
                line += ",,,,,,,"

            if row < len(csv要素list):
                line += csv要素list[r] 
            else:
                line += ",,,,,,,"


            csvlist.append(line)


        # ファイルオープン
        f = open(self.出力シート名+'.csv', 'w')
        writer = csv.writer(f, lineterminator='\n')

        # 出力
        writer.writerow(csvlist)

        # ファイルクローズ
        f.close()


    #########################################
    ##     ３次元　skyline  of  matrix     ##
    ##          ** SkYMAT.for **           ##
    #########################################
    def SkYマトリックス(self, NEQ):

        NBC = 0
        for i in range(self.拘束条件数):
            if 1 == self.nxfx[i]: NBC = NBC + 1
            if 1 == self.nyfx[i]: NBC = NBC + 1
            if 1 == self.nzfx[i]: NBC = NBC + 1
            if 1 == self.mxfx[i]: NBC = NBC + 1
            if 1 == self.myfx[i]: NBC = NBC + 1
            if 1 == self.mzfx[i]: NBC = NBC + 1
        
        NEQ = 6 * self.節点数 - NBC

        for i in range(self.節点数):
            self.iD[0][i] = 1
            self.iD[1][i] = 1
            self.iD[2][i] = 1
            self.iD[3][i] = 1
            self.iD[4][i] = 1
            self.iD[5][i] = 1
        
        for i in range(self.拘束条件数):
            j = self.拘束条件節点[i]
            if 1 == self.nxfx[i]: self.iD[0][j] = 0
            if 1 == self.nyfx[i]: self.iD[1][j] = 0
            if 1 == self.nzfx[i]: self.iD[2][j] = 0
            if 1 == self.mxfx[i]: self.iD[3][j] = 0
            if 1 == self.myfx[i]: self.iD[4][j] = 0
            if 1 == self.mzfx[i]: self.iD[5][j] = 0
        
        j = 0
        for i in range(self.節点数):
            if self.iD[0][i] == 1:
                j = j + 1
                self.iD[0][i] = j
            
            if self.iD[1][i] == 1:
                j = j + 1
                self.iD[1][i] = j
            
            if self.iD[2][i] == 1:
                j = j + 1
                self.iD[2][i] = j
            
            if self.iD[3][i] == 1:
                j = j + 1
                self.iD[3][i] = j
            
            if self.iD[4][i] == 1:
                j = j + 1
                self.iD[4][i] = j
            
            if self.iD[5][i] == 1:
                j = j + 1
                self.iD[5][i] = j


        ND = 12
        for i in range(NEQ):
            self.MHT[i] = 0

        LM = [0] * 12
        for jEL in range( self.要素数):
            for i in range(ND):
                LM[i] = 0
            
            j = self.要素節点[jEL][0]
            LM[0]  = self.iD[0][j]
            LM[1]  = self.iD[1][j]
            LM[2]  = self.iD[2][j]
            LM[3]  = self.iD[3][j]
            LM[4]  = self.iD[4][j]
            LM[5]  = self.iD[5][j]
            j = self.要素節点[jEL][1]
            LM[6]  = self.iD[0][j]
            LM[7]  = self.iD[1][j]
            LM[8]  = self.iD[2][j]
            LM[9]  = self.iD[3][j]
            LM[10] = self.iD[4][j]
            LM[11] = self.iD[5][j]

            LS = 10000000
            for i in range(ND):
                if LM[i] != 0 and LM[i] < LS:
                    LS = LM[i]
                          
            for i in range(ND):
                ii = LM[i]
                if ii != 0:
                    MEE = ii - LS
                    if MEE > self.MHT[ii]: self.MHT[ii] = MEE


        for i in range(NEQ + 1):
            self.MAXA[i] = 0
        
        self.MAXA[0] = 1
        self.MAXA[1] = 2

        for i in range(1, NEQ):
            self.MAXA[i + 1] = self.MAXA[i] + self.MHT[i] + 1
        
        if self.MAXA[NEQ + 1] - self.MAXA[0] > self.配列上限:
            print( "メモリオーバーしました")

        for jEL in range(self.要素数):
            self.小剛性マトリックス作成(jEL)
            for i in range(ND):
                LM[i] = 0
            
            j = self.要素節点[jEL][0]
            LM[0]  = self.iD[0][j]
            LM[1]  = self.iD[1][j]
            LM[2]  = self.iD[2][j]
            LM[3]  = self.iD[3][j]
            LM[4]  = self.iD[4][j]
            LM[5]  = self.iD[5][j]
            j = self.要素節点[jEL][1]
            LM[6]  = self.iD[0][j]
            LM[7]  = self.iD[1][j]
            LM[8]  = self.iD[2][j]
            LM[9]  = self.iD[3][j]
            LM[10] = self.iD[4][j]
            LM[11] = self.iD[5][j]

            NDi = 0
            for i in range(ND):
                ii = LM[i]
                if ii > 0:
                    kS = i
                    for j in range(ND):
                        jj = LM[j]
                        if jj > 0:
                            ij = ii - jj
                            if ij >= 0:
                                NEC = self.MAXA[ii] + ij
                                kSS = kS
                                if j >= i: kSS = j + NDi
                                self.AjCB[NEC] = self.AjCB[NEC] + self.SE[kSS]
                        kS = kS + ND - j
                NDi = NDi + ND - i



    ############################################
    ##     ３次元　小剛性マトリックス作成     ##
    ##        selm(12,12)---> se(78)          ##
    ##            ** STiMAS.for **            ##
    ############################################
    def 小剛性マトリックス作成(self, jEL):

        ts  = [ [0.0] * 3 ] * 3
        tf  = [ [0.0] * 3 ] * 3
        te  = [ [0.0] * 3 ] * 3
        t   = [ [0.0] * 3 ] * 3
        ek2 = [ [0.0] * 3 ] * 3

        M    = self.要素材料[jEL]
        FAii = self.fai[jEL]
        DX   = self.節点X[self.要素節点[jEL][1]] - self.節点X[self.要素節点[jEL][0]]
        DY   = self.節点Y[self.要素節点[jEL][1]] - self.節点Y[self.要素節点[jEL][0]]
        DZ   = self.節点Z[self.要素節点[jEL][1]] - self.節点Z[self.要素節点[jEL][0]]
        EL   = math.sqrt(DX * DX + DY * DY + DZ * DZ)

        if DX == 0 and DY == 0:
            te[0][0] = 0
            te[0][1] = 0
            te[0][2] = 1
            te[1][0] = math.cos(FAii)
            te[1][1] = math.sin(FAii)
            te[1][2] = 0
            te[2][0] = -math.sin(FAii)
            te[2][1] = math.cos(FAii)
            te[2][2] = 0
        else:
            xl = DX / EL
            XM = DY / EL
            XN = DZ / EL
            xlm = math.sqrt(xl * xl + XM * XM)
            ts[0][0] = xl
            ts[0][1] = XM
            ts[0][2] = XN
            ts[1][0] = -XM / xlm
            ts[1][1] = xl / xlm
            ts[1][2] = 0
            ts[2][0] = -XN * xl / xlm
            ts[2][1] = -XM * XN / xlm
            ts[2][2] = xlm
            tf[0][0] = 1
            tf[0][1] = 0
            tf[0][2] = 0
            tf[1][0] = 0
            tf[1][1] = math.cos(FAii)
            tf[1][2] = math.sin(FAii)
            tf[2][0] = 0
            tf[2][1] = -math.sin(FAii)
            tf[2][2] = math.cos(FAii)

            for i in range(3):
                for j in range(3):
                    S = 0
                    for k in range(3):
                        S = S + tf[i][k] * ts[k][j]
                    te[i][j] = S

        G = self.弾性係数[M] * self.断面積[M] / EL
        YYi = self.yi[M]
        ZZi = self.zi[M]
        if self.kTR1[jEL] == 0 and self.kTR2[jEL] == 0: YYi = 0
        if self.kTR1[jEL] == 0 and self.kTR2[jEL] == 0: ZZi = 0

        EE  = self.弾性係数[M]
        EL2 = EL * EL
        EL3 = EL * EL2
        Z6  = 6 * EE * ZZi / EL2
        Z12 = 2 * Z6 / EL
        Y6  = 6 * EE * YYi / EL2
        Y12 = 2 * Y6 / EL
        GkL = self.gk[M] / EL
        Y2  = 2 * EE * YYi / EL
        Y4  = 2 * Y2
        Z2  = 2 * EE * ZZi / EL
        Z4  = 2 * Z2

        for i in range(12):
            for j  in range(12):
                self.Ek[i][j] = 0
        
        self.Ek[0] [0]  =  G
        self.Ek[0] [6]  = -G
        self.Ek[1] [1]  =  Z12
        self.Ek[1] [5]  =  Z6
        self.Ek[1] [7]  = -Z12
        self.Ek[1] [11] =  Z6
        self.Ek[2] [2]  =  Y12
        self.Ek[2] [4]  = -Y6
        self.Ek[2] [8]  = -Y12
        self.Ek[2] [10] = -Y6
        self.Ek[3] [3]  =  GkL
        self.Ek[3] [9]  = -GkL
        self.Ek[4] [4]  =  Y4
        self.Ek[4] [8]  =  Y6
        self.Ek[4] [10] =  Y2
        self.Ek[5] [5]  =  Z4
        self.Ek[5] [7]  = -Z6
        self.Ek[5] [11] =  Z2
        self.Ek[6] [6]  =  G
        self.Ek[7] [7]  =  Z12
        self.Ek[7] [11] = -Z6
        self.Ek[8] [8]  =  Y12
        self.Ek[8] [10] =  Y6
        self.Ek[9] [9]  =  GkL
        self.Ek[10][10] =  Y4
        self.Ek[11][11] =  Z4

        for i in range(11):
            for j in range(i + 1, 12):
                self.Ek[j][i] = self.Ek[i][j]
        
        for i in range(12):
            for j in range(12):
                t[i][j] = 0
        
        for i in range(3):
            for j in range(3):
                t[i][j] = te[i][j]
                t[3 + i][3 + j] = te[i][j]
                t[6 + i][6 + j] = te[i][j]
                t[9 + i][9 + j] = te[i][j]
        

        for i in range(12):
            for j in range(12):
                S = 0
                for k in range(12):
                    S = t[k][i] * self.Ek[k][j] + S
                ek2[i][ j] = S
        
        for i in range(12):
            for j in range(12):
                S = 0
                for k in range(12):
                    S = ek2[i][k] * t[k][j] + S
                self.Ek[i][j] = S
        

        if self.kTR1[jEL] == 5 and self.kTR2[jEL] == 7: self.elka1(3)
        if self.kTR1[jEL] == 6 and self.kTR2[jEL] == 7: self.elka1(4)
        if self.kTR1[jEL] == 4 and self.kTR2[jEL] == 7: self.elka1(5)
        if self.kTR1[jEL] == 7 and self.kTR2[jEL] == 5: self.elka1(9)
        if self.kTR1[jEL] == 7 and self.kTR2[jEL] == 6: self.elka1(10)
        if self.kTR1[jEL] == 7 and self.kTR2[jEL] == 4: self.elka1(11)

        if self.kTR1[jEL] == 5 and self.kTR2[jEL] == 5: self.elka2(3)
        if self.kTR1[jEL] == 6 and self.kTR2[jEL] == 6: self.elka2(4)
        if self.kTR1[jEL] == 4 and self.kTR2[jEL] == 4: self.elka2(5)

        if self.kTR1[jEL] == 3 and self.kTR2[jEL] == 7: self.elka3(5)
        if self.kTR1[jEL] == 2 and self.kTR2[jEL] == 7: self.elka3(4)
        if self.kTR1[jEL] == 1 and self.kTR2[jEL] == 7: self.elka3(3)
        if self.kTR1[jEL] == 7 and self.kTR2[jEL] == 3: self.elka3(11)
        if self.kTR1[jEL] == 7 and self.kTR2[jEL] == 2: self.elka3(10)
        if self.kTR1[jEL] == 7 and self.kTR2[jEL] == 1: self.elka3(9)

        if self.kTR1[jEL] == 0 and self.kTR2[jEL] == 7: self.elka4(3)
        if self.kTR1[jEL] == 7 and self.kTR2[jEL] == 0: self.elka4(9)

        if self.kTR1[jEL] == 3 and self.kTR2[jEL] == 3: self.elka5(0)
        if self.kTR1[jEL] == 2 and self.kTR2[jEL] == 2: self.elka5(1)
        if self.kTR1[jEL] == 1 and self.kTR2[jEL] == 1: self.elka5(2)

        k = 0
        for i in range(12):
            for j in range(i, 12):
                k = k + 1
                self.SE[k] = self.Ek[i][j]
        



    ###########################################
    ##    ３次元  [A] ----> [L]*[D]*[L]t     ##
    ##           ** SUBDEC.for **            ##
    ###########################################
    def decomp(self, NN):

        for N in range(NN):
            kN = self.MAXA[N]
            kL = kN + 1
            kU = self.MAXA[N + 1] - 1
            kH = kU - kL
            if kH > 0:
                k = N - kH
                iC = 0
                kLT = kU
                for j in range(kH):
                    iC = iC + 1
                    kLT = kLT - 1
                    ki = self.MAXA[k]
                    ND = self.MAXA[k + 1] - ki - 1
                    if ND > 0:
                        if iC < ND:
                            kk = iC
                        else:
                            kk = ND
                        C = 0
                        for L  in range(kk):
                            C = C + self.AjCB[ki + L] * self.AjCB[kLT + L]

                        self.AjCB[kLT] = self.AjCB[kLT] - C

                    k = k + 1

            if kH >= 0:
                k = N
                B = 0
                for kk in range(kL, kU):
                    k = k - 1
                    ki = self.MAXA[k]
                    C = self.AjCB[kk] / self.AjCB[ki]
                    if abs(C) >= 10000000:
                        print("計算エラー")
                        sys.exit()

                    B = B + C * self.AjCB[kk]
                    self.AjCB[kk] = C

                self.AjCB[kN] = self.AjCB[kN] - B

            if self.AjCB[kN] == 0: self.AjCB[kN] = -1E-16




    ################################################################
    ##    ３次元　reduce and back-substitute iteration vectors    ##
    ##                    ** SUBRED.for **                        ##
    ################################################################
    def redbak(self, NN):

        for N in range(NN):
            kL = self.MAXA[N] + 1
            kU = self.MAXA[N + 1] - 1
            if kU - kL >= 0:
                k = N
                C = 0
                for kk in range(kL, kU):
                    k = k - 1
                    C = C + self.AjCB[kk] * self.FORCE[k]

                self.FORCE[N] = self.FORCE[N] - C


        for N in range(NN):
            k = self.MAXA[N]
            self.FORCE[N] = self.FORCE[N] / self.AjCB[k]


        N = NN
        for L in range(1, NN):
            kL = self.MAXA[N] + 1
            kU = self.MAXA[N + 1] - 1
            if kU - kL >= 0:
                k = N
                for kk in range(kL, kU):
                    k = k - 1
                    self.FORCE[k] = self.FORCE[k] - self.AjCB[kk] * self.FORCE[N]

            N = N - 1





    ##################################################################
    #      ３次元 節点に分布荷重を集中荷重とモーメントに等価する     #
    #                     ** WBUNPU.for **                           #
    ##################################################################
    def 分布荷重振り分け(self):

        for i in range(self.分布荷重数):
            N1 = self.分布荷重節点[i][0]
            N2 = self.分布荷重節点[i][1]
            for j in range(self.要素数):
                M1 = self.要素節点[j][0]
                M2 = self.要素節点[j][1]
                if N1 == M1 and N2 == M2 or N1 == M2 and N2 == M1:
                    if self.kTR1[j] == 0 and self.kTR2[j] == 0:
                        X1 = self.節点X[N1]
                        Y1 = self.節点Y[N1]
                        Z1 = self.節点Z[N1]
                        X2 = self.節点X[N2]
                        Y2 = self.節点Y[N2]
                        Z2 = self.節点Z[N2]
                        DL = math.sqrt((X2 - X1) * (X2 - X1) \
                            + (Y2 - Y1) * (Y2 - Y1) + (Z2 - Z1) * (Z2 - Z1))
                        self.集中荷重数 = self.集中荷重数 + 1
                        self.集中荷重節点[self.集中荷重数] = N1
                        self.fx [self.集中荷重数] = 0.5 * DL * self.wx[i]
                        self.fy [self.集中荷重数] = 0.5 * DL * self.wy[i]
                        self.fz [self.集中荷重数] = 0.5 * DL * self.wz[i]
                        self.fmx[self.集中荷重数] = 0
                        self.fmy[self.集中荷重数] = 0
                        self.fmz[self.集中荷重数] = 0
                        self.集中荷重数 = self.集中荷重数 + 1
                        self.集中荷重節点[self.集中荷重数] = N2
                        self.fx [self.集中荷重数] = 0.5 * DL * self.wx[i]
                        self.fy [self.集中荷重数] = 0.5 * DL * self.wy[i]
                        self.fz [self.集中荷重数] = 0.5 * DL * self.wz[i]
                        self.fmx[self.集中荷重数] = 0
                        self.fmy[self.集中荷重数] = 0
                        self.fmz[self.集中荷重数] = 0


                    if self.kTR1[j] == 7 and self.kTR2[j] == 7:
                        X1 = self.節点X[N1]
                        Y1 = self.節点Y[N1]
                        Z1 = self.節点Z[N1]
                        X2 = self.節点X[N2]
                        Y2 = self.節点Y[N2]
                        Z2 = self.節点Z[N2]
                        DL = math.sqrt((X2 - X1) * (X2 - X1) \
                            + (Y2 - Y1) * (Y2 - Y1) + (Z2 - Z1) * (Z2 - Z1))

                        YFM1 = abs(self.wz[i]) * (X2 - X1) * (X2 - X1) / 12
                        if (X2 - X1) * self.wz[i] > 0:
                            YFM1 = -YFM1
                        else:
                            YFM1 = YFM1

                        XFM1 = abs(self.wz[i]) * (Y2 - Y1) * (Y2 - Y1) / 12
                        if (Y2 - Y1) * self.wz[i] > 0:
                            XFM1 = XFM1
                        else:
                            XFM1 = -XFM1

                        ZFM2 = abs(self.wx[i]) * (Y2 - Y1) * (Y2 - Y1) / 12
                        if (Y2 - Y1) * self.wx[i] > 0:
                            ZFM2 = -ZFM2
                        else:
                            ZFM2 = ZFM2

                        YFM2 = abs(self.wx[i]) * (Z2 - Z1) * (Z2 - Z1) / 12
                        if (Z2 - Z1) * self.wx[i] > 0:
                            YFM2 = YFM2
                        else:
                            YFM2 = -YFM2

                        ZFM3 = abs(self.wy[i]) * (X2 - X1) * (X2 - X1) / 12
                        if (X2 - X1) * self.wy[i] > 0:
                            ZFM3 = ZFM3
                        else:
                            ZFM3 = -ZFM3

                        XFM3 = abs(self.wy[i]) * (Z2 - Z1) * (Z2 - Z1) / 12
                        if (Z2 - Z1) * self.wy[i] > 0:
                            XFM3 = -XFM3
                        else:
                            XFM3 = XFM3

                        XFM = XFM1 + XFM3
                        YFM = YFM1 + YFM2
                        ZFM = ZFM2 + ZFM3
                        self.集中荷重数 = self.集中荷重数 + 1
                        self.集中荷重節点[self.集中荷重数] = N1
                        self.fx [self.集中荷重数] = 0.5 * DL * self.wx[i]
                        self.fy [self.集中荷重数] = 0.5 * DL * self.wy[i]
                        self.fz [self.集中荷重数] = 0.5 * DL * self.wz[i]
                        self.fmx[self.集中荷重数] = XFM
                        self.fmy[self.集中荷重数] = YFM
                        self.fmz[self.集中荷重数] = ZFM
                        self.集中荷重数 = self.集中荷重数 + 1
                        self.集中荷重節点[self.集中荷重数] = N2
                        self.fx [self.集中荷重数] = 0.5 * DL * self.wx[i]
                        self.fy [self.集中荷重数] = 0.5 * DL * self.wy[i]
                        self.fz [self.集中荷重数] = 0.5 * DL * self.wz[i]
                        self.fmx[self.集中荷重数] = -XFM
                        self.fmy[self.集中荷重数] = -YFM
                        self.fmz[self.集中荷重数] = -ZFM
        




