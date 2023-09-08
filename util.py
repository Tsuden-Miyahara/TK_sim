

from math import sqrt, degrees as deg, radians as rad, sin, tan, asin

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