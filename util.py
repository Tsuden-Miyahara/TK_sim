

from math import sqrt, degrees as deg, radians as rad, sin, tan, asin, atan2

def snell_s_law(incident_angle: float, n1: float, n2: float):
    """
    スネルの法則を用いて屈折角を計算する関数
    :param incident_angle: 入射角（度）
    :param n1: 入射前の媒質の屈折率
    :param n2: 入射後の媒質の屈折率
    :return: (屈折角 [全反射の場合はNone], 臨界角 [存在しない場合はNone])。
    """
    assert 0 <= incident_angle <= 90, "incident_angle must be between 0 and 90 degrees"
    assert n1 > 0 and n2 > 0, "n1 and n2 must be positive"
    incident_angle_rad = rad(incident_angle)
    critical_angle = None
    if n1 > n2:
        critical_angle_rad = asin(n2 / n1)
        critical_angle = deg(critical_angle_rad)
        if incident_angle_rad > critical_angle_rad:
            return (None, critical_angle) # 全反射
    refracted_angle = deg( asin( sin(incident_angle_rad) * n1 / n2 ) )
    return (refracted_angle, critical_angle)

class LINE2D:
    # y = a * x + b
    def __init__(self, a, b) -> None:
        self.a: float = a
        self.b: float = b
    @classmethod
    def getFromPosAndDeg(self, x, y, d):
        a: float = tan(rad(d))
        b: float = y - a * x
        return LINE2D(a, b)
    
    def calcWithX(self, x):
        return self.a * x + self.b
    def calcWithY(self, y):
        return (y - self.b) / self.a


def line_circle_intersection(line: LINE2D, cx: float, cy: float, r: float):
    # 直線の方程式を y = ax + b から x = (y - b) / a に変換
    A = 1 + line.a**2
    B = -2 * cx + 2 * line.a * (line.b - cy)
    C = cx**2 + (line.b - cy)**2 - r**2

    # 判別式
    D = B**2 - 4 * A * C

    if D < 0:
        return None  # 実数解なし: 直線と円は交わらない
    elif D == 0:
        x: float = -B / (2 * A)
        y: float = line.a * x + line.b
        return [(x, y)]  # 実数解が一つ: 直線と円は接する
    else:
        x1: float = (-B + sqrt(D)) / (2*A)
        y1: float = line.a*x1 + line.b
        x2: float = (-B - sqrt(D)) / (2*A)
        y2: float = line.a * x2 + line.b
        return [(x1, y1), (x2, y2)]  # 実数解が二つ: 直線と円は交わる


































def get_theta2(n12, theta1):
    return deg( asin( sin(rad(theta1)) / n12 ) )

def get_poi_of_circle_with_line(cx, cy, r, x1, y1, x2, y2):
    xd = x2 - x1; yd = y2 - y1
    X = x1 - cx; Y = y1 - cy
    a = xd**2 + yd**2
    b = xd * X + yd * Y
    c = X**2 + Y**2 - r**2
    D = b**2 - a*c
    s1 = (-b + sqrt(D)) / a
    s2 = (-b - sqrt(D)) / a
    return (x1 + xd*s1, y1 + yd*s1), (x1 + xd*s2, y1 + yd*s2)


if __name__ == '__main__':
    v = get_poi_of_circle_with_line(
        *(0, 0), # 円の中心
        12.7,    # 円の半径
        *(-7.72, -13.29),
        *(0, -(7.72 * tan(rad(30.5))))
    )
    print(v)
    print(
        snell_s_law(40.1, 1.459, 1)
    )