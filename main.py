# Copyright 2022 Dikanskiy Egor
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# импорт библиотек
import pygame
import time
import random
from pygame import mixer


# класс игры
class Main():
    def __init__(self):
        # инициализация pygame
        self.width, self.height = 800, 480
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Race')
        pygame.display.set_icon(pygame.image.load("Data/Textures/car_icon.bmp"))

        self.WHITE = (255, 255, 255)

        # звгрузка картинок(спрайтов)
        self.foreground1 = pygame.sprite.Sprite()
        self.foreground1.image = pygame.image.load("Data/Textures/autoslalom_1.png").convert_alpha()
        self.foreground1.rect = self.foreground1.image.get_rect()
        self.foreground1.image = pygame.transform.scale(self.foreground1.image, (800, 480))

        self.foreground2 = pygame.sprite.Sprite()
        self.foreground2.image = pygame.image.load("Data/Textures/autoslalom_2.png").convert_alpha()
        self.foreground2.rect = self.foreground2.image.get_rect()
        self.foreground2.image = pygame.transform.scale(self.foreground2.image, (800, 480))

        self.foreground3 = pygame.sprite.Sprite()
        self.foreground3.image = pygame.image.load("Data/Textures/autoslalom_3.png").convert_alpha()
        self.foreground3.rect = self.foreground3.image.get_rect()
        self.foreground3.image = pygame.transform.scale(self.foreground3.image, (800, 480))

        self.foreground_back = pygame.sprite.Sprite()
        self.foreground_back.image = pygame.image.load("Data/Textures/autoslalom_back.png").convert_alpha()
        self.foreground_back.rect = self.foreground_back.image.get_rect()
        self.foreground_back.image = pygame.transform.scale(self.foreground_back.image, (800, 480))

        self.foreground_rigt = pygame.sprite.Sprite()
        self.foreground_rigt.image = pygame.image.load("Data/Textures/autoslalom_right.png").convert_alpha()
        self.foreground_rigt.rect = self.foreground_rigt.image.get_rect()
        self.foreground_rigt.image = pygame.transform.scale(self.foreground_rigt.image, (146, 480))

        self.foreground_left = pygame.sprite.Sprite()
        self.foreground_left.image = pygame.image.load("Data/Textures/autoslalom_left.png").convert_alpha()
        self.foreground_left.rect = self.foreground_left.image.get_rect()
        self.foreground_left.image = pygame.transform.scale(self.foreground_left.image, (157.46, 480))

        self.player_sprite = pygame.sprite.Sprite()
        self.player_sprite.image = pygame.image.load("Data/Textures/car.png").convert_alpha()
        self.player_sprite.rect = self.player_sprite.image.get_rect()
        self.x = 360
        self.y = 310
        self.player_sprite.image = pygame.transform.scale(self.player_sprite.image, (75, 47))

        self.enemy_img = pygame.sprite.Sprite()
        self.enemy_img.image = pygame.image.load("Data/Textures/enemy.png")
        self.enemy_img.rect = self.enemy_img.image.get_rect()
        self.enemy = self.enemy_img.image

        self.enemy_img2 = pygame.sprite.Sprite()
        self.enemy_img2.image = pygame.image.load("Data/Textures/enemy.png")
        self.enemy_img2.rect = self.enemy_img.image.get_rect()
        self.enemy2 = self.enemy_img2.image

        # размеры игрока и препятствий
        self.width_of_player = 75
        self.height_of_player = 47
        self.width_of_enemy = 40
        self.height_of_enemy = 10

        # для записи максимального реккорда
        f = open('Data/Max_Score/max_score.txt', 'r')
        self.score = 0
        self.max_score = f.readlines()[0]
        f.close()

        # запуск игры
        self.game_music = mixer.Sound("Data/Sounds/game.wav")
        self.men = True
        self.play()

    def collision(self):
        # обработка столкновений
        enemy_bottom_right_x = self.e_x + self.width_of_enemy
        enemy_bottom_right_y = self.e_y + self.height_of_enemy
        enemy_bottom_left_x = self.e_x
        enemy_bottom_left_y = self.e_y + self.height_of_enemy

        player_top_right_x = self.x + self.width_of_player
        player_top_right_y = self.y
        player_top_left_x = self.x
        player_top_left_y = self.y

        enemy_bottom_right_x2 = self.e_x2 + self.width_of_enemy
        enemy_bottom_right_y2 = self.e_y2 + self.height_of_enemy
        enemy_bottom_left_x2 = self.e_x2
        enemy_bottom_left_y2 = self.e_y2 + self.height_of_enemy

        if enemy_bottom_right_x <= player_top_right_x and enemy_bottom_right_y >= player_top_right_y and enemy_bottom_left_x >= player_top_left_x:
            return True
        if enemy_bottom_left_x <= player_top_left_x and enemy_bottom_left_y >= player_top_left_y and enemy_bottom_right_x >= player_top_right_x:
            return True
        if enemy_bottom_right_x2 <= player_top_right_x and enemy_bottom_right_y2 >= player_top_right_y and enemy_bottom_left_x2 >= player_top_left_x:
            return True
        if enemy_bottom_left_x2 <= player_top_left_x and enemy_bottom_left_y2 >= player_top_left_y and enemy_bottom_right_x2 >= player_top_right_x:
            return True
        return False

    def add_enemy(self, x, y):
        # добавление 1 препятсвия
        self.screen.blit(self.enemy_img.image, (x, y))

    def add_enemy2(self, x, y):
        # добавление 2 препятсвия
        self.screen.blit(self.enemy_img2.image, (x, y))

    def bg_anim(self):
        # анимация фона
        if self.dt <= 1:
            self.screen.blit(self.foreground1.image, self.foreground1.rect)
        if self.dt >= 1 and self.dt <= 2:
            self.screen.blit(self.foreground2.image, self.foreground2.rect)
        if self.dt >= 2 and self.dt <= 3:
            self.screen.blit(self.foreground3.image, self.foreground3.rect)
        if self.dt >= 3 and self.dt <= 4:
            self.screen.blit(self.foreground1.image, self.foreground1.rect)
        if self.dt >= 4 and self.dt <= 5:
            self.screen.blit(self.foreground2.image, self.foreground2.rect)
        if self.dt >= 5 and self.dt <= 6:
            self.screen.blit(self.foreground3.image, self.foreground3.rect)
        if self.dt >= 6 and self.dt <= 7:
            self.screen.blit(self.foreground1.image, self.foreground1.rect)
        if self.dt >= 7 and self.dt <= 8:
            self.screen.blit(self.foreground2.image, self.foreground2.rect)
        if self.dt >= 8 and self.dt <= 9:
            self.screen.blit(self.foreground3.image, self.foreground3.rect)
        if self.dt >= 9 and self.dt <= 10:
            self.screen.blit(self.foreground1.image, self.foreground1.rect)
        if self.dt >= 10:
            self.screen.blit(self.foreground2.image, self.foreground2.rect)

    def menu(self):
        # меню(старт)
        self.men = True
        self.result = False
        self.run = False
        self.ex = mixer.Sound("Data/Sounds/exit.wav")
        self.start = mixer.Sound("Data/Sounds/start.wav")
        self.start_time = time.time()

        while self.men:
            # основной цикл меню
            self.dt = time.time() - self.start_time
            if self.dt > 10:
                self.start_time = time.time()

            # обьявление кнопок
            play_text = pygame.font.Font("Data/Fonts/digital-7.ttf", 74).render("PLAY", True, (0, 0, 0))
            exit_text = pygame.font.Font("Data/Fonts/digital-7.ttf", 24).render("EXIT", True, (0, 0, 0))

            # отрисовка кнопок
            self.screen.blit(self.foreground_back.image, self.foreground_back.rect)
            self.screen.blit(exit_text, (385, 300))

            # анимация кнопок
            if self.dt <= 1:
                self.screen.blit(play_text, (330, 230))
            if self.dt >= 1 and self.dt <= 2:
                self.screen.blit(play_text, (330, 235))
            if self.dt >= 2 and self.dt <= 3:
                self.screen.blit(play_text, (330, 230))
            if self.dt >= 3 and self.dt <= 4:
                self.screen.blit(play_text, (330, 235))
            if self.dt >= 4 and self.dt <= 5:
                self.screen.blit(play_text, (330, 230))
            if self.dt >= 5 and self.dt <= 6:
                self.screen.blit(play_text, (330, 235))
            if self.dt >= 6 and self.dt <= 7:
                self.screen.blit(play_text, (330, 230))
            if self.dt >= 7 and self.dt <= 8:
                self.screen.blit(play_text, (330, 235))
            if self.dt >= 8 and self.dt <= 9:
                self.screen.blit(play_text, (330, 230))
            if self.dt >= 9 and self.dt <= 10:
                self.screen.blit(play_text, (330, 235))
            if self.dt >= 10:
                self.screen.blit(play_text, (330, 230))

            # обработка нажатий кнопок
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    self.men = False
                    self.result = False
                    self.run = False
                    self.play()
                if (pygame.mouse.get_pos()[0] > 650 and
                        pygame.mouse.get_pos()[1] < 350 and pygame.mouse.get_pos()[1] > 300):
                    if (event.type == pygame.MOUSEBUTTONDOWN):
                        self.run = True
                        self.men = False
                        self.result = False
                        self.start.play()
                        self.play()
                if (pygame.mouse.get_pos()[0] > 650 and
                        pygame.mouse.get_pos()[1] < 75 and pygame.mouse.get_pos()[1] > 50):
                    if (event.type == pygame.MOUSEBUTTONDOWN):
                        self.game_dif = 0
                        self.run = True
                        self.men = False
                        self.result = False
                        self.start.play()
                        self.play()
                if (pygame.mouse.get_pos()[0] > 650 and
                        pygame.mouse.get_pos()[1] < 150 and pygame.mouse.get_pos()[1] > 75):
                    if (event.type == pygame.MOUSEBUTTONDOWN):
                        self.game_dif = 1
                        self.run = True
                        self.men = False
                        self.result = False
                        self.start.play()
                        self.play()
                if (pygame.mouse.get_pos()[0] < self.width / 2 + play_text.get_width() / 2 and
                        pygame.mouse.get_pos()[
                            0] > self.width / 2 - play_text.get_width() / 2):
                    if (pygame.mouse.get_pos()[1] < 280 and
                            pygame.mouse.get_pos()[1] > 250):
                        if (event.type == pygame.MOUSEBUTTONDOWN):
                            self.men = False
                            self.result = False
                            self.run = True
                            self.start.play()
                            self.play()
                    if (pygame.mouse.get_pos()[1] < 320 and
                            pygame.mouse.get_pos()[1] > 300):
                        if (event.type == pygame.MOUSEBUTTONDOWN):
                            self.ex.play()
                            time.sleep(0.5)
                            self.men = False
                            self.result = False
                            self.run = False
                            self.play()

            pygame.display.update()

    def game(self):
        # игра
        self.die = mixer.Sound("Data/Sounds/die.wav")
        self.button = mixer.Sound("Data/Sounds/button.wav")
        # обьявление начальных данных
        self.score = 0
        self.e_x = 550
        self.e_y = 120
        self.e_speed = 0.05
        self.e_speed2 = 0.05
        try:
            if self.game_dif == 0:
                self.e_speed = 0.05
                self.e_speed2 = 0.05
            elif self.game_dif == 1:
                self.e_speed = 0.1
                self.e_speed2 = 0.1
        except AttributeError:
            pass
        self.mn = float(random.choice([0.47, 0.9, 1.4]))
        self.e_x2 = 550
        self.e_y2 = 120
        self.mn2 = float(random.choice([0.47, 0.9, 1.4]))
        self.run = True
        right = False
        left = False
        self.start_time2 = time.time()

        # основной цикл игры
        while self.run:
            self.dt2 = time.time() - self.start_time2
            self.dt = time.time() - self.start_time

            # изменение скорости со временем
            if self.dt > 10:
                self.e_speed *= 1.25
                self.e_speed2 *= 1.15
                self.start_time = time.time()

            self.screen.fill(self.WHITE)
            self.bg_anim()

            for event in pygame.event.get():
                # проверка закрытия окна
                if (event.type == pygame.QUIT):
                    self.run = False
                    self.result = False
                    self.men = False
                    self.play()

                # обработка нажатий на клавиатуре
                if (event.type == pygame.KEYUP):
                    if (event.key == pygame.K_d):
                        right = False
                    if (event.key == pygame.K_a):
                        left = False
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_d):
                        right = True
                        self.button.play()
                    if (event.key == pygame.K_a):
                        left = True
                        self.button.play()

            # обработка нажатий кнопок клавиатуры
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and self.x > 270:
                self.x -= 0.25
                if left == True:
                    self.screen.blit(self.foreground_left.image, (0, 0))
            if keys[pygame.K_d] and self.x < 440:
                self.x += 0.25
                if right == True:
                    self.screen.blit(self.foreground_rigt.image, (654, 0))

            # обработка нажатий кнопок в игре
            if (pygame.mouse.get_pos()[0] > 650 and
                    pygame.mouse.get_pos()[1] > 350):
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    if self.x < 440:
                        self.x += 0.25
                        self.screen.blit(self.foreground_rigt.image, (654, 0))
            if (pygame.mouse.get_pos()[0] < 150 and
                    pygame.mouse.get_pos()[1] > 350):
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    if self.x > 270:
                        self.x -= 0.25
                        self.screen.blit(self.foreground_left.image, (0, 0))
            if (pygame.mouse.get_pos()[0] < 150 and
                    pygame.mouse.get_pos()[1] < 350):
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    self.e_speed *= 1.001

            # спавн препятствий и подсчёт очков
            self.e_y += self.e_speed
            self.e_x -= self.e_speed * self.mn
            if self.e_y >= 360:
                self.e_y = 120
                self.e_x = 550
                self.mn = float(random.choice([0.47, 0.9, 1.4]))
                self.score += 1
                self.game_music.play()
            if self.dt2 > 2:
                self.e_y2 += self.e_speed
                self.e_x2 -= self.e_speed * self.mn2
                if self.e_y2 >= 360:
                    self.e_y2 = 120
                    self.e_x2 = 550
                    self.mn2 = float(random.choice([0.47, 0.9, 1.4]))
                    self.score += 1
                    self.game_music.play()

            # проверка столкновения
            if self.collision():
                self.run = False
                self.result = True
                self.men = False
                self.x = 360
                self.y = 310
                self.die.play()
                self.play()

            # отрисовка
            score_text = pygame.font.Font("Data/Fonts/digital-7.ttf", 74).render(str(self.score), True, (0, 0, 0))
            self.screen.blit(score_text, (290, 130))
            self.add_enemy(self.e_x, self.e_y)
            self.add_enemy2(self.e_x2, self.e_y2)
            self.screen.blit(self.player_sprite.image, (self.x, self.y))

            pygame.display.update()

    def res(self):
        # результаты
        self.start = mixer.Sound("Data/Sounds/start.wav")
        self.ex = mixer.Sound("Data/Sounds/exit.wav")
        if self.score > int(self.max_score):
            self.max_score = self.score
            f2 = open('Data/Max_Score/max_score.txt', 'w')
            f2.write(str(self.max_score))

        # основной цикл окна результатов
        while self.result:
            self.dt = time.time() - self.start_time
            if self.dt > 10:
                self.start_time = time.time()

            # обьявление кнопок
            play_text = pygame.font.Font("Data/Fonts/digital-7.ttf", 74).render(f"PLAY AGAIN", True,
                                                                                (0, 0, 0))
            score_text = pygame.font.Font("Data/Fonts/digital-7.ttf", 24).render(f"score: {self.score}", True,
                                                                                 (0, 0, 0))
            max_score_text = pygame.font.Font("Data/Fonts/digital-7.ttf", 24).render(f"max_score: {self.max_score}",
                                                                                     True,
                                                                                     (0, 0, 0))
            exit_text = pygame.font.Font("Data/Fonts/digital-7.ttf", 24).render("EXIT", True, (0, 0, 0))

            # отрисовка кнопок
            self.screen.blit(self.foreground_back.image, self.foreground_back.rect)
            self.screen.blit(score_text, (260, 300))
            self.screen.blit(max_score_text, (260, 325))
            self.screen.blit(exit_text, (470, 310))

            # анимация кнопок
            if self.dt <= 1:
                self.screen.blit(play_text, (260, 230))
            if self.dt >= 1 and self.dt <= 2:
                self.screen.blit(play_text, (260, 235))
            if self.dt >= 2 and self.dt <= 3:
                self.screen.blit(play_text, (260, 230))
            if self.dt >= 3 and self.dt <= 4:
                self.screen.blit(play_text, (260, 235))
            if self.dt >= 4 and self.dt <= 5:
                self.screen.blit(play_text, (260, 230))
            if self.dt >= 5 and self.dt <= 6:
                self.screen.blit(play_text, (260, 235))
            if self.dt >= 6 and self.dt <= 7:
                self.screen.blit(play_text, (260, 230))
            if self.dt >= 7 and self.dt <= 8:
                self.screen.blit(play_text, (260, 235))
            if self.dt >= 8 and self.dt <= 9:
                self.screen.blit(play_text, (260, 230))
            if self.dt >= 9 and self.dt <= 10:
                self.screen.blit(play_text, (260, 235))
            if self.dt >= 10:
                self.screen.blit(play_text, (260, 230))

            # обработка нажатий кнопок
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    self.run = False
                    self.men = False
                    self.result = False
                    self.play()
                if (pygame.mouse.get_pos()[0] > 650 and
                        pygame.mouse.get_pos()[1] < 350):
                    if (event.type == pygame.MOUSEBUTTONDOWN):
                        self.run = True
                        self.men = False
                        self.result = False
                        self.start.play()
                        self.play()
                if (pygame.mouse.get_pos()[0] > 650 and
                        pygame.mouse.get_pos()[1] < 75 and pygame.mouse.get_pos()[1] > 50):
                    if (event.type == pygame.MOUSEBUTTONDOWN):
                        self.game_dif = 0
                        self.run = True
                        self.men = False
                        self.result = False
                        self.start.play()
                        self.play()
                if (pygame.mouse.get_pos()[0] > 650 and
                        pygame.mouse.get_pos()[1] < 150 and pygame.mouse.get_pos()[1] > 75):
                    if (event.type == pygame.MOUSEBUTTONDOWN):
                        self.game_dif = 1
                        self.run = True
                        self.men = False
                        self.result = False
                        self.start.play()
                        self.play()
                if (pygame.mouse.get_pos()[0] < self.width / 2 + play_text.get_width() / 2 and
                        pygame.mouse.get_pos()[
                            0] > self.width / 2 - play_text.get_width() / 2):
                    if (pygame.mouse.get_pos()[1] < 280 and
                            pygame.mouse.get_pos()[1] > 250):
                        if (event.type == pygame.MOUSEBUTTONDOWN):
                            self.run = True
                            self.men = False
                            self.result = False
                            self.start.play()
                            self.play()
                    if (pygame.mouse.get_pos()[1] < 320 and
                            pygame.mouse.get_pos()[1] > 300):
                        if (event.type == pygame.MOUSEBUTTONDOWN):
                            self.ex.play()
                            time.sleep(0.5)
                            self.men = False
                            self.result = False
                            self.run = False
                            self.play()

            pygame.display.update()

    def play(self):
        # проверка статуса
        if self.men == True:
            self.menu()
        if self.result == True:
            self.res()
        if self.run == True:
            self.game()
        else:
            exit(0)


game = Main()
