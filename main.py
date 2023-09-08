from math import radians as rad, degrees as deg, sin, cos, tan, asin, acos, atan

from util import get_poi_of_circle_with_line, get_theta2

"""
パラメータを設定し光軸4の傾斜角γ4を計算する。
この傾斜角γ4が0°となるのが正常な光経路となる。

①全ての設定パラメータを定める。
②B点の位置（X,Y）、光軸1の傾斜角γ1を計算する。
③C1点の位置(X2、Y2)を計算する。
④C1点の入射角θ1、屈折角θ2、光軸2の傾斜角γ2を計算す
る。
⑤同様にC2点、A点について、位置、入射角、屈折角、光軸の傾
斜角を計算する。
⑥光軸4の傾斜角γ4を吟味する。
"""

def calc(beta1, phy1, b_pos_x, b_pos_y, debug=True):
    # 1, 2
    BETA_1  = beta1            # 入射面交差角
    PHI_1   = phy1            # [mm] 液菅径
    T_1     = 1               # [mm] 液菅厚み
    N_1     = 1.49            # アクリル屈折率
    N_2     = 1.00            # 空気屈折率
    N_3     = 1.459           # 液管屈折率
    L_1     = 0               # [mm] B点の位置誤差

    B_POS   = (b_pos_x, b_pos_y)
    X1, _ = B_POS
    Y1 = X1 / tan( rad(BETA_1) ) # 13.1
    R  = 12.7
    GAMMA_1 = BETA_1
    if debug: print(f"#1\nX1 = {abs(X1)} mm\nY1 = {abs(Y1)} mm\nR  = {R} mm\nγ1 = {GAMMA_1} deg\n")

    # 2        # 光軸1の傾斜角
    if debug: print(f"#2\nB: {B_POS}\n")

    # 3
    _, C1_POS  = get_poi_of_circle_with_line(
        *(0, 0), R - 1,
        *B_POS, *(0, -(X1 * tan(rad(GAMMA_1))))
    )
    C1_X, C1_Y = C1_POS
    ALPHA_1 = deg(asin(-C1_X / R))
    if debug: print(f"#3\nC1: {C1_POS}\nα1 = {ALPHA_1} deg\n")



    # 4 アクリル製プリズム (+ガラス) から空気へ
    N_1_2   = N_2 / N_1
    THETA_1 = 90 - BETA_1 - ALPHA_1
    THETA_2 = get_theta2(N_1_2, THETA_1)
    GAMMA_2         = 90 - ALPHA_1 - THETA_2

    THETA_1_CRIT  = deg(asin(N_1_2))
    THETA_2_IDEAL = 90 - ALPHA_1
    if debug: print(f"#4\n入射角 = {THETA_1} deg (臨界: {THETA_1_CRIT} deg)\n屈折角 = {THETA_2} deg (理想: {THETA_2_IDEAL} deg)\n傾斜角 = {GAMMA_2}\n")

    return (BETA_1, THETA_1, THETA_2, GAMMA_2, THETA_1_CRIT, THETA_2_IDEAL)




if __name__ == '__main__':
    import os
    os.system('cls')
    
    plus_minus = 1
    POS_CENTER = lambda _: (-7.72, -13.29)
    def POS_UPPER(b):
        x, y = POS_CENTER(b)
        return (x - sin(b) * plus_minus, y + cos(b) * plus_minus)
    def POS_LOWER(b):
        x, y = POS_CENTER(b)
        return (x + sin(b) * plus_minus, y - cos(b) * plus_minus)
        
    # 変数ここから
    base = 30.5             # β1の初期値
    step = 0.01             # 刻み
    repeat = 1000           # 繰り返し
    
    tolerance = 0.3         # 屈折角の理想値と算出値の許容差
    
    pos_target = POS_CENTER # 入射点
    # ここまで
    
    RES = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    print(f"探索中 (β1: {base} deg -> {base - repeat * step} deg [{step}刻み])")
    for n in range(repeat):
        v = base - n * step
        _temp = calc(v, 24.5, *pos_target(v), False)
        beta_1, theta_1, theta_2, gamma_2, theta_1_crit, theta_2_ideal = _temp
        if (theta_2_ideal - theta_2 < tolerance):
            RES = _temp
            print(f"探索中断 (β1: {v} deg)")
            break
        elif (theta_2_ideal < theta_2) or (theta_1_crit < theta_1):
            print(f"探索中断 (β1: {RES[0]} deg)")
            break
        RES = _temp
    
    beta_1, theta_1, theta_2, gamma_2, theta_1_crit, theta_2_ideal = RES
    print(f"\n======\n入射角 = {round(theta_1, 4)} deg\n  (臨界まで: 約{round(theta_1_crit - theta_1, 3)} deg)\n屈折角 = {round(theta_2, 4)} deg\n  (理想値との差: 約{round(theta_2_ideal - theta_2, 3)} deg)\n傾斜角 = {gamma_2}\n")