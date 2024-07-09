import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D ASCII Spinning Donut")
clock = pygame.time.Clock()

# ASCII characters
CHARS = ".,-~:;=!*#$@"

# Donut parameters
A, B = 0, 0
R1, R2, K2 = 1, 2, 5
K1 = WIDTH * K2 * 3 / (8 * (R1 + R2))

def render_frame():
    global A, B
    output = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]
    zbuffer = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

    cosA, sinA = math.cos(A), math.sin(A)
    cosB, sinB = math.cos(B), math.sin(B)

    for theta in range(0, 628, 7):  # 0 to 2*pi
        costheta, sintheta = math.cos(theta / 100), math.sin(theta / 100)
        for phi in range(0, 628, 2):  # 0 to 2*pi
            cosphi, sinphi = math.cos(phi / 100), math.sin(phi / 100)

            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = K2 + cosA * circlex * sinphi + circley * sinA
            ooz = 1 / z

            xp = int(WIDTH / 2 + K1 * ooz * x)
            yp = int(HEIGHT / 2 - K1 * ooz * y)

            luminance = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * (cosA * sintheta - costheta * sinA * sinphi)
            if luminance > 0:
                lindex = int(luminance * 8)
                if 0 <= xp < WIDTH and 0 <= yp < HEIGHT:
                    if ooz > zbuffer[yp][xp]:
                        zbuffer[yp][xp] = ooz
                        output[yp][xp] = CHARS[lindex]

    screen.fill((0, 0, 0))
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if output[i][j] != ' ':
                color_value = int((CHARS.index(output[i][j]) / 11) * 255)
                color = (color_value, 255 - color_value, (color_value * 2) % 255)
                screen.set_at((j, i), color)
    
    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    render_frame()
    A += 0.04
    B += 0.02
    clock.tick(30)

pygame.quit()
  