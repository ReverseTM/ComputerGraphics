import pygame
import customtkinter
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

rotation_angle_x = 0.0
rotation_angle_y = 0.0

rotate_up = False
rotate_down = False
rotate_left = False
rotate_right = False
scale_up = False
scale_down = False

scale_factor = 1.0
clip_height = 1.2


def draw_clipped_sphere(radius, sides, vertical_scale, horizontal_scale, rotation_angle_x):
    for i in range(-sides // 2, sides // 2):
        lat1 = math.pi * (i / sides)
        z1 = math.sin(lat1) * radius * vertical_scale
        zr1 = math.cos(lat1) * radius * horizontal_scale

        lat2 = math.pi * ((i + 1) / sides)
        z2 = math.sin(lat2) * radius * vertical_scale
        zr2 = math.cos(lat2) * radius * horizontal_scale

        glBegin(GL_QUAD_STRIP)
        for j in range(sides + 1):
            lon = 2 * math.pi * (j / sides)
            x = math.cos(lon + rotation_angle_x) * zr2
            y = math.sin(lon + rotation_angle_x) * zr2
            glVertex3f(x, y, z2)

            x = math.cos(lon + rotation_angle_x) * zr1
            y = math.sin(lon + rotation_angle_x) * zr1
            glVertex3f(x, y, z1)
        glEnd()

def draw_filled_circles(radius, sides, vertical_scale, horizontal_scale, rotation_angle_x):
    for i in range(-sides // 2, sides // 2):
        lat = math.pi * (i / sides)
        z = math.sin(lat) * radius * vertical_scale
        zr = math.cos(lat) * radius * horizontal_scale

        glBegin(GL_TRIANGLE_FAN)
        for j in range(sides + 1):
            lon = 2 * math.pi * (j / sides)
            x = math.cos(lon + rotation_angle_x) * zr
            y = math.sin(lon + rotation_angle_x) * zr
            glVertex3f(x, y, z)
        glEnd()


def handle_events():
    global rotate_up, rotate_down, rotate_left, rotate_right, scale_up, scale_down, scale_factor, clip_height
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                rotate_up = True
            elif event.key == pygame.K_DOWN:
                rotate_down = True
            elif event.key == pygame.K_LEFT:
                rotate_left = True
            elif event.key == pygame.K_RIGHT:
                rotate_right = True
            elif event.key == pygame.K_PAGEUP:
                scale_up = True
            elif event.key == pygame.K_PAGEDOWN:
                scale_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                rotate_up = False
            elif event.key == pygame.K_DOWN:
                rotate_down = False
            elif event.key == pygame.K_LEFT:
                rotate_left = False
            elif event.key == pygame.K_RIGHT:
                rotate_right = False
            elif event.key == pygame.K_PAGEUP:
                scale_up = False
            elif event.key == pygame.K_PAGEDOWN:
                scale_down = False


def draw_figure(entry):
    global rotation_angle_x, rotation_angle_y, clip_height, scale_factor
    light_parameters = [int(i) for i in entry.get().split(' ')]
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glLightfv(GL_LIGHT0, GL_POSITION, light_parameters)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glEnable(GL_LIGHT0)
    glMaterial(GL_FRONT, GL_DIFFUSE, [0.0, 0.0, 1.0, 1.0])  # Blue material for the sphere

    vertical_scale = 2.0

    clock = pygame.time.Clock()

    while True:
        
        handle_events()

        rotation_angle_x += 0.01

        if rotate_up:
            glRotatef(-5, 5, 0, 0)
        elif rotate_down:
            glRotatef(5, 5, 0, 0)

        if rotate_left:
            rotation_angle_y -= 5
            glRotatef(-5, 0, 1, 0)  # Rotate around the Y-axis
        elif rotate_right:
            rotation_angle_y += 5
            glRotatef(5, 0, 1, 0)   # Rotate around the Y-axis

        if scale_up:
            scale_factor += 0.010
        elif scale_down:
            scale_factor -= 0.010
            
        # Вращение сцены
        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Усечение сферы
        glEnable(GL_CLIP_PLANE0)
        glClipPlane(GL_CLIP_PLANE0, (0, 0, 1, clip_height * scale_factor))
        glEnable(GL_CLIP_PLANE1)
        glClipPlane(GL_CLIP_PLANE1, (0, 0, -1, clip_height * scale_factor))

        # Отрисовка
        draw_clipped_sphere(1, 20, vertical_scale * scale_factor, scale_factor, rotation_angle_x)
        draw_filled_circles(1, 20, vertical_scale * scale_factor, scale_factor, rotation_angle_x)

        glDisable(GL_CLIP_PLANE0)
        glDisable(GL_CLIP_PLANE1)

        pygame.display.flip()
        pygame.time.wait(10)


def show_interface():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    window = customtkinter.CTk()
    window.geometry("320x240")

    frame = customtkinter.CTkFrame(master=window)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame, text="parameter a value")
    label.pack(pady=30, padx=10)

    entry = customtkinter.CTkEntry(master=frame, placeholder_text="Enter a light parameters")
    entry.pack(pady=10, padx=10)

    button = customtkinter.CTkButton(master=frame, text="Do it", command=lambda: draw_figure(entry))
    button.pack(pady=10, padx=10)

    window.mainloop()


def main():
    show_interface()


if __name__ == '__main__':
    main()
    