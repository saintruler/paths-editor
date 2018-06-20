import pygame


class Object:
    def __init__(self, x, y, image):
        self.image = image
        self.pos = self.x, self.y = x, y

    def move_to(self, x, y):
        self.pos = self.x, self.y = x, y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.pos = self.x, self.y

    def draw(self, surface):
        rect = self.image.get_rect(
            centerx=w // 2 + self.x - cam.x,
            centery=h // 2 + cam.y - self.y
        )

        surface.blit(self.image, rect)


class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self, surface):
        pygame.draw.line(
            surface, pygame.Color('red'),
            (w // 2 + self.start[0] - cam.x, h // 2 + cam.y - self.start[1]),
            (w // 2 + self.end[0] - cam.x, h // 2 + cam.y - self.end[1]), 5
        )


class Circle:
    def __init__(self, pos):
        self.pos = pos

    def draw(self, surface):
        pygame.draw.circle(
            surface, pygame.Color('green'),
            (w // 2 + self.pos[0] - cam.x, h // 2 + cam.y - self.pos[1]), 15
        )


class Camera:
    def __init__(self, x, y):
        self.pos = self.x, self.y = x, y

    def move_to(self, x, y):
        self.pos = self.x, self.y = x, y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.pos = self.x, self.y


def get_mouse_coord():
    mouse = pygame.mouse.get_pos()
    mouse_x = cam.x + (mouse[0] - w // 2)
    mouse_y = cam.y + (h // 2 - mouse[1])
    return mouse_x, mouse_y


pygame.init()
w, h = size = 1280, 720
screen = pygame.display.set_mode(size)

cam = Camera(0, 0)
obj = Object(0, 0, pygame.image.load('ground_layer.png').convert_alpha())
objects = [obj]

paths = [[]]

line = [None, None]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if line[0] is not None:
                    line[0] = None
            elif event.key == pygame.K_u:
                if paths[-1]:
                    paths[-1].pop()
            elif event.key == pygame.K_RETURN:
                for i, path in enumerate(paths):
                    with open('commands{}.txt'.format(i), 'w', encoding='utf-8') as f:
                        for o in path:
                            if isinstance(o, Line):
                                f.write('move_to {} {}\n'.format(*o.end))
                            elif isinstance(o, Circle):
                                f.write('sleep n\n')
            elif event.key == pygame.K_SPACE:
                paths.append([])

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = get_mouse_coord()
                if line[0] is None:
                    line[0] = pos
                elif line[1] is None:
                    line[1] = pos
                    paths[-1].append(Line(*line))
                    line = [None, None]
            elif event.button == 3:
                if line[0] is None:
                    paths[-1].append(Circle(get_mouse_coord()))

    dx = 0
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        dx -= 1
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        dx += 1

    dy = 0
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        dy -= 1
    if pygame.key.get_pressed()[pygame.K_UP]:
        dy += 1
    cam.move(dx * 2, dy * 2)

    screen.fill(pygame.Color('black'))

    for object_ in objects:
        object_.draw(screen)

    for path in paths:
        for o in path:
            o.draw(screen)

    if line[0] is not None:
        pygame.draw.line(
            screen, pygame.Color('red'),
            (w // 2 + line[0][0] - cam.x, h // 2 + cam.y - line[0][1]),
            pygame.mouse.get_pos(), 5
        )

    pygame.display.flip()
