from Calcrate import Calcrate

if __name__ == "__main__":

    cal = Calcrate()
    NEQ = 0

    cal.データ入力()
    cal.SKYマトリックス(NEQ)
    cal.分布荷重振り分け()
    cal.外力add()
    cal.decomp(NEQ)
    cal.redbak(NEQ)
    cal.変位計算()
    cal.力とモーメントの計算()

    cal.結果出力()

    print("解析が終わりました")
