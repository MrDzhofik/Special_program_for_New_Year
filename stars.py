import os
import random
import glob

import pygame

def get_list_mp3():
    extension = '*.mp3'
    current_directory = os.path.join(os.getcwd(), extension)
    list_mp3 = glob.glob(current_directory)
    return list_mp3

# Пример использования
mp3 = get_list_mp3()

# Вывести список mp3 файлов
print("Список mp3 файлов:")
for i in range(len(mp3)):
    mp3[i] = os.path.basename(mp3[i])
    print(mp3[i])

# Выбор песни
musics = mp3
print("Введите число для выбора песни:")
for i in range(len(musics)):
    print(f'{i + 1} - {musics[i]}')
choice = int(input('>>> '))
music = musics[(choice - 1) % len(musics)]

# инициализация Pygame:
pygame.init()
# размеры окна определяем автоматически:
print(f"Разрешение вашего экрана: {pygame.display.Info().current_w} х {pygame.display.Info().current_h}")
SCREENSIZE = WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h  # 1920, 1200
GRAVITY = 0.08
# частота кадров
FPS = 60
clock = pygame.time.Clock()
# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)



# формирование кадра:
# команды рисования на холсте  
def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # print(fullname)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# для отслеживания улетевших частиц
# удобно использовать пересечение прямоугольников
screen_rect = (0, 0, WIDTH, HEIGHT)


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png", -1)]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))

# Картинка
bg_image = load_image("NG.jpg")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()

# Проигрывание песни
pygame.mixer.music.load(music)
pygame.mixer.music.play(-1)
running = True

running = True
move = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # создаём частицы по щелчку мыши
            if event.button == 1:
                create_particles(pygame.mouse.get_pos())
                move = True
        if event.type == pygame.MOUSEBUTTONUP:
            move = False
        if event.type == pygame.MOUSEMOTION and move:
            create_particles(pygame.mouse.get_pos())

    all_sprites.update()
    screen.blit(bg_image, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
