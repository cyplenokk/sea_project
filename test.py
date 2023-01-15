from typing import Tuple

import pygame, sys, os
import pickle
from pygame.font import Font

FPS = 50
pygame.font.init()

size = width, height = 800, 500
screen = pygame.display.set_mode(size)
screen2 = pygame.display.set_mode(size)

clock = pygame.time.Clock()

start = 0
objects = []

pixel = pygame.font.Font('progresspixel_bold.ttf', 30)

all_sprites = pygame.sprite.Group()

play = False


def terminate():
    pygame.quit()
    sys.exit()


objects = []


class AnimatedSprite(pygame.sprite.Sprite):  # класс для анимаций
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Button():  # класс для кнопок
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False, alreadyPressed=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = pixel.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

        objects.append(self)

    def process(self):



        mousePos = pygame.mouse.get_pos()

        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            print(self.alreadyPressed)
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                self.alreadyPressed = False


                if not self.alreadyPressed:
                    print('yay')
                    self.alreadyPressed = True
                    self.onclickFunction()

            else:
                self.alreadyPressed = True

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)



def start_screen():
    screen.fill((0, 0, 0))

    global new_near_cells, filled_cells, near_cells, ship_map1, filled_cells2, near_cells2, new_near_cells2, ship_map2, \
        wrecked_cells, battle, filled_cells_pl1, near_cells_pl1, new_near_cells_pl1, ships_of_player1, ships_of_player2, \
        all_ships2, list_of_ship2, list_of_ship3, list_of_ship4

    ship_map1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 ]



    filled_cells2 = []  # список заполняемых клеток для второго поля  (корабли)

    # промежуточный список для создания конечного new_near_cells
    near_cells2 = []  # # промежуточный список для создания конечного new_near_cells2

    # список заполняемых клеток для первого поля (клетки вокруг кораблей, которые нельзя заполнять)
    new_near_cells2 = []  # # список заполняемых клеток для второго поля (клетки вокруг кораблей, которые нельзя заполнять)

    # карта с кораблями первого игрока
    ship_map2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 ]  # карта с кораблями второго игрока

    wrecked_cells = []

    battle = False

    filled_cells_pl1 = []
    near_cells_pl1 = []
    new_near_cells_pl1 = []

    ships_of_player1 = {
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0
    }

    ships_of_player2 = {
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0
    }
    all_ships2 = []

    list_of_ship2 = []
    list_of_ship3 = []
    list_of_ship4 = []

    # функция для запуска стартового окна
    running = True
    x_pos1 = 800
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for object1 in objects:
            object1.process()

        surf1 = pygame.Surface((130, 130))
        surf1.fill(('black'))
        screen.blit(surf1, (x_pos1, 70))
        customButton = Button(200, 200, 400, 100, 'start', start_game_player1)
        f2 = pygame.font.Font('progresspixel_bold.ttf', 70)
        textt = f2.render('sea battle', True, (115, 2, 2))
        textt_shadow = f2.render('sea battle', True, (205, 29, 29))
        screen.blit(textt_shadow, (205, 20))
        screen.blit(textt, (200, 20))

        ship1 = load_image('ship_one.jpg')
        ship1 = pygame.transform.scale(ship1, (130, 130))
        screen.blit(ship1, (x_pos1, 70))

        pygame.display.flip()

        clock.tick(FPS)

        x_pos1 -= 4
        if x_pos1 <= -200:
            x_pos1 = 800




def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image.set_colorkey(('white'))
    return image





def start_game_player1():
    global filled_cells, near_cells, new_near_cells

    filled_cells = []
    near_cells = []
    new_near_cells = []

    game = True

    clock = pygame.time.Clock()
    # добавление анимации на поле
    wave_1 = load_image("waves2.jpg")
    moving_x = 27
    moving_y = 27
    wave_inp = pygame.transform.scale(wave_1, (230, 130))
    counter = 0
    for i in range(11):
        for j in range(10):
            if counter == 10:
                moving_x = 27
                moving_y += 27
                counter = 0
            else:
                waves = AnimatedSprite(wave_inp, 9, 6, 77 + moving_x, 102 + moving_y)
                moving_x += 27
                counter += 1
    # wave1 = pygame.transform.scale(wave_1, (500, 400))
    # wave2 = pygame.transform.scale(wave_2, (600, 500))
    # wave3 = pygame.transform.scale(wave_1, (250, 150))
    # wave4 = pygame.transform.scale(wave_2, (300, 200))
    # wave5 = pygame.transform.scale(wave_1, (400, 300))
    # waves1 = AnimatedSprite(wave1, 9, 6, 322, 330)
    # waves2 = AnimatedSprite(wave2, 9, 6, 103, 288)
    # waves3 = AnimatedSprite(wave3, 9, 6, 105, 127)
    # waves33 = AnimatedSprite(wave3, 9, 6, 105, 127)
    # waves4 = AnimatedSprite(wave4, 9, 6, 265, 280)
    # waves5 = AnimatedSprite(wave5, 9, 6, 315, 157)
    # waves6 = AnimatedSprite(wave5, 9, 6, 150, 182)

    drawing = False

    screen.fill((0, 0, 0))

    cells4 = 1
    cells3 = 2
    cells2 = 3
    cells1 = 4

    while game:
        if not drawing:
            surf = pygame.Surface((297, 297))
            surf.fill(('#008B8B'))
            screen.blit(surf, (80, 100))
            surf1 = pygame.Surface((297, 297))
            surf1.fill(('#480607'))
            screen.blit(surf1, (410, 100))

            cells_coll = []

        board = Board(11, 11)
        board1 = Board(11, 11)
        board1.set_view(410, 100, 27)
        board.set_view(80, 100, 27)

        draw_ship(filled_cells, near_cells, new_near_cells)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0] or event.type == pygame.MOUSEBUTTONDOWN:
                if board.get_click(event.pos) is not None:
                    x, y = board.get_click(event.pos)
                    cells_coll.append([x, y])
                    print(x, y)
                    board.fill_cell(x, y, '#0A5257')
                    boat = load_image('ship_one.jpg')
                    boat = pygame.transform.scale(boat, (27, 27))
                    screen.blit(boat, (77 + x * 27, 102 + y * 27))


                    # self.IMAGE = pygame.Surface((self.width * self.tile_size, self.height * self.tile_size))
                    # self.IMAGE.blit(self.Image_background, (0, 0))
                    # self.IMAGE.blit(self.Image_foreground, (0, 0))

                    drawing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                spisok = []
                for i in cells_coll:
                    if i not in spisok:
                        spisok.append(i)
                spisok = sorted(spisok)

                # проверка: подходят ли выделенные клетки
                if len(spisok) == 4 and cells4 > 0:
                    if (spisok[0][0] == spisok[1][0] == spisok[2][0] == spisok[3][0] and spisok[0][1] ==
                        spisok[1][1] - 1 == spisok[2][1] - 2 == spisok[3][1] - 3) or (spisok[0][0] ==
                                                                                      spisok[1][0] - 1 == spisok[2][
                                                                                          0] - 2 == spisok[3][0] - 3 and
                                                                                      spisok[0][1] ==
                                                                                      spisok[1][1] == spisok[2][1] ==
                                                                                      spisok[3][1]):
                        if spisok[0] not in new_near_cells and spisok[1] not in new_near_cells and spisok[2] \
                                not in new_near_cells and spisok[3] not in new_near_cells:
                            for i in spisok:
                                ship_map1[i[1] - 1][i[0] - 1] = 1
                            filled_cells.append(spisok)
                            print(filled_cells)
                            cells4 -= 1

                if len(spisok) == 3 and cells3 > 0:
                    if (spisok[0][0] == spisok[1][0] == spisok[2][0] and spisok[0][1] ==
                        spisok[1][1] - 1 == spisok[2][1] - 2) or (spisok[0][0] ==
                                                                  spisok[1][0] - 1 == spisok[2][0] - 2 and spisok[0][
                                                                      1] ==
                                                                  spisok[1][1] == spisok[2][1]):
                        if spisok[0] not in new_near_cells and spisok[1] not in new_near_cells and spisok[2] \
                                not in new_near_cells:
                            for i in spisok:
                                ship_map1[i[1] - 1][i[0] - 1] = 1
                            filled_cells.append(spisok)
                            print(filled_cells)
                            cells3 -= 1

                if len(spisok) == 2 and cells2 > 0:
                    if (spisok[0][0] == spisok[1][0] and spisok[0][1] ==
                        spisok[1][1] - 1) or (spisok[0][0] ==
                                              spisok[1][0] - 1 and spisok[0][1] ==
                                              spisok[1][1]):
                        if spisok[0] not in new_near_cells and spisok[1] not in new_near_cells:
                            for i in spisok:
                                ship_map1[i[1] - 1][i[0] - 1] = 1
                            filled_cells.append(spisok)
                            print(filled_cells)
                            cells2 -= 1

                if len(spisok) == 1 and cells1 > 0:
                    if spisok[0] not in new_near_cells:
                        for i in spisok:
                            ship_map1[i[1] - 1][i[0] - 1] = 1
                        filled_cells.append(spisok)
                        print(filled_cells)
                        cells1 -= 1

                drawing = False

            # если все корабли выставлены, теперь корабли выбирает второй игрок
            if cells1 == 0 and cells2 == 0 and cells3 == 0 and cells4 == 0:
                new_near_cells = []
                for el in all_sprites:
                    el.kill()
                start_game_player2()

        all_sprites.draw(screen)
        all_sprites.update()

        f1 = pygame.font.Font('progresspixel_bold.ttf', 15)
        number = 0
        for i in range(115, 350, 27):
            number += 1
            text1 = f1.render(str(number), True, ('white'))
            screen.blit(text1, (i, 100))
            screen.blit(text1, (i + 330, 100))

        text1 = f1.render('10', True, ('white'))
        screen.blit(text1, (354, 100))
        screen.blit(text1, (365 + 318, 100))

        number = 0
        spisok = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'к']
        for i in range(130, 400, 27):
            text1 = f1.render(spisok[number], True, ('white'))
            screen.blit(text1, (90, i))
            screen.blit(text1, (90 + 330, i))

            number += 1

        all_sprites.draw(screen)
        all_sprites.update()

        clock.tick(6)
        pygame.display.flip()

        font2 = pygame.font.Font('progresspixel_bold.ttf', 24)
        font3 = pygame.font.Font('progresspixel_bold.ttf', 19)
        text2 = font3.render('player 1:', True, ('#008B8B'))
        screen.blit(text2, (80, 20))

        text1 = font2.render('choose places for ships', True, ('white'))
        screen.blit(text1, (80, 40))

        board.render(screen)
        board1.render(screen)

        blitt = pygame.Surface((130, 130))
        blitt.fill(('black'))
        screen.blit(blitt, (80, 400))

        font3 = pygame.font.Font('progresspixel_bold.ttf', 15)

        if cells4 == 0:
            ship4 = font3.render(f'4 cells ships: {cells4}', True, ('red'))
            screen.blit(ship4, (80, 400))
        else:
            ship4 = font3.render(f'4 cells ships: {cells4}', True, ('green'))
            screen.blit(ship4, (80, 400))

        if cells3 == 0:
            ship4 = font3.render(f'3 cells ships: {cells3}', True, ('red'))
            screen.blit(ship4, (80, 420))
        else:
            ship4 = font3.render(f'3 cells ships: {cells3}', True, ('green'))
            screen.blit(ship4, (80, 420))

        if cells2 == 0:
            ship4 = font3.render(f'2 cells ships: {cells2}', True, ('red'))
            screen.blit(ship4, (80, 440))
        else:
            ship4 = font3.render(f'2 cells ships: {cells2}', True, ('green'))
            screen.blit(ship4, (80, 440))

        if cells1 == 0:
            ship4 = font3.render(f'1 cell ships: {cells1}', True, ('red'))
            screen.blit(ship4, (80, 460))
        else:
            ship4 = font3.render(f'1 cell ships: {cells1}', True, ('green'))
            screen.blit(ship4, (80, 460))

        pygame.display.update()


# то же самое для второго игрока
def start_game_player2():
    global new_near_cells2, filled_cells2, near_cells2

    filled_cells2 = []  # список заполняемых клеток для второго поля  (корабли)

    # промежуточный список для создания конечного new_near_cells
    near_cells2 = []  # # промежуточный список для создания конечного new_near_cells2

    # список заполняемых клеток для первого поля (клетки вокруг кораблей, которые нельзя заполнять)
    new_near_cells2 = []  # # спи

    game = True

    clock = pygame.time.Clock()
    wave_2 = load_image("waves2.jpg")
    moving_x = 27
    moving_y = 27
    wave_inp = pygame.transform.scale(wave_2, (230, 130))
    counter = 0
    lst_waves = []
    for i in range(11):
        for j in range(10):
            if counter == 10:
                moving_x = 27
                moving_y += 27
                counter = 0
            else:
                lst_waves.append(AnimatedSprite(wave_inp, 9, 6, 407 + moving_x, 102 + moving_y))
                moving_x += 27
                counter += 1
    # wave_1 = load_image("waves2.jpg")
    # wave_2 = load_image("reversed.jpg")
    # wave1 = pygame.transform.scale(wave_1, (500, 400))
    # wave2 = pygame.transform.scale(wave_2, (600, 500))
    # wave3 = pygame.transform.scale(wave_1, (300, 200))
    # wave4 = pygame.transform.scale(wave_2, (300, 200))
    # wave5 = pygame.transform.scale(wave_1, (400, 300))
    # waves1 = AnimatedSprite(wave1, 9, 6, 605, 220)
    # waves2 = AnimatedSprite(wave2, 9, 6, 430, 178)
    # waves3 = AnimatedSprite(wave3, 9, 6, 511, 120)
    # waves4 = AnimatedSprite(wave4, 9, 6, 670, 145)
    # waves5 = AnimatedSprite(wave5, 9, 6, 570, 345)
    # waves6 = AnimatedSprite(wave5, 9, 6, 490, 296)

    drawing = False

    screen.fill((0, 0, 0))

    cells4 = 1
    cells3 = 2
    cells2 = 3
    cells1 = 4

    while game:
        if not drawing:
            surf = pygame.Surface((297, 297))
            surf.fill(('#008B8B'))
            screen.blit(surf, (80, 100))
            surf1 = pygame.Surface((297, 297))
            surf1.fill(('#480607'))
            screen.blit(surf1, (410, 100))

            cells_coll = []

        board = Board(11, 11)
        board1 = Board(11, 11)
        board1.set_view(410, 100, 27)
        board.set_view(80, 100, 27)

        draw_ship(filled_cells2, near_cells2, new_near_cells2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0] or event.type == pygame.MOUSEBUTTONDOWN:
                if board1.get_click(event.pos) is not None:
                    x, y = board1.get_click(event.pos)
                    cells_coll.append([x, y])
                    print(x, y)
                    board1.fill_cell(x, y, '#2F0404')
                    boat = load_image('ship_one.jpg')
                    boat = pygame.transform.scale(boat, (27, 27))
                    screen.blit(boat, (403 + x * 27, 102 + y * 27))

                    drawing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                spisok = []
                for i in cells_coll:
                    if i not in spisok:
                        spisok.append(i)
                spisok = sorted(spisok)

                if len(spisok) == 4 and cells4 > 0:
                    if (spisok[0][0] == spisok[1][0] == spisok[2][0] == spisok[3][0] and spisok[0][1] ==
                        spisok[1][1] - 1 == spisok[2][1] - 2 == spisok[3][1] - 3) or (spisok[0][0] ==
                                                                                      spisok[1][0] - 1 == spisok[2][
                                                                                          0] - 2 == spisok[3][
                                                                                          0] - 3 and spisok[0][1] ==
                                                                                      spisok[1][1] == spisok[2][
                                                                                          1] == spisok[3][1]):
                        if spisok[0] not in new_near_cells2 and spisok[1] not in new_near_cells2 and spisok[2] \
                                not in new_near_cells2 and spisok[3] not in new_near_cells2:
                            for i in spisok:
                                ship_map2[i[1] - 1][i[0] - 1] = 1
                            filled_cells2.append(spisok)
                            print(filled_cells2)
                            cells4 -= 1

                if len(spisok) == 3 and cells3 > 0:
                    if (spisok[0][0] == spisok[1][0] == spisok[2][0] and spisok[0][1] ==
                        spisok[1][1] - 1 == spisok[2][1] - 2) or (spisok[0][0] ==
                                                                  spisok[1][0] - 1 == spisok[2][0] - 2 and
                                                                  spisok[0][1] ==
                                                                  spisok[1][1] == spisok[2][1]):
                        if spisok[0] not in new_near_cells2 and spisok[1] not in new_near_cells2 and spisok[2] \
                                not in new_near_cells2:
                            for i in spisok:
                                ship_map2[i[1] - 1][i[0] - 1] = 1
                            filled_cells2.append(spisok)
                            print(filled_cells2)
                            cells3 -= 1

                if len(spisok) == 2 and cells2 > 0:
                    if (spisok[0][0] == spisok[1][0] and spisok[0][1] ==
                        spisok[1][1] - 1) or (spisok[0][0] ==
                                              spisok[1][0] - 1 and spisok[0][1] ==
                                              spisok[1][1]):
                        if spisok[0] not in new_near_cells2 and spisok[1] not in new_near_cells2:
                            for i in spisok:
                                ship_map2[i[1] - 1][i[0] - 1] = 1
                            filled_cells2.append(spisok)
                            print(filled_cells2)
                            cells2 -= 1

                if len(spisok) == 1 and cells1 > 0:
                    if spisok[0] not in new_near_cells2:
                        for i in spisok:
                            ship_map2[i[1] - 1][i[0] - 1] = 1
                        filled_cells2.append(spisok)
                        print(filled_cells2)
                        cells1 -= 1

                drawing = False

            if cells1 == 0 and cells2 == 0 and cells3 == 0 and cells4 == 0:
                new_near_cells = []
                for el in all_sprites:
                    el.kill()
                print('over')
                print(ship_map1)
                print(ship_map2)
                play_game_1()  # здесь должен быть переход в режим игры

        all_sprites.draw(screen)
        all_sprites.update()

        f1 = pygame.font.Font('progresspixel_bold.ttf', 15)
        number = 0
        for i in range(115, 350, 27):
            number += 1
            text1 = f1.render(str(number), True, ('white'))
            screen.blit(text1, (i, 100))
            screen.blit(text1, (i + 330, 100))

        text1 = f1.render('10', True, ('white'))
        screen.blit(text1, (354, 100))
        screen.blit(text1, (365 + 318, 100))

        number = 0
        spisok = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'к']
        for i in range(130, 400, 27):
            text1 = f1.render(spisok[number], True, ('white'))
            screen.blit(text1, (90, i))
            screen.blit(text1, (90 + 330, i))

            number += 1

        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(6)
        pygame.display.flip()

        font2 = pygame.font.Font('progresspixel_bold.ttf', 24)
        font3 = pygame.font.Font('progresspixel_bold.ttf', 19)
        text2 = font3.render('player 2:', True, ('#480607'))
        screen.blit(text2, (620, 20))

        text1 = font2.render('choose places for ships', True, ('white'))
        screen.blit(text1, (380, 40))

        board.render(screen)
        board1.render(screen)

        blitt = pygame.Surface((130, 130))
        blitt.fill(('black'))
        screen.blit(blitt, (580, 400))

        font3 = pygame.font.Font('progresspixel_bold.ttf', 15)

        if cells4 == 0:
            ship4 = font3.render(f'4 cells ships: {cells4}', True, ('red'))
            screen.blit(ship4, (580, 400))
        else:
            ship4 = font3.render(f'4 cells ships: {cells4}', True, ('green'))
            screen.blit(ship4, (580, 400))

        if cells3 == 0:
            ship4 = font3.render(f'3 cells ships: {cells3}', True, ('red'))
            screen.blit(ship4, (580, 420))
        else:
            ship4 = font3.render(f'3 cells ships: {cells3}', True, ('green'))
            screen.blit(ship4, (580, 420))

        if cells2 == 0:
            ship4 = font3.render(f'2 cells ships: {cells2}', True, ('red'))
            screen.blit(ship4, (580, 440))
        else:
            ship4 = font3.render(f'2 cells ships: {cells2}', True, ('green'))
            screen.blit(ship4, (580, 440))

        if cells1 == 0:
            ship4 = font3.render(f'1 cell ships: {cells1}', True, ('red'))
            screen.blit(ship4, (580, 460))
        else:
            ship4 = font3.render(f'1 cell ships: {cells1}', True, ('green'))
            screen.blit(ship4, (580, 460))

        pygame.display.update()



def play_game_1():
    player1 = True

    global ships_of_player1



    first_time = True
    if first_time:

        near_cells_pl1 = []
        new_near_cells_pl1 = []
        first_time = False

    new_near_cells = [1]

    global battle

    play = True

    game = True
    clock = pygame.time.Clock()

    for el in filled_cells2:
        for elem in el:
            all_ships2.append(elem)

    # добавление анимации на поле
    wave = load_image("waves2.jpg")
    wave_inp = pygame.transform.scale(wave, (230, 130))
    # wave_2 = load_image("reversed.jpg")
    # wave1 = pygame.transform.scale(wave_1, (500, 400))
    # wave2 = pygame.transform.scale(wave_2, (600, 500))
    # wave3 = pygame.transform.scale(wave_1, (300, 200))
    # wave4 = pygame.transform.scale(wave_2, (300, 200))
    # wave5 = pygame.transform.scale(wave_1, (400, 300))
    # waves1 = AnimatedSprite(wave1, 9, 6, 322, 330)
    # waves2 = AnimatedSprite(wave2, 9, 6, 103, 288)
    # waves3 = AnimatedSprite(wave3, 9, 6, 103, 120)
    # waves4 = AnimatedSprite(wave4, 9, 6, 265, 280)
    # waves5 = AnimatedSprite(wave5, 9, 6, 315, 157)
    # waves6 = AnimatedSprite(wave5, 9, 6, 150, 182)

    drawing = False

    screen.fill((0, 0, 0))

    cells4 = 1
    cells3 = 2
    cells2 = 3
    cells1 = 4

    while game:
        if not drawing:
            surf = pygame.Surface((297, 297))
            surf.fill(('#480607'))
            screen.blit(surf, (80, 100))
            surf1 = pygame.Surface((297, 297))
            surf1.fill(('#008B8B'))
            screen.blit(surf1, (410, 100))

            cells_coll = []

        board = Board(11, 11)
        board1 = Board(11, 11)
        board1.set_view(410, 100, 27)
        board.set_view(80, 100, 27)

        draw_ship(filled_cells_pl1, near_cells_pl1, new_near_cells_pl1, play=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if board.get_click(event.pos) is not None:
                    x, y = board.get_click(event.pos)
                    cells_coll.append([x, y])
                    print(x, y)
                    board.fill_cell(x, y, '#0A5257')

                    drawing = True
                    fire = load_image("fire.png")
                    fire1 = pygame.transform.scale(fire, (250, 150))

                    # print(cells_coll)
                    # print(ship_map2[cells_coll[0][0] - 1][cells_coll[0][1] - 1])
                    # print(ship_map2)
                    if ship_map2[cells_coll[0][1] - 1][cells_coll[0][0] - 1] == 1 and cells_coll not in filled_cells_pl1:
                        print('прошел')
                        fires = AnimatedSprite(fire1, 5, 4, 27 * x + 68, 27 * y + 90)
                        filled_cells_pl1.append(cells_coll)
                        battle = True
                        # print(all_ships2)

                        # проверка кораблей
                        # однопалубный
                        if [x + 1, y] not in all_ships2 and [x, y + 1] not in all_ships2 \
                                and [x - 1, y] not in all_ships2 and [x, y - 1] not in all_ships2:
                            print('убит корабль из 1')
                            ships_of_player1['1'] += 1

                            if ships_of_player1['1'] == 4 and ships_of_player1['2'] == 3 and ships_of_player1['3'] == 2 \
                                and ships_of_player1['4'] == 1:
                                print('game over')
                                finish()


                        # трехпалубный

                        elif [x + 1, y] in all_ships2 and [x + 2, y] in all_ships2 \
                                and [x + 3, y] not in all_ships2 and [x - 1, y] not in all_ships2:
                            if [x + 1, y] in list_of_ship3 and [x + 2, y] in list_of_ship3:
                                print('убит корабль из 3')
                                ships_of_player1['3'] += 1
                                if ships_of_player1['1'] == 4 and ships_of_player1['2'] == 3 and ships_of_player1[
                                    '3'] == 2 \
                                        and ships_of_player1['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 3 поражен')
                                list_of_ship3.append([x, y])
                        elif [x, y + 1] in all_ships2 and [x, y + 2] in all_ships2 \
                                and [x, y + 3] not in all_ships2 and [x, y - 1] not in all_ships2:
                            if [x, y + 1] in list_of_ship3 and [x, y + 2] in list_of_ship3:
                                print('убит корабль из 3')
                                ships_of_player1['3'] += 1
                                if ships_of_player1['1'] == 4 and ships_of_player1['2'] == 3 and ships_of_player1[
                                    '3'] == 2 \
                                        and ships_of_player1['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 3 поражен')
                                list_of_ship3.append([x, y])
                        elif [x - 1, y] in all_ships2 and [x - 2, y] in all_ships2 \
                                and [x - 3, y] not in all_ships2 and [x + 1, y] not in all_ships2:
                            if [x - 1, y] in list_of_ship3 and [x - 2, y] in list_of_ship3:
                                print('убит корабль из 3')
                                ships_of_player1['3'] += 1
                                if ships_of_player1['1'] == 4 and ships_of_player1['2'] == 3 and ships_of_player1[
                                    '3'] == 2 \
                                        and ships_of_player1['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 3 поражен')
                                list_of_ship3.append([x, y])
                        elif [x, y - 1] in all_ships2 and [x, y - 2] in all_ships2 \
                                and [x, y - 3] not in all_ships2 and [x, y + 1] not in all_ships2:
                            if [x, y - 1] in list_of_ship3 and [x, y - 2] in list_of_ship3:
                                print('убит корабль из 3')
                                ships_of_player1['3'] += 1
                                if ships_of_player1['1'] == 4 and ships_of_player1['2'] == 3 and ships_of_player1[
                                    '3'] == 2 \
                                        and ships_of_player1['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 3 поражен')
                                list_of_ship3.append([x, y])
                        elif [x + 1, y] in all_ships2 and [x - 1, y] in all_ships2 \
                                and [x + 2, y] not in all_ships2 and [x - 2, y] not in all_ships2:
                            if [x + 1, y] in list_of_ship3 and [x - 1, y] in list_of_ship3:
                                print('убит корабль из 3')
                                ships_of_player1['3'] += 1
                                if ships_of_player1['1'] == 4 and ships_of_player1['2'] == 3 and ships_of_player1[
                                    '3'] == 2 \
                                        and ships_of_player1['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 3 поражен')
                                list_of_ship3.append([x, y])
                        elif [x, y + 1] in all_ships2 and [x, y - 1] in all_ships2 \
                                and [x, y + 2] not in all_ships2 and [x, y - 2] not in all_ships2:
                            if [x, y + 1] in list_of_ship3 and [x, y - 1] in list_of_ship3:
                                print('убит корабль из 3')
                                ships_of_player1['3'] += 1
                                if ships_of_player1['1'] == 4 and ships_of_player1['2'] == 3 and ships_of_player1[
                                    '3'] == 2 \
                                        and ships_of_player1['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 3 поражен')
                                list_of_ship3.append([x, y])

                        # двухпалубный

                        elif [x + 1, y] in all_ships2 and [x - 1, y] not in all_ships2 and [x + 2, y] not in all_ships2:
                            if [x + 1, y] in list_of_ship2:
                                print('убит корабль из 2')
                                ships_of_player1['2'] += 1
                                if ships_of_player1['1'] == 4 and ships_of_player1['2'] == 3 and ships_of_player1[
                                    '3'] == 2 \
                                        and ships_of_player1['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 2 поражен')
                                list_of_ship2.append([x, y])
                        elif [x, y + 1] in all_ships2 and [x, y - 1] not in all_ships2 and [x, y + 2] not in all_ships2:
                            if [x, y + 1] in list_of_ship2:
                                print('убит корабль из 2')
                                ships_of_player1['2'] += 1
                                if ships_of_player1['1'] == 4 and ships_of_player1['2'] == 3 and ships_of_player1[
                                    '3'] == 2 \
                                        and ships_of_player1['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 2 поражен')
                                list_of_ship2.append([x, y])
                        elif [x - 1, y] in all_ships2 and [x + 1, y] not in all_ships2 and [x - 2, y] not in all_ships2:
                            if [x - 1, y] in list_of_ship2:
                                print('убит корабль из 2')
                                ships_of_player1['2'] += 1
                                if ships_of_player1['1'] == 4 and ships_of_player1['2'] == 3 and ships_of_player1[
                                    '3'] == 2 \
                                        and ships_of_player1['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 2 поражен')
                                list_of_ship2.append([x, y])
                        elif [x, y - 1] in all_ships2 and [x, y + 1] not in all_ships2 and [x, y - 2] not in all_ships2:
                            if [x, y - 1] in list_of_ship2:
                                print('убит корабль из 2')
                                ships_of_player1['2'] += 1
                                if ships_of_player1['1'] == 4 and ships_of_player1['2'] == 3 and ships_of_player1[
                                    '3'] == 2 \
                                        and ships_of_player1['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 2 поражен')
                                list_of_ship2.append([x, y])

                        # четырехпалубный

                        else:
                            if len(list_of_ship4) == 3:
                                print('убит корабль из 4')
                                ships_of_player1['4'] += 1
                                if ships_of_player1['1'] == 4 and ships_of_player1['2'] == 3 and ships_of_player1[
                                    '3'] == 2 \
                                        and ships_of_player1['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 4 поражен')
                                list_of_ship4.append([x, y])
                        print(ships_of_player1)

                        # !!!!!!!!!!!!!
                        # здесь происходит запись пораженных кораблей в txt файл
                        # пока что каждый раз заново создается файл, но нужно будет сделать,
                        # чтобы только в конце он 1 раз создался

                        # with open('Ships_of_player1.txt', 'w+') as f:
                        #     pickle.dump(ships_of_player1, f)
                        play_game_1()
                    if ship_map2[cells_coll[0][1] - 1][cells_coll[0][0] - 1] != 1:
                        new_near_cells_pl1.append(cells_coll)
                        print('не прошел')
                        wave_put = AnimatedSprite(wave_inp, 9, 6, 27 * x + 78, 27 * y + 100)
                        play_game_2()

                    # проверка: подходят ли выделенные клетки

                    drawing = False

            # если все корабли выставлены, теперь корабли выбирает второй игрок

        all_sprites.draw(screen)
        all_sprites.update()

        f1 = pygame.font.Font('progresspixel_bold.ttf', 15)
        number = 0
        for i in range(115, 350, 27):
            number += 1
            text1 = f1.render(str(number), True, ('white'))
            screen.blit(text1, (i, 100))
            screen.blit(text1, (i + 330, 100))

        text1 = f1.render('10', True, ('white'))
        screen.blit(text1, (354, 100))
        screen.blit(text1, (365 + 318, 100))

        number = 0
        spisok = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'к']
        for i in range(130, 400, 27):
            text1 = f1.render(spisok[number], True, ('white'))
            screen.blit(text1, (90, i))
            screen.blit(text1, (90 + 330, i))

            number += 1

        all_sprites.draw(screen)
        all_sprites.update()

        clock.tick(6)
        pygame.display.flip()

        font2 = pygame.font.Font('progresspixel_bold.ttf', 24)
        font3 = pygame.font.Font('progresspixel_bold.ttf', 19)
        text2 = font3.render('player 1:', True, ('#008B8B'))
        screen.blit(text2, (80, 20))

        text1 = font2.render('your turn', True, ('white'))
        screen.blit(text1, (80, 40))

        board.render(screen)
        board1.render(screen)

        blitt = pygame.Surface((130, 130))
        blitt.fill(('black'))
        screen.blit(blitt, (80, 400))

        pygame.display.update()




def play_game_2():
    player1 = True

    global ships_of_player2, filled_cells4

    all_ships1 = []

    list2_of_ship2 = []
    list2_of_ship3 = []
    list2_of_ship4 = []

    filled_cells4 = []
    near_cells4 = []
    new_near_cells4 = []

    new_near_cells = [1]

    global battle

    play = True

    game = True

    for el in filled_cells:
        for elem in el:
            all_ships1.append(elem)

    clock = pygame.time.Clock()
    wave = load_image("waves2.jpg")
    wave_inp = pygame.transform.scale(wave, (230, 130))
    # wave_1 = load_image("waves2.jpg")
    # wave_2 = load_image("reversed.jpg")
    # wave1 = pygame.transform.scale(wave_1, (500, 400))
    # wave2 = pygame.transform.scale(wave_2, (600, 500))
    # wave3 = pygame.transform.scale(wave_1, (300, 200))
    # wave4 = pygame.transform.scale(wave_2, (300, 200))
    # wave5 = pygame.transform.scale(wave_1, (400, 300))
    # waves1 = AnimatedSprite(wave1, 9, 6, 605, 220)
    # waves2 = AnimatedSprite(wave2, 9, 6, 430, 178)
    # waves3 = AnimatedSprite(wave3, 9, 6, 511, 120)
    # waves4 = AnimatedSprite(wave4, 9, 6, 670, 145)
    # waves5 = AnimatedSprite(wave5, 9, 6, 570, 345)
    # waves6 = AnimatedSprite(wave5, 9, 6, 490, 296)

    drawing = False

    screen.fill((0, 0, 0))

    cells4 = 1
    cells3 = 2
    cells2 = 3
    cells1 = 4

    while game:
        if not drawing:
            surf = pygame.Surface((297, 297))
            surf.fill(('#480607'))
            screen.blit(surf, (80, 100))
            surf1 = pygame.Surface((297, 297))
            surf1.fill(('#008B8B'))
            screen.blit(surf1, (410, 100))

            cells_coll = []

        board = Board(11, 11)
        board1 = Board(11, 11)
        board1.set_view(410, 100, 27)
        board.set_view(80, 100, 27)

        draw_ship(filled_cells4, near_cells4, new_near_cells4, play=True, number=2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if board1.get_click(event.pos) is not None:
                    x, y = board1.get_click(event.pos)
                    cells_coll.append([x, y])
                    print(x, y)
                    board1.fill_cell(x, y, '#0A5257')

                    drawing = True

                    fire = load_image("fire.png")
                    fire1 = pygame.transform.scale(fire, (250, 150))

                    print(cells_coll)
                    print(cells_coll[0][0])
                    print(cells_coll[0][1])
                    if ship_map1[cells_coll[0][1] - 1][cells_coll[0][0] - 1] == 1 and cells_coll not in filled_cells4:
                        fires = AnimatedSprite(fire1, 5, 4, 27 * x + 400, 27 * y + 90)
                        print('прошел')
                        filled_cells4.append(cells_coll)

                        # проверка кораблей
                        # однопалубный
                        if [x + 1, y] not in all_ships1 and [x, y + 1] not in all_ships1 \
                                and [x - 1, y] not in all_ships1 and [x, y - 1] not in all_ships1:
                            print('убит корабль из 1')
                            ships_of_player2['1'] += 1
                            if ships_of_player2['1'] == 4 and ships_of_player2['2'] == 3 and ships_of_player2['3'] == 2 \
                                and ships_of_player2['4'] == 1:
                                print('game over')
                                finish()


                        # трехпалубный

                        elif [x + 1, y] in all_ships1 and [x + 2, y] in all_ships1 \
                                and [x + 3, y] not in all_ships1 and [x - 1, y] not in all_ships1:
                            if [x + 1, y] in list2_of_ship3 and [x + 2, y] in list2_of_ship3:
                                print('убит корабль из 3')
                                ships_of_player2['3'] += 1
                                if ships_of_player2['1'] == 4 and ships_of_player2['2'] == 3 and ships_of_player2[
                                    '3'] == 2 \
                                        and ships_of_player2['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 3 поражен')
                                list2_of_ship3.append([x, y])
                        elif [x, y + 1] in all_ships1 and [x, y + 2] in all_ships1 \
                                and [x, y + 3] not in all_ships1 and [x, y - 1] not in all_ships1:
                            if [x, y + 1] in list2_of_ship3 and [x, y + 2] in list2_of_ship3:
                                print('убит корабль из 3')
                                ships_of_player2['3'] += 1
                                if ships_of_player2['1'] == 4 and ships_of_player2['2'] == 3 and ships_of_player2[
                                    '3'] == 2 \
                                        and ships_of_player2['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 3 поражен')
                                list2_of_ship3.append([x, y])
                        elif [x - 1, y] in all_ships1 and [x - 2, y] in all_ships1 \
                                and [x - 3, y] not in all_ships1 and [x + 1, y] not in all_ships1:
                            if [x - 1, y] in list2_of_ship3 and [x - 2, y] in list2_of_ship3:
                                print('убит корабль из 3')
                                ships_of_player2['3'] += 1
                                if ships_of_player2['1'] == 4 and ships_of_player2['2'] == 3 and ships_of_player2[
                                    '3'] == 2 \
                                        and ships_of_player2['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 3 поражен')
                                list2_of_ship3.append([x, y])
                        elif [x, y - 1] in all_ships1 and [x, y - 2] in all_ships1 \
                                and [x, y - 3] not in all_ships1 and [x, y + 1] not in all_ships1:
                            if [x, y - 1] in list2_of_ship3 and [x, y - 2] in list2_of_ship3:
                                print('убит корабль из 3')
                                ships_of_player2['3'] += 1
                                if ships_of_player2['1'] == 4 and ships_of_player2['2'] == 3 and ships_of_player2[
                                    '3'] == 2 \
                                        and ships_of_player2['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 3 поражен')
                                list2_of_ship3.append([x, y])
                        elif [x + 1, y] in all_ships1 and [x - 1, y] in all_ships1 \
                                and [x + 2, y] not in all_ships1 and [x - 2, y] not in all_ships1:
                            if [x + 1, y] in list2_of_ship3 and [x - 1, y] in list2_of_ship3:
                                print('убит корабль из 3')
                                ships_of_player2['3'] += 1
                                if ships_of_player2['1'] == 4 and ships_of_player2['2'] == 3 and ships_of_player2[
                                    '3'] == 2 \
                                        and ships_of_player2['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 3 поражен')
                                list2_of_ship3.append([x, y])
                        elif [x, y + 1] in all_ships1 and [x, y - 1] in all_ships1 \
                                and [x, y + 2] not in all_ships1 and [x, y - 2] not in all_ships1:
                            if [x, y + 1] in list2_of_ship3 and [x, y - 1] in list2_of_ship3:
                                print('убит корабль из 3')
                                ships_of_player2['3'] += 1
                                if ships_of_player2['1'] == 4 and ships_of_player2['2'] == 3 and ships_of_player2[
                                    '3'] == 2 \
                                        and ships_of_player2['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 3 поражен')
                                list2_of_ship3.append([x, y])

                        # двухпалубный

                        elif [x + 1, y] in all_ships1 and [x - 1, y] not in all_ships1 and [x + 2, y] not in all_ships1:
                            if [x + 1, y] in list2_of_ship2:
                                print('убит корабль из 2')
                                ships_of_player2['2'] += 1
                                if ships_of_player2['1'] == 4 and ships_of_player2['2'] == 3 and ships_of_player2[
                                    '3'] == 2 \
                                        and ships_of_player2['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 2 поражен')
                                list2_of_ship2.append([x, y])
                        elif [x, y + 1] in all_ships1 and [x, y - 1] not in all_ships1 and [x, y + 2] not in all_ships1:
                            if [x, y + 1] in list2_of_ship2:
                                print('убит корабль из 2')
                                ships_of_player2['2'] += 1
                                if ships_of_player2['1'] == 4 and ships_of_player2['2'] == 3 and ships_of_player2[
                                    '3'] == 2 \
                                        and ships_of_player2['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 2 поражен')
                                list2_of_ship2.append([x, y])
                        elif [x - 1, y] in all_ships1 and [x + 1, y] not in all_ships1 and [x - 2, y] not in all_ships1:
                            if [x - 1, y] in list2_of_ship2:
                                print('убит корабль из 2')
                                ships_of_player2['2'] += 1
                                if ships_of_player2['1'] == 4 and ships_of_player2['2'] == 3 and ships_of_player2[
                                    '3'] == 2 \
                                        and ships_of_player2['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 2 поражен')
                                list2_of_ship2.append([x, y])
                        elif [x, y - 1] in all_ships1 and [x, y + 1] not in all_ships1 and [x, y - 2] not in all_ships1:
                            if [x, y - 1] in list2_of_ship2:
                                print('убит корабль из 2')
                                ships_of_player2['2'] += 1
                                if ships_of_player2['1'] == 4 and ships_of_player2['2'] == 3 and ships_of_player2[
                                    '3'] == 2 \
                                        and ships_of_player2['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 2 поражен')
                                list2_of_ship2.append([x, y])

                        # четырехпалубный

                        else:
                            if len(list2_of_ship4) == 3:
                                print('убит корабль из 4')
                                ships_of_player2['4'] += 1
                                if ships_of_player2['1'] == 4 and ships_of_player2['2'] == 3 and ships_of_player2[
                                    '3'] == 2 \
                                        and ships_of_player2['4'] == 1:
                                    print('game over')
                                    finish()
                            else:
                                print('корабль из 4 поражен')
                                list2_of_ship4.append([x, y])
                        print(ships_of_player2)

                        # !!!!!!!!!!!!!
                        # здесь происходит запись пораженных кораблей в txt файл
                        # пока что каждый раз заново создается файл, но нужно будет сделать,
                        # чтобы только в конце он 1 раз создался

                        # with open('Ships_of_player2.txt', 'w+') as f:
                        #     pickle.dump(ships_of_player2, f)

                    elif ship_map1[cells_coll[0][1] - 1][cells_coll[0][0] - 1] != 1:
                        print('не прошел')
                        new_near_cells4.append(cells_coll)
                        wave_put = AnimatedSprite(wave_inp, 9, 6, 27 * x + 407, 27 * y + 102)
                        play_game_1()

                drawing = False
        # здесь должен быть переход в режим игры

        all_sprites.draw(screen)
        all_sprites.update()

        f1 = pygame.font.Font('progresspixel_bold.ttf', 15)
        number = 0
        for i in range(115, 350, 27):
            number += 1
            text1 = f1.render(str(number), True, ('white'))
            screen.blit(text1, (i, 100))
            screen.blit(text1, (i + 330, 100))

        text1 = f1.render('10', True, ('white'))
        screen.blit(text1, (354, 100))
        screen.blit(text1, (365 + 318, 100))

        number = 0
        spisok = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'к']
        for i in range(130, 400, 27):
            text1 = f1.render(spisok[number], True, ('white'))
            screen.blit(text1, (90, i))
            screen.blit(text1, (90 + 330, i))

            number += 1

        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(6)
        pygame.display.flip()

        font2 = pygame.font.Font('progresspixel_bold.ttf', 24)
        font3 = pygame.font.Font('progresspixel_bold.ttf', 19)
        text2 = font3.render('player 2:', True, ('#480607'))
        screen.blit(text2, (620, 20))

        text1 = font2.render('your turn', True, ('white'))
        screen.blit(text1, (600, 40))

        board.render(screen)
        board1.render(screen)

        blitt = pygame.Surface((130, 130))
        blitt.fill(('black'))
        screen.blit(blitt, (580, 400))

        font3 = pygame.font.Font('progresspixel_bold.ttf', 15)

        pygame.display.update()


def finish():
    screen.fill((0, 0, 0))

    global ships_of_player1, ships_of_player2, all_ships2, list_of_ship2, list_of_ship3, list_of_ship4, filled_cells4, \
        filled_cells_pl1

    all_ships2 = []

    list_of_ship2 = []
    list_of_ship3 = []
    list_of_ship4 = []

    filled_cells4 = []
    filled_cells_pl1 = []


    ships_of_player1 = {
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0
    }

    ships_of_player2 = {
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0
    }


    running = True
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for object1 in objects:
            object1.process()

        customButton = Button(200, 200, 400, 100, 'play again', start_screen)
        f2 = pygame.font.Font('progresspixel_bold.ttf', 70)
        textt = f2.render('game over', True, (115, 2, 2))
        textt_shadow = f2.render('game over', True, (205, 29, 29))
        screen.blit(textt_shadow, (205, 20))
        screen.blit(textt, (200, 20))


        pygame.display.flip()

        clock.tick(FPS)



def draw_ship(filled_cells_none, near_cells_none, new_near_cells_none, play=False,
              number=1):  # класс для отрисовки заполненных клеток
    global new_near_cells2
    global new_near_cells

    if play is False:
        for i in range(len(filled_cells_none)):
            for y in range(len(filled_cells_none[i])):
                near_cells_none.append([filled_cells_none[i][y][0] - 1, filled_cells_none[i][y][1] - 1])
                near_cells_none.append([filled_cells_none[i][y][0], filled_cells_none[i][y][1] - 1])
                near_cells_none.append([filled_cells_none[i][y][0] + 1, filled_cells_none[i][y][1] - 1])
                near_cells_none.append([filled_cells_none[i][y][0] - 1, filled_cells_none[i][y][1]])
                near_cells_none.append([filled_cells_none[i][y][0] + 1, filled_cells_none[i][y][1]])
                near_cells_none.append([filled_cells_none[i][y][0] - 1, filled_cells_none[i][y][1] + 1])
                near_cells_none.append([filled_cells_none[i][y][0], filled_cells_none[i][y][1] + 1])
                near_cells_none.append([filled_cells_none[i][y][0] + 1, filled_cells_none[i][y][1] + 1])

        for i in near_cells_none:
            if i not in new_near_cells_none:
                new_near_cells_none.append(i)

        for i in sorted(new_near_cells_none):
            if i[0] == 0 or i[0] > 10 or i[1] == 0 or i[1] > 10:
                del new_near_cells_none[new_near_cells_none.index(i)]

        for g in sorted(new_near_cells_none):
            for i in range(len(filled_cells_none)):
                for y in range(len(filled_cells_none[i])):
                    if g == filled_cells_none[i][y]:
                        del new_near_cells_none[new_near_cells_none.index(g)]
    if play is False:
        if len(new_near_cells) == 0:
            x = 410
            near_color = '#2F0404'
            color = '#080101'
        else:
            x = 80
            near_color = '#0A5257'
            color = '#053538'
    else:
        if number == 1:
            x = 80
            near_color = '#2F0404'
            color = '#080101'
        else:
            x = 410
            near_color = '#0A5257'
            color = '#053538'
    for i in range(len(filled_cells_none)):
        for y in range(len(filled_cells_none[i])):
            board2 = Board(11, 11)
            board2.set_view(x, 100, 27)
            board2.fill_cell(filled_cells_none[i][y][0], filled_cells_none[i][y][1], color)
            indexx = near_cells
    for i in new_near_cells_none:
        if play is True:
            board2 = Board(11, 11)
            board2.set_view(x, 100, 27)
            board2.fill_cell(i[0][0], i[0][1], near_color)

        else:
            board2 = Board(11, 11)
            board2.set_view(x, 100, 27)
            board2.fill_cell(i[0], i[1], near_color)


class Board:  # класс для создания полей
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for x_i in range(self.width):
            for y_i in range(self.height):
                fill = 0 if self.board[y_i][x_i] else 1
                left_top_x = x_i * self.cell_size + self.left
                left_top_y = y_i * self.cell_size + self.top
                pygame.draw.rect(screen, pygame.Color('white'), (
                    ((left_top_x, left_top_y), (self.cell_size, self.cell_size))
                ), fill)

    def fill_cell(self, x, y, color='#053538'):
        left_top_x = x * self.cell_size + self.left
        left_top_y = y * self.cell_size + self.top
        pygame.draw.rect(screen, pygame.Color(color), ((left_top_x, left_top_y), (self.cell_size, self.cell_size)))

    def get_cell(self, mouse_pos: Tuple[int, int]) -> Tuple[int, int] or None:
        x, y = mouse_pos
        if x < self.left + self.cell_size or y < self.top + self.cell_size:
            return None
        x -= self.left
        y -= self.top
        if x > self.width * self.cell_size or y > self.height * self.cell_size:
            return None
        x_i = x // self.cell_size
        y_i = y // self.cell_size
        return int(x_i), int(y_i)

    def on_click(self, cell_coords: Tuple[int, int]) -> None:
        x, y = cell_coords
        for y_i in range(self.height):
            current_value = self.board[y][x]
            self.board[y][x] = 0 if current_value else 1

        for x_i in range(self.width):
            if x_i != x:
                current_value = self.board[y][x]
                self.board[y][x] = 0 if current_value else 1

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)
            return cell
        else:
            print(None)

    pygame.display.update()


screen.fill((0, 0, 0))


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    start = 0
    objects = []



    start_screen()

    pygame.display.flip()
    for object in objects:
        object.process()