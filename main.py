import os.path
import pygame
import random
from pygame import mixer
pygame.display.set_caption("Game")
#Иницилализация
pygame.init()
mixer.init()
#Constant
WIDTH = 600
HEIDTH = int(WIDTH * 1.2)
score = 0
WHITE = (255, 255, 255)
#Шрифты
font_small = pygame.font.SysFont('Lucida Sana', 45)
font_big = pygame.font.SysFont('Lucida Sana', 60)
cloud_move = False

FPS = 60
#проверка файла
if os.path.exists("score.txt"):
    with open("score.txt", "r") as file:
        x = file.read()
        heidth_score = int(x)
else:
    heidth_score = 0

clock = pygame.time.Clock()
GRAVITY = 1
MAX_CLOUD = 15
count_jump = 0
SCROLLE = 200
scrolle = 0
scrool_bg = 0
gameover = False
SCORE = 0
#Создание игравого окна
screen = pygame.display.set_mode((WIDTH, HEIDTH))
#Загрузка изображения
bg_img = pygame.image.load("assert/bluemoon.png").convert_alpha()
player_img = pygame.image.load("assert/jump.png").convert_alpha()
cloud_img = pygame.image.load("assert/облако.png").convert_alpha()
ufo_img = pygame.image.load("assert/ufo-space.png").convert_alpha()
ufo_img.set_colorkey(WHITE)

#Загрука Музыки
# jump_simpl =pygame.mixer.Sound("")
bg_musik = mixer.music.load("assert/Galaxy.mp3")
game_over_music =pygame.mixer.Sound("assert/game_over_mus.mp3")
# juump_simpl =pygame.mixer.Sound("assert/jump_mp3.mp3")
game_over_music.set_volume(0.2)
#Установка уровня Гормкости


pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0)
#Включение музыки


#Функия для рисования фона
def drow_screen(scrool_bg):
    screen.blit(bg_img, (0, 0 + scrool_bg))
    screen.blit(bg_img, (0, - HEIDTH + scrool_bg))
def draw_text(text, font, text_colot, x, y):
    img = font.render(text, True, text_colot)
    screen.blit(img, (x, y))

#функция отрисовки панели игрока
def draw_panel():

    draw_text(f"Score: {score}", font_small, WHITE, 0, 0)



class Player():

    def __init__(self, x, y):
        #Функция transform.scale увеличевает изображение
        self.image  = pygame.transform.scale(player_img, (45, 45))
        self.heidth = 40
        self.width = 25
        self.rect = pygame.Rect(0, 0, self.width, self.heidth)
        #Начальнве координаты игрока
        self.rect.center = (x, y)
        #Переменная для изначального положения игрока
        self.flip = False
        self.vel_y = 0
        self.move_count = 0
        #  Создание маски для столкновения
        self.mask = pygame.mask.from_surface(self.image)
    def move(self):
        """
        Функция перемешениея игрока по экрану
        :return:
        """
        #сброс переменные
        scrolle = 0
        dx = 0
        dy = 0
        count_jump = 0

        #Проверка окончание игры

        if player.rect.top > HEIDTH:
            gameover = True
        #отслеживание нажатие кнопок на клавиатуры
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.flip = True
            dx = -10
        if key[pygame.K_RIGHT]:
            dx = 10
            self.flip = False
        #Вспомогвтельный прыжок
        if key[pygame.K_SPACE]:
                dy = 0
                dy = - 10
                count_jump+=1
        #выход на esc
        if key[pygame.K_ESCAPE]:
            run = False
            gameover = False
            pygame.quit()

        #Гравитация
        self.vel_y += GRAVITY
        dy += self.vel_y

        #Порверска столкновений с экраном
        if self.rect.left + dx <0:
            dx = -self.rect.left
        if self.rect.right + dx > WIDTH:
            dx = WIDTH - self.rect.right



        #Проверка стокновение с облаком
        for cloud in cloud_grup:
            #Проверка столкновений двух квадратов
            if cloud.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.heidth):
                if self.rect.bottom<cloud.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = cloud.rect.top
                        dy = 0
                        self.vel_y = -20
                        count_jump = 0
                        # juump_simpl.play()

        if self.rect.top <= SCROLLE:
            if self.vel_y < 0:
                scrolle = -dy


        #Обновление позиции игрока
        self.rect.x += dx
        self.rect.y += dy + scrolle




        return scrolle

    def draw(self):
        """
        отричовка элемента  и игрока н  экране
        :return:
        """
        # отрисовка квадрата для получения для столкновений
        #transform.flip(аргументы само изображение. начальноре положение. устнановка флага
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x -12,self.rect.y -5))
        # #Отрисовка прямоугольника для определения столкновения
        # pygame.draw.rect(screen, WIDTH, self.rect, 2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, y, ):
        pygame.sprite.Sprite.__init__(self)
        self.direection = random.choice([-1,1])
        self.image =  pygame.transform.scale(ufo_img, (45, 45))
        self.rect = self.image.get_rect()


        if self.direection == 1:
            self.rect.x = 0
        else:
            self.rect.x = WIDTH
        self.rect.y = y
    #Обновление Врага
    def update(self, width, srolle):
        #Перемещение по экрану
        self.rect.x += self.direection * 2
        self.rect.y += scrolle
        #Проверка Столкновение с экраном Врага
        if self.rect.right < 0 or self.rect.left > width:
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, width, cloud_move):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(cloud_img, (width, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move = cloud_move
        self.move_counter = random.randint(0, 50 )
        self.direction = random.choice([-1, 1])
        self.speed_cloud = random.randint(1, 2)

    def update(self, scrolle):
        # Проверка движующегося облака
        if self.move == True:
            #отрисовка движующегося блака
            self.rect.x +=self.direction * self.speed_cloud
            self.move_counter +=1
        self.rect.y += scrolle
        #Изменения напрвление облака
        if self.move_counter>= 100 or self.rect.left < 0 or self.rect.right >HEIDTH:
            self.direction *= -1
            self.move_counter = 0
        #Проверка исчезновение облака
        if self.rect.top > HEIDTH:
            self.kill()


run = True

#Вызов класс игрока

player = Player(WIDTH//2, HEIDTH//2)
# Создание группы облаков
cloud_grup = pygame.sprite.Group()
enemy_groop  = pygame.sprite.Group()
#Отрисовка стратовой платформы
cloud = Cloud(WIDTH//2 - 50, HEIDTH - 200, 90, False)
cloud_grup.add(cloud)

#Главный цыкл программы
while run:

    clock.tick(FPS)
    scrolle = player.move()
    scrool_bg += scrolle

    if gameover == False:
        #Обновление облаков
        scrool_bg += scrolle
        if scrool_bg > HEIDTH:
            scrool_bg = 0

        drow_screen(scrool_bg)

        # pygame.draw.line(screen, WHITE, (0, SCROLLE), (WIDTH, SCROLLE))
        #Отрисовка облаков
        if len(cloud_grup)< MAX_CLOUD:
            c_w = random.randint(70 , 90)
            c_x = random.randint(0, WIDTH - c_w)
            c_y = cloud.rect.y - random.randint(80, 120)
            cloud_tipe = random.randint(1, 2)

            #Проверка очков ПРи 300 очках начинают двигаться облака
            if score > 300:
                if cloud_tipe == 1:
                    cloud_move = True
                else:
                    cloud_move = False
            cloud = Cloud(c_x, c_y, c_w, cloud_move )
            cloud_grup.add(cloud)
        #Проверка врага на поле
        if len(enemy_groop) == 0 and score > 1500:
            ememy = Enemy(100)
            enemy_groop.add(ememy)
        #Обновление очков
        if scrolle > 0:
            score += scrolle

        #Отрисовка линии предыдущего рекорда
        pygame.draw.line(screen, WHITE, (0, score - heidth_score + SCROLLE), (WIDTH, score - heidth_score + SCROLLE), 3)
        draw_text("max_score",font_small,  WHITE, WIDTH - 130, score - heidth_score +SCROLLE)
        #Отрисовка игрока
        player.draw()
        #Отрисовка Очков
        draw_panel()
        #Отрисовка Врага
        enemy_groop.draw(screen)
        #обновление облаков
        cloud_grup.update(scrolle)
        #обновление  врагов
        enemy_groop.update(WIDTH, scrolle)
        #Отрисовка Облаков
        cloud_grup.draw(screen)
        # #Временая рамка для отслеживание столкновение
        # for i in enemy_groop:
        #     pygame.draw.rect(screen, WHITE, i.rect, 1)
        #Проверка столкновение с Sprite с группой Sprites
        if  pygame.sprite.spritecollide(player, enemy_groop, False):
            #Вторая проверка столкновения для более точного определения столкновения
            if pygame.sprite.spritecollide(player, enemy_groop, False, pygame.sprite.collide_mask):
                game_over_music.play()
                gameover = True

        # Проверка столкновение с концом экрана конец игры
        if player.rect.top > HEIDTH:
            game_over_music.play()
            gameover = True


    else:
        # Отрисовка текста
        draw_text("Game Over", font_big, (255, 0,0, 0), WIDTH // 2 - 100 , 200)
        draw_text(f"Очки:{score} ", font_small, (255, 255, 0, 0), WIDTH // 2 - 100, 250)
        pygame.mixer.music.stop()


        #Открытие файла для записи очков
        if score > heidth_score:
            heidth_score = score
            with open("score.txt", "w") as file:
                file.write(str(heidth_score))

        key = pygame.key.get_pressed()
        #Restart
        if key[pygame.K_r]:
            gameover = False
            score = 0
            scrolle = 0

            player.rect.center = (WIDTH // 2, HEIDTH // 2)
            cloud_grup.empty()
            #Рестарт Враги
            enemy_groop.empty()
            cloud = Cloud(WIDTH // 2 - 50, HEIDTH - 200, 90, False)

            cloud_grup.add(cloud)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    pygame.display.update()
pygame.quit()
