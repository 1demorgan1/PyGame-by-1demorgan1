import pygame
import random


pygame.init()

# размеры окна
screen_width = 480
screen_height = 480
game_screen = pygame.display.set_mode((screen_width, screen_height))

# нужные цвета
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# fps - кадрый в секунду ( вау )
# если этот параметр изменять, то игра будет идти медленней или быстрей ( 10 самый оптимальный, если меньше, то отклик
# долгий очень:)
fps = 10

# 1 клетка будет 48 на 48
cell_size = 48
num_cells = screen_width // cell_size

# загрузка картинок
tile_light = pygame.image.load("tile_light.png")
tile_light = pygame.transform.scale(tile_light, (cell_size, cell_size))

tile_dark = pygame.image.load("tile_dark.png")
tile_dark = pygame.transform.scale(tile_dark, (cell_size, cell_size))

head = pygame.image.load("head.png")
head = pygame.transform.scale(head, (cell_size, cell_size))

body = pygame.image.load("body.png")
body = pygame.transform.scale(body, (cell_size, cell_size))

food = pygame.image.load("fruit.png")
food = pygame.transform.scale(food, (cell_size, cell_size))

font = pygame.font.Font(None, 48)

# через fps будем работать с временем, поэтому и взяли 10
clock = pygame.time.Clock()

# класс Змейки - движущегося объекта
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = head
        self.rect = self.image.get_rect()
        self.rect.x = screen_width / 2
        self.rect.y = screen_height / 2
        self.direction = "right"
        self.body_parts = [] # все "дольки" змейки
        self.grow() # сделаем как во всех Змейках - 3 частички со старта
        self.grow()
        self.grow()

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.direction != "down":
            self.direction = "up"
        elif keys[pygame.K_DOWN] and self.direction != "up":
            self.direction = "down"
        elif keys[pygame.K_LEFT] and self.direction != "right":
            self.direction = "left"
        elif keys[pygame.K_RIGHT] and self.direction != "left":
            self.direction = "right"
        
        # движение змейки
        if self.direction == "right":
            self.rect.x += cell_size
            if self.rect.x > screen_width - 1:
                self.rect.x = 0
        elif self.direction == "left":
            self.rect.x -= cell_size
            if self.rect.x < 0:
                self.rect.x = screen_width - cell_size
        elif self.direction == "up":
            self.rect.y -= cell_size
            if self.rect.y < 0:
                self.rect.y = screen_height - cell_size
        elif self.direction == "down":
            self.rect.y += cell_size
            if self.rect.y > screen_height - 1:
                self.rect.y = 0

    # добавим новую частичку для змейки
    def grow(self):
        self.body_parts.insert(0, (self.rect.x, self.rect.y))
        
# еда - очки для игры и способ увеличения самой змейки
class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = food
        self.rect = self.image.get_rect()
        self.randomize_position() # рандомная позиция на экране для еды

    def randomize_position(self): # новые координаты для еды
        self.rect.x = random.randrange(0, screen_width - cell_size, cell_size)
        self.rect.y = random.randrange(0, screen_height - cell_size, cell_size)

# главное, самое первое меню
def menu_screen():
    # координаты для кнопок
    play_button = pygame.Rect(0, 0, 8*cell_size, 2*cell_size)
    exit_button = pygame.Rect(0, 0, 8*cell_size, 2*cell_size)
    play_button.center = (screen_width // 2, 5*cell_size)
    exit_button.center = (screen_width // 2, screen_height - 2*cell_size)

    while True:
        for event in pygame.event.get():
            # выход из игры
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN: # начинаем работу с кликом
                if play_button.collidepoint(event.pos):
                    game() # функция игры - сама игра
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    quit()

        # игровое поле
        for row in range(num_cells):
            for col in range(num_cells):
                if (row + col) % 2 == 0:
                    image = tile_light
                else:
                    image = tile_dark
                game_screen.blit(image, (col * cell_size, row * cell_size))

        text = font.render("ЗМЕЙКА", True, black)
        game_screen.blit(text, (screen_width // 2 - text.get_width() // 2, cell_size * 1 - text.get_height() // 2))
        
        # рисуем кнопки
        pygame.draw.rect(game_screen, black, play_button) 
        pygame.draw.rect(game_screen, black, exit_button)

        # делаем текст кнопок
        text = font.render("Играть", True, white)
        text_rect = text.get_rect(center=play_button.center)
        game_screen.blit(text, text_rect)

        text = font.render("Выйти", True, white)
        text_rect = text.get_rect(center=exit_button.center)
        game_screen.blit(text, text_rect)

        pygame.display.update() # обновляем экран

# функция игры в змейку
def game():
    # создаем змею, еду
    all_sprites = pygame.sprite.Group()
    snake = Snake()
    food = Food()
    all_sprites.add(snake, food)

    # счетчик очков
    score = 0

    # играем в игру
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # игровое поле
        for row in range(num_cells):
            for col in range(num_cells):
                if (row + col) % 2 == 0:
                    image = tile_light
                else:
                    image = tile_dark
                game_screen.blit(image, (col * cell_size, row * cell_size))

        # обновление объектов - змейка и еда
        all_sprites.update()
        all_sprites.draw(game_screen)

        # работа с телом змеи
        if snake.body_parts:
            snake.body_parts.pop()
            snake.body_parts.insert(0, (snake.rect.x, snake.rect.y))

            for i, part in enumerate(snake.body_parts):
                if i == 0:
                    continue
                game_screen.blit(body, part)
                # проверка на столкновения с собой
                if snake.rect.x == part[0] and snake.rect.y == part[1]:
                    game_over(score)

        # проверка на поедание еды
        if pygame.sprite.collide_rect(snake, food):
            food.randomize_position()
            score += 10
            snake.grow()

        text = font.render(str(score), True, black)
        text_rect = text.get_rect(center=(screen_width // 2, cell_size // 2))
        game_screen.blit(text, text_rect)

        pygame.display.update()

        # задание частоты кадров
        clock.tick(fps)

# экран когда мы проиграли
def game_over(score):

    back_to_menu_button = pygame.Rect(0, 0, 8*cell_size, 2*cell_size)
    restart_button = pygame.Rect(0, 0, 8*cell_size, 2*cell_size)
    back_to_menu_button.center = (screen_width // 2, screen_height - 2*cell_size)
    restart_button.center = (screen_width // 2, 5*cell_size)
    # ждем дальнейшнего действия от игрока, а пока что пускаем его в ожидании
    # и пока что проверяем на выход из игры
    while True:
        for event in pygame.event.get():
            # выход из игры
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # если клик мышки
            if event.type == pygame.MOUSEBUTTONDOWN:
                # если ЛКМ
                if event.button == 1:
                    # если кнопка - Back to menu
                    if back_to_menu_button.collidepoint(event.pos):
                        menu_screen()
                    # если кнопка - restart
                    elif restart_button.collidepoint(event.pos):
                        game()

        # игровое поле
        for row in range(num_cells):
            for col in range(num_cells):
                if (row + col) % 2 == 0:
                    image = tile_light
                else:
                    image = tile_dark
                game_screen.blit(image, (col * cell_size, row * cell_size))

        text = font.render("ВЫ ПРОИГРАЛИ!", True, black)
        game_screen.blit(text, (screen_width // 2 - text.get_width() // 2, cell_size * 1 - text.get_height() // 2))

        text = font.render(str(score), True, black)
        game_screen.blit(text, (screen_width // 2 - text.get_width() // 2, cell_size * 2.5 - text.get_height() // 2))

        # рисуем кнопки
        pygame.draw.rect(game_screen, black, back_to_menu_button) 
        pygame.draw.rect(game_screen, black, restart_button)

        # отображаем текст кнопок
        text = font.render("Начать заново", True, white)
        text_rect = text.get_rect(center=restart_button.center)
        game_screen.blit(text, text_rect)

        text = font.render("Выйти в меню", True, white)
        text_rect = text.get_rect(center=back_to_menu_button.center)
        game_screen.blit(text, text_rect)

        pygame.display.update()

menu_screen()