from msvcrt import getch
import os
import numpy as np
from math import sin, cos
import sys

os.system('')  # init ansi

os.system('cls')

class Screen:
    def __init__(self):
        self.pixels = np.zeros((120, 80, 3))

    def render(self):
        data = '\033[H'
        for y in range(0, self.pixels.shape[1], 2):
            for x in range(0, self.pixels.shape[0]):
                u, d = self.pixels[x, y,:], self.pixels[x, y+1,:]
                r1, g1, b1 = u
                r2, g2, b2 = d
                data += f'\033[48;2;{int(r1)};{int(g1)};{int(b1)}m\033[38;2;{int(r2)};{int(g2)};{int(b2)}m▄'
            data += '\033[0m\n'
        print(data, end='')
        sys.stdout.flush()

screen = Screen()

for x in range(120):
    for y in range(80):
        screen.pixels[x, y] = [x * 255 // 120, y * 255 // 120, 0]

screen.render()

exit()

def double_pendulum(theta1, theta2, omega1, omega2, l1, l2, m1, m2, g, dt):
    alpha1 = (-g*(2*m1 + m2 )*sin(theta1)-g*m2 *sin(theta1 -2*theta2 )-2*m2 *sin(theta1 -theta2 )*(omega2 *omega2 *l2 +omega1 *omega1 *l1 *cos(theta1 -theta2 )))/(l1 *(2*m1 +m2 -m2 *cos(2*theta1 -2*theta2 )))
    alpha2 = (2*sin(theta1 - theta2))*(omega1*omega1 *l1 *(m1 +m2 ) + g*(m1 +m2 )*cos(theta1) + omega2 *omega2 *l2 *m2 *cos(theta1 -theta2 )  )/l2 /(  2*m1 +m2 -m2 *cos(2*theta1 -2*theta2 ))

    omega1 += dt*alpha1;
    omega2 += dt*alpha2;
    theta1 += dt*omega1;
    theta2 += dt*omega2;

    return theta1, theta2, omega1, omega2

def get_integer_points(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    points = []
    while True:
        points.append((x1, y1))
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    return points

theta1, theta2, omega1, omega2, l1, l2, m1, m2, g, dt = 2, -2, 0, 0, 1, 1, 1, 1, 9.81, 0.001

while True:
    for _ in range(30):
        theta1, theta2, omega1, omega2 = double_pendulum(theta1, theta2, omega1, omega2, l1, l2, m1, m2, g, dt)

    for x in range(120):
        for y in range(80):
            screen.pixels[x, y,:] = [0, 0, 0]

    x1, y1 = -l1 * sin(theta1), l1 * cos(theta1)
    x2, y2 = x1 - l2 * sin(theta2), y1 + l2 * cos(theta2)
    scale = 18

    for x, y in get_integer_points(60, 40, int(x1 * scale + 60), int(y1 * scale + 40)):
        screen.pixels[x, y,:] = [0, 255, 0]
    for x, y in get_integer_points(int(x1 * scale + 60), int(y1 * scale + 40), int(x2 * scale + 60), int(y2 * scale + 40)):
        screen.pixels[x, y,:] = [0, 255, 255]

    screen.render()
