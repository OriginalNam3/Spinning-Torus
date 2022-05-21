import numpy as np
from numpy import sin, cos

r1 = 2  # radius of torus
r2 = 1  # radius of each ring

zoom = 2
cam = 5  # camera pos = [0, 0, cam], display is always at cam - zoom
light = [0, -1, 1]  # take dot product with normal to find light intensity
brightness = 10  # constant for scaling the dot product

# rotations per frame
a = 0.02  # z rotation
b = 0.01  # y rotation
c = 0.04  # x rotation


def mmul(ma, mb):  # multiply 3x3 matrices
    product = [[0 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                product[i][k] += ma[i][j] * mb[j][k]
    return product


rx = [[cos(a), -sin(a), 0], [sin(a), cos(a), 0], [0, 0, 1]]
ry = [[cos(b), 0, sin(b)], [0, 1, 0], [-sin(b), 0, cos(b)]]
rz = [[1, 0, 0], [0, cos(c), -sin(c)], [0, sin(c), cos(c)]]
rm = mmul(mmul(rx, ry), rz)  # rotational matrix
cur = rm  # current orientation

chars = ".,-~:;=!*#$@"  # alphabet for display

res = 80  # resolution
scale = 2 / res


def rotate(v):  # rotates v to cur orientation
    product = [0, 0, 0]
    for i in range(3):
        for j in range(3):
            product[j] += v[i] * cur[i][j]
    for i in range(3):
        v[i] = product[i]


def unit(v):  # returns unit vector of v
    x, y, z = v
    size = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    x /= size
    y /= size
    z /= size
    return [x, y, z]


def get_light(a):  # returns dot product
    product = 0
    for k in range(3):
        product += a[k] * light[k]
    return product


torus = []
i = 0
while i < 6.28:  # generate points on torus
    j = 0
    while j < 6.28:
        sini = sin(i)
        sinj = sin(j)
        cosi = cos(i)
        cosj = cos(j)
        coords = [sini * (r1 + r2 * cosj), cosi * (r1 + r2 * cosj), r2 * sinj]
        norm = unit([sini * cosj, cosi * cosj, sinj])
        torus.append([coords, norm])
        j += 0.02
    i += 0.05

while True:
    display = [[' ' for _ in range(2 * res)] for _ in range(res)]  # 2*res x res resolution
    mxz = [[-100 for _ in range(2 * res)] for _ in range(res)]
    for _v, _normal in torus:
        v = _v[:]
        rotate(v)
        x, y, z = v

        f = (zoom / (cam - z))
        i = res + int((x * f) / scale)
        j = int(res / 2) + int((y * f) / (scale * 3))

        if 0 <= i < 2 * res and 0 <= j < res and z > mxz[j][i]:
            mxz[j][i] = z
            normal = _normal[:]
            rotate(normal)
            # to_light = unit([light[0] - x, light[1] - y, light[2] - z])
            # to_cam = unit([cam[0] - x, cam[1] - y, cam[2] - z])
            # N = max(0, int(dot(to_cam, to_light) * 11))  # how tf do I calculate light
            N = max(0, min(11, int(get_light(normal) * brightness)))
            display[j][i] = chars[N]

    print(*["".join(row) for row in display], sep="\n")
    cur = mmul(cur, rm)

