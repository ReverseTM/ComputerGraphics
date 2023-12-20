import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math


def draw_clipped_sphere(radius, sides, vertical_scale):
    for i in range(-sides // 2, sides // 2):
        lat1 = math.pi * (i / sides)
        z1 = math.sin(lat1) * radius * vertical_scale
        zr1 = math.cos(lat1) * radius

        lat2 = math.pi * ((i + 1) / sides)
        z2 = math.sin(lat2) * radius * vertical_scale
        zr2 = math.cos(lat2) * radius

        glBegin(GL_QUAD_STRIP)
        for j in range(sides + 1):
            lon = 2 * math.pi * (j / sides)
            x = math.cos(lon) * zr2
            y = math.sin(lon) * zr2
            glVertex3f(x, y, z2)

            x = math.cos(lon) * zr1
            y = math.sin(lon) * zr1
            glVertex3f(x, y, z1)
        glEnd()


def draw_filled_circles(radius, sides, vertical_scale):
    for i in range(-sides // 2, sides // 2):
        lat = math.pi * (i / sides)
        z = math.sin(lat) * radius * vertical_scale
        zr = math.cos(lat) * radius

        glBegin(GL_TRIANGLE_FAN)
        for j in range(sides + 1):
            lon = 2 * math.pi * (j / sides)
            x = math.cos(lon) * zr
            y = math.sin(lon) * zr
            glVertex3f(x, y, z)
        glEnd()


def main():
    # Инициализация Pygame
    pygame.init()

    # Установка режима отображения и перспективы
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    # Настройка света и материала
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 1, 0, 3])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glEnable(GL_LIGHT0)
    glMaterial(GL_FRONT, GL_DIFFUSE, [0.0, 0.0, 1.0, 1.0])  # Синий материал для сферы

    # Параметры отсечения
    vertical_scale = 2.0
    clip_height = 1.2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Вращение сцены
        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Включение и настройка отсечения
        glEnable(GL_CLIP_PLANE0)
        glClipPlane(GL_CLIP_PLANE0, (0, 0, 1, clip_height))
        glEnable(GL_CLIP_PLANE1)
        glClipPlane(GL_CLIP_PLANE1, (0, 0, -1, clip_height))

        # Отрисовка сферы с отсечением и кругов
        draw_clipped_sphere(1, 20, vertical_scale)
        draw_filled_circles(1, 20, vertical_scale)

        # Отключение отсечения
        glDisable(GL_CLIP_PLANE0)
        glDisable(GL_CLIP_PLANE1)

        # Обновление экрана
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
