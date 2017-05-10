import sys
from Calcrate import Calcrate

if __name__ == "__main__":

    cal = Calcrate()
    NEQ = 0

    err = cal.データ入力()
    if not err is None:
        print(err)
        sys.exit()

    err, NEQ = cal.SkYマトリックス(0)
    if not err is None:
        print(err)
        sys.exit()

    err = cal.分布荷重振り分け()
    if not err is None:
        print(err)
        sys.exit()

    err = cal.外力add()
    if not err is None:
        print(err)
        sys.exit()

    err = cal.decomp(NEQ)
    if not err is None:
        print(err)
        sys.exit()

    err = cal.redbak(NEQ)
    if not err is None:
        print(err)
        sys.exit()

    err = cal.変位計算()
    if not err is None:
        print(err)
        sys.exit()

    err = cal.力とモーメントの計算()
    if not err is None:
        print(err)
        sys.exit()

    err = cal.結果出力()
    if not err is None:
        print(err)
        sys.exit()

    print("解析が終わりました")
