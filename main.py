from math import radians as rad, degrees as deg, sin, cos, tan, asin, atan2

from util import LINE2D, line_circle_intersection, snell_s_law

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

class N:
    AIR = 1
    GLASS = 1.459
    ACRYLIC_RESIN = 1.49

def calc(b_pos_x: float, b_pos_y: float, beta_1: float, holder_r: float, tube_r: float, tube_thickness: float = 1):
    """
    :param b_pos_x: 照射位置 (X)
    :param b_pos_y: 照射位置 (Y)
    :param beta_1: β1の角度
    :param holder_r: 液菅ホルダーの半径
    :param tube_r: 液菅の半径
    :param tube_thickness: 液菅の厚さ
    :return: (θ6, θ6が平行になるときの角度)
    """
    b_pos = (b_pos_x, b_pos_y)
    tube_center_pos = (0, -holder_r + tube_r)
    tube_center_pos_x, tube_center_pos_y = tube_center_pos
    
    # 入射光 (line1) の式を求める
    line1 = LINE2D.getFromPosAndDeg(*b_pos, beta_1)
    
    # 入射光と円の交点 (c1) の座標を求める
    _c1_poses = line_circle_intersection(line1, *(0, 0), holder_r)
    if not _c1_poses: raise Exception('入射光 (line1) がホルダーを通らない')
    _, c1_pos = _c1_poses
    c1_pos_x, c1_pos_y = c1_pos
    
    # α1を求める
    _270deg_minus_alpha_1 = (deg( atan2(c1_pos_y - 0, c1_pos_x - 0) ) + 360) % 360
    alpha_1 = 270 - _270deg_minus_alpha_1
    
    # θ1を求める
    theta_1 = 90 - (alpha_1 + beta_1)
    
    # θ2を求める
    theta_2, _ = snell_s_law(theta_1, N.ACRYLIC_RESIN, N.AIR)
    if not theta_2: raise Exception('全反射（c1）')
    
    # 入射光 (line2) の式を求める
    _line2_angle = 90 - (alpha_1 + theta_2)
    line2 = LINE2D.getFromPosAndDeg(*c1_pos, _line2_angle)
    
    # 入射光と円の交点 (c2) の座標を求める
    _c2_poses = line_circle_intersection(line2, *tube_center_pos, tube_r)
    if not _c2_poses: raise Exception('入射光 (line2) がホルダーを通らない')
    _, c2_pos = _c2_poses
    c2_pos_x, c2_pos_y = c2_pos
    
    # α2を求める
    _270deg_minus_alpha_2 = (deg( atan2(c2_pos_y - tube_center_pos_y, c2_pos_x - tube_center_pos_x) ) + 360) % 360
    alpha_2 = 270 - _270deg_minus_alpha_2
    
    # θ3を求める
    _x = 90 - (alpha_1 + theta_2)
    theta_3 = 180 - (alpha_2 + 90 + _x)
    
    # θ4を求める
    theta_4, _ = snell_s_law(theta_3, N.AIR, N.GLASS)
    if not theta_4: raise Exception('全反射（c2）')
    
    # 入射光 (line3) の式を求める
    _line3_angle = 90 - (alpha_2 + theta_4)
    line3 = LINE2D.getFromPosAndDeg(*c2_pos, _line3_angle)
    
    # 入射光と円の交点 (A = c3) の座標を求める
    _c3_poses = line_circle_intersection(line3, *tube_center_pos, tube_r - tube_thickness)
    if not _c3_poses: raise Exception('入射光 (line3) がホルダーを通らない')
    _, c3_pos = _c3_poses
    c3_pos_x, c3_pos_y = c3_pos
    
    # α3を求める
    _270deg_minus_alpha_3 = (deg( atan2(c3_pos_y - tube_center_pos_y, c3_pos_x - tube_center_pos_x) ) + 360) % 360
    alpha_3 = 270 - _270deg_minus_alpha_3
    
    # θ5を求める
    theta_5 = (90 - alpha_3) - (90 - alpha_2 - theta_4)
    
    # θ6を求める
    theta_6, _ = snell_s_law(theta_5, N.GLASS, N.AIR)
    if not theta_6: raise Exception('全反射（A = c3）')
    
    return (theta_6, 90 - alpha_3)




CENTER_MARGIN = 1
STATIC_CENTER = (-7.72, -13.29)
class POS:
    @classmethod
    def CENTER(self, _=None):
        return STATIC_CENTER
    @classmethod
    def UPPER(self, beta_1):
        x, y = STATIC_CENTER
        return (x - sin(beta_1) * CENTER_MARGIN, y + cos(beta_1) * CENTER_MARGIN)
    @classmethod
    def LOWER(self, beta_1):
        x, y = STATIC_CENTER
        return (x + sin(beta_1) * CENTER_MARGIN, y - cos(beta_1) * CENTER_MARGIN)


if __name__ == '__main__':
    import os
    from matplotlib import pyplot
    import questionary as qs
    from typing import List
    
    while True:
        os.system('cls')
        
        phi = None
        
        while phi is None or phi == -1:
            phi = qs.select(
                '液菅径',
                choices=[
                    qs.Choice(title="Φ6", value=6),
                    qs.Choice(title="Φ12", value=12),
                    qs.Choice(title="Φ24.5", value=24.5),
                    qs.Choice(title="...その他", value=-1),
                ],
            ).ask()
            if phi == -1:
                phi = -1
                while ((type(phi) is not int) and (type(phi) is not float)) or phi < 0 or 25 < phi:
                    phi = qs.text('液菅径 [mm] (0.0 - 25.0): ').ask()
                    try:
                        phi = float(phi)
                    except ValueError:
                        phi = -1
                        break
        
        pm = -1
        while ((type(pm) is not int) and (type(pm) is not float)) or pm < 0 or 5 < pm:
            pm = qs.text('L1 (= B点の位置誤差) [mm] (0.0 - 5.0)\n  <初期値=1.5>: ').ask()
            if pm == '':
                pm = 1.5
            else:
                try:
                    pm = float(pm)
                except ValueError:
                    continue
        ag = -1
        while ((type(ag) is not int) and (type(ag) is not float)) or ag < 0 or 15 < ag:
            ag = qs.text('θ6の理想値と算出値の最大許容差 [deg] (0.0 - 15.0)\n  <初期値=1>: ').ask()
            if ag == '':
                ag = 1
            else:
                try:
                    ag = float(ag)
                except ValueError:
                    continue
            

        beta_1 = 30.5             # β1の初期値
        
        step = 0.001             # 刻み
        repeat = int(pm * 1000)          # 繰り返し
        
        tolerance = ag         # θ6の理想値と算出値の最大許容差
        
        # 液菅直径 [6 - 24.5]
        tube_d = phi
        
        X: List[float] = []
        Y1: List[float] = []
        Y2: List[float] = []
        OKAY: List[float] = []
        # print(f"探索中 (β1: {beta_1} deg -> {beta_1 - repeat * step} deg [{step}刻み])")
        

        
        is_valid_upper = False
        is_valid_lower = False
        
        for n in range(repeat - 1):
            CENTER_MARGIN = (n + 1) * step
            # upper
            try:
                THETA_6, THETA_6_IDEAL = calc(*POS.UPPER(beta_1), beta_1, 12.7, tube_d / 2, 1)
                print(f"θ6: {THETA_6}, θ6_id: {THETA_6_IDEAL}")
                is_valid_upper = True

                THETA_6_DELTA = THETA_6_IDEAL - THETA_6
                
                X  += [CENTER_MARGIN]
                Y1 += [THETA_6]
                Y2 += [THETA_6_IDEAL]
                
                if (abs(THETA_6_DELTA) < tolerance):
                    OKAY += [CENTER_MARGIN]
                    if False:
                        print(f"探索中断 [{n} / {repeat}] (L1: +{CENTER_MARGIN} mm)")
                        break
            except Exception as e:
                if is_valid_upper:
                    print(f"探索中断 [{n} / {repeat}] (L1: +{CENTER_MARGIN} mm): {e}")
                    break
                print(f"スキップ [{n} / {repeat}] (L1: +{CENTER_MARGIN} mm): {e}")
                
        X.reverse()
        Y1.reverse()
        Y2.reverse()
        
        
        try:
            THETA_6, THETA_6_IDEAL = calc(*POS.CENTER(), beta_1, 12.7, tube_d / 2, 1)
            print(f"θ6: {THETA_6}, θ6_id: {THETA_6_IDEAL}")
            is_valid = True
            THETA_6_DELTA = THETA_6_IDEAL - THETA_6
            X  += [0]
            Y1 += [THETA_6]
            Y2 += [THETA_6_IDEAL]
        except:
            pass
        
        
        for n in range(repeat - 1):
            CENTER_MARGIN = (n + 1) * step
            # lower
            try:
                THETA_6, THETA_6_IDEAL = calc(*POS.LOWER(beta_1), beta_1, 12.7, tube_d / 2, 1)
                print(f"θ6: {THETA_6}, θ6_id: {THETA_6_IDEAL}")
                is_valid_lower = True

                THETA_6_DELTA = THETA_6_IDEAL - THETA_6
                
                X  += [-CENTER_MARGIN]
                Y1 += [THETA_6]
                Y2 += [THETA_6_IDEAL]
                
                if (abs(THETA_6_DELTA) < tolerance):
                    OKAY += [-CENTER_MARGIN]
                    if False:
                        print(f"探索中断 [{n} / {repeat}] (L1: -{CENTER_MARGIN} mm)")
                        break
            except Exception as e:
                if is_valid_lower:
                    print(f"探索中断 [{n} / {repeat}] (L1: -{CENTER_MARGIN} mm): {e}")
                    break
                print(f"スキップ [{n} / {repeat}] (L1: -{CENTER_MARGIN} mm): {e}")
                
                
        l = len(X)
        _max: float = max(Y1 + Y2)
        
        pyplot.title(f'Φ{phi}\nmargin: {ag} [deg]\n Valid L1={round(min(OKAY), 7)}~{round(max(OKAY), 7)}')
        
        pyplot.ylim(0, _max + 5)
        if len(OKAY): pyplot.axvspan(min(OKAY), max(OKAY), color='gray')
        pyplot.plot(X, Y1, '.-', label="calculated")
        pyplot.plot(X, Y2, '.-', label="ideal")
        #pyplot.plot(X[l - 1], Y1[l - 1], '*')
        #pyplot.plot(X[l - 1], Y2[l - 1], '*')
        pyplot.xlabel(f'L1 [mm] (± {pm} mm)')
        pyplot.ylabel('θ6 [deg]')
        
        #pyplot.text(0, 0, f'L1: ± {pm} [mm]\nmargin: {ag} [deg]', bbox={
        #    "facecolor" : "white",
        #    "edgecolor" : "red",
        #    "linewidth" : 1
        #})
        pyplot.legend()
        pyplot.grid()
        pyplot.show()
        
        # qs.text('').ask()

































"""


def calc1(beta1, phy1, b_pos_x, b_pos_y, debug=True):
    # 1, 2
    BETA_1  = beta1            # 入射面交差角
    PHI_1   = phy1            # [mm] 液菅径
    T_1     = 1               # [mm] 液菅厚み
    N_1     = 1.49            # アクリル屈折率
    N_2     = 1.00            # 空気屈折率
    N_3     = 1.459           # 液管屈折率
    L_1     = 0               # [mm] B点の位置誤差

    B_POS   = (b_pos_x, b_pos_y)
    X1, _   = B_POS
    Y1      = X1 / tan( rad(BETA_1) ) # 13.1
    R       = 12.7
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
    N_1_2         = N_2 / N_1
    THETA_1       = 90 - BETA_1 - ALPHA_1
    THETA_2       = get_theta2(N_1_2, THETA_1)
    GAMMA_2       = 90 - ALPHA_1 - THETA_2

    THETA_1_CRIT  = deg(asin(N_1_2))
    THETA_2_IDEAL = 90 - ALPHA_1
    if debug: print(f"#4\n入射角 = {THETA_1} deg (臨界: {THETA_1_CRIT} deg)\n屈折角 = {THETA_2} deg (理想: {THETA_2_IDEAL} deg)\n傾斜角 = {GAMMA_2}\n")

    return (BETA_1, THETA_1, THETA_2, GAMMA_2, THETA_1_CRIT, THETA_2_IDEAL)


    # 変数ここから
    base = 30.5             # β1の初期値
    step = 0.01             # 刻み
    repeat = 1000           # 繰り返し
    
    tolerance = 0.3         # 屈折角の理想値と算出値の最大許容差
    
    pos_target = POS.CENTER # 入射点
    # ここまで
    
    
    X = []
    Y1 = []
    Y2 = []
    RES = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    print(f"探索中 (β1: {base} deg -> {base - repeat * step} deg [{step}刻み])")
    for n in range(repeat):
        v = base - n * step
        _temp = calc1(v, 24.5, *pos_target(v), False)
        beta_1, theta_1, theta_2, gamma_2, theta_1_crit, theta_2_ideal = _temp
        t2 = theta_2_ideal - theta_2
        
        X  += [v]
        Y1 += [theta_2]
        Y2 += [theta_2_ideal]
        
        if (abs(t2) < tolerance):
            RES = _temp
            print(f"探索中断 [{n} / {repeat}] (β1: {v} deg)")
            break
        elif (theta_2_ideal < theta_2) or (theta_1_crit < theta_1):
            print(f"探索中断 [{n - 1} / {repeat}] (β1: {RES[0]} deg)")
            break
        RES = _temp
    
    beta_1, theta_1, theta_2, gamma_2, theta_1_crit, theta_2_ideal = RES
    print(f\"""
======
入射角 = {round(theta_1, 4)} deg
(臨界まで: 約{round(theta_1_crit - theta_1, 3)} deg)
屈折角 = {round(theta_2, 4)} deg
(理想値との差: 約{round(theta_2_ideal - theta_2, 3)} deg)
傾斜角 = {gamma_2}
\"""
    )
    l = len(X)
    
    _max: int = max(Y1 + Y2)
    
    pyplot.ylim(0, _max + 5)
    pyplot.plot(X, Y1, '.-', label="calculated")
    pyplot.plot(X, Y2, '.-', label="ideal")
    pyplot.plot(X[l - 1], Y1[l - 1], '*')
    pyplot.plot(X[l - 1], Y2[l - 1], '*')
    pyplot.xlabel('β1 [deg]')
    pyplot.ylabel('θ2 [deg]')
    pyplot.legend()
    pyplot.grid()
    pyplot.show()

"""