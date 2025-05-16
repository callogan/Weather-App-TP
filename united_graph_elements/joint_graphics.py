import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from base_renderer import BaseRenderer


class OpenGLRenderer(BaseRenderer):
    def __init__(self):
        super().__init__()
        self.rotation_x = 0.0
        self.rotation_y = 0.0
        self.scale = 1.0
        self.last_x = 0
        self.last_y = 0
        self.mouse_pressed = False
        self.reset_button_width = 150
        self.reset_button_height = 30
        self.window_width = 800
        self.window_height = 600
        self.button_margin_left = 10
        self.button_margin_bottom = 10
        self.update_reset_button_position()
        pygame.font.init()
        self.button_font = pygame.font.SysFont('Arial', 20)
        print("Renderer initialized")

    def update_reset_button_position(self):
        self.reset_button_x = self.button_margin_left
        self.reset_button_y = self.window_height - self.reset_button_height - self.button_margin_bottom

    def resize(self, width, height):
        self.window_width = width
        self.window_height = height
        self.update_reset_button_position()
        glViewport(0, 0, width, height)
        self.setup_projection()

    def init_gl(self):
        try:
            print("Initializing OpenGL...")
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            glEnable(GL_COLOR_MATERIAL)
            glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

            glLightfv(GL_LIGHT0, GL_POSITION, (5.0, 5.0, 5.0, 1.0))
            glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
            glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))
            glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))

            glMaterialfv(GL_FRONT, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
            glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))
            glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
            glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

            self.setup_projection()
            print("OpenGL initialization completed")
        except Exception as e:
            print(f"Error in init_gl: {e}")
            raise

    def setup_projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.window_width / self.window_height, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5.0)

    def resize(self, width, height):
        self.window_width = width
        self.window_height = height
        glViewport(0, 0, width, height)
        self.setup_projection()

    def draw(self):
        try:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            glTranslatef(0.0, 0.0, -5.0)

            glEnable(GL_LIGHTING)

            glScalef(self.scale, self.scale, self.scale)

            glRotatef(self.rotation_x, 1, 0, 0)
            glRotatef(self.rotation_y, 0, 1, 0)

            self.draw_cube_with_normals()

            self.draw_reset_button()

        except Exception as e:
            print(f"Error in draw: {e}")
            raise

    def draw_cube_with_normals(self):
        glBegin(GL_QUADS)

        glNormal3f(0, 0, 1)
        glVertex3f(-1, -1, 1)
        glVertex3f(1, -1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(-1, 1, 1)

        glNormal3f(0, 0, -1)
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, 1, -1)
        glVertex3f(1, 1, -1)
        glVertex3f(1, -1, -1)

        glNormal3f(-1, 0, 0)
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, -1, 1)
        glVertex3f(-1, 1, 1)
        glVertex3f(-1, 1, -1)

        glNormal3f(1, 0, 0)
        glVertex3f(1, -1, -1)
        glVertex3f(1, 1, -1)
        glVertex3f(1, 1, 1)
        glVertex3f(1, -1, 1)

        glNormal3f(0, 1, 0)
        glVertex3f(-1, 1, -1)
        glVertex3f(-1, 1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(1, 1, -1)

        glNormal3f(0, -1, 0)
        glVertex3f(-1, -1, -1)
        glVertex3f(1, -1, -1)
        glVertex3f(1, -1, 1)
        glVertex3f(-1, -1, 1)
        glEnd()

    def draw_reset_button(self):
        try:
            glPushAttrib(GL_ALL_ATTRIB_BITS)
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, self.window_width, self.window_height, 0, -1, 1)

            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()

            glDisable(GL_LIGHTING)
            glDisable(GL_DEPTH_TEST)
            glDisable(GL_TEXTURE_2D)

            glBegin(GL_QUADS)
            glColor3f(0.2, 0.2, 0.2)
            glVertex2f(self.reset_button_x, self.reset_button_y)
            glVertex2f(self.reset_button_x + self.reset_button_width, self.reset_button_y)
            glVertex2f(self.reset_button_x + self.reset_button_width, self.reset_button_y + self.reset_button_height)
            glVertex2f(self.reset_button_x, self.reset_button_y + self.reset_button_height)
            glEnd()

            text_surface = self.button_font.render("Reset", True, (255, 255, 255), (51, 51, 51))
            text_data = pygame.image.tostring(text_surface, "RGBA", True)
            text_w, text_h = text_surface.get_width(), text_surface.get_height()

            text_x = int(self.reset_button_x + (self.reset_button_width - text_w) / 2)
            text_y = int(self.reset_button_y + (self.reset_button_height - text_h) / 2 + text_h)
            glRasterPos2f(text_x, text_y)
            glDrawPixels(text_w, text_h, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glPopMatrix()
            glPopAttrib()
        except Exception as e:
            print(f"Error in draw_reset_button: {e}")
            raise

    def reset_position(self):
        print("Resetting position...")
        self.rotation_x = 0.0
        self.rotation_y = 0.0
        self.scale = 1.0
        print("Position reset completed")

    def handle_mouse(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                if (self.reset_button_x <= x <= self.reset_button_x + self.reset_button_width and
                        self.reset_button_y <= y <= self.reset_button_y + self.reset_button_height):
                    print("Reset button clicked")
                    self.reset_position()
                else:
                    self.mouse_pressed = True
                    self.last_x = x
                    self.last_y = y
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_pressed = False
        elif event.type == MOUSEMOTION:
            if self.mouse_pressed:
                x, y = event.pos
                dx = x - self.last_x
                dy = y - self.last_y
                self.rotation_y += dx * 0.5
                self.rotation_x += dy * 0.5
                self.last_x = x
                self.last_y = y
        elif event.type == MOUSEWHEEL:
            if event.y > 0:
                self.scale *= 1.1
            else:
                self.scale /= 1.1
            self.scale = max(0.1, min(5.0, self.scale))


def main():
    global renderer

    print("Starting application...")

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Cube")

    renderer = OpenGLRenderer()
    renderer.init_gl()

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                renderer.handle_mouse(event)

            renderer.draw()
            pygame.display.flip()
            pygame.time.wait(10)

    except Exception as e:
        print(f"Error in main loop: {e}")
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
