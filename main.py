from typing import Tuple

import pygame, sys, os
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
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
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
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


def start_screen():  # функция для запуска стартового окна
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


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image.set_colorkey(('white'))
    return image


filled_cells = []   # список заполняемых клеток для первого поля (корабли)
filled_cells2 = []  # список заполняемых клеток для второго поля  (корабли)

near_cells = []   # промежуточный список для создания конечного new_near_cells
near_cells2 = []   # # промежуточный список для создания конечного new_near_cells2


new_near_cells = []   # список заполняемых клеток для первого поля (клетки вокруг кораблей, которые нельзя заполнять)
new_near_cells2 = []   # # список заполняемых клеток для второго поля (клетки вокруг кораблей, которые нельзя заполнять)

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
            ]                                   # карта с кораблями первого игрока
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
            ]                                  # карта с кораблями второго игрока





def start_game_player1():
    global new_near_cells

    game = True

    clock = pygame.time.Clock()

    # wave = load_image("waves2.jpg")
    # wave = pygame.transform.scale(wave, (500, 400))
    # waves = AnimatedSprite(wave, 9, 6, 320, 305)

    # wave = load_image("reversed.jpg")
    # wave1 = pygame.transform.scale(wave, (300, 200))
    # waves1 = AnimatedSprite(wave1, 9, 6, 180, 203)       попытка добавить анимацию на поле

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
                                ship_map1[i[0] - 1][i[1] - 1] = 1
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
                                ship_map1[i[0] - 1][i[1] - 1] = 1
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
                                ship_map1[i[0] - 1][i[1] - 1] = 1
                            filled_cells.append(spisok)
                            print(filled_cells)
                            cells2 -= 1

                if len(spisok) == 1 and cells1 > 0:
                    if spisok[0] not in new_near_cells:
                        for i in spisok:
                            ship_map1[i[0] - 1][i[1] - 1] = 1
                        filled_cells.append(spisok)
                        print(filled_cells)
                        cells1 -= 1

                drawing = False


            # если все корабли выставлены, теперь корабли выбирает второй игрок
            if cells1 == 0 and cells2 == 0 and cells3 == 0 and cells4 == 0:
                new_near_cells = []
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
    global new_near_cells2

    game = True

    ship_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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

    clock = pygame.time.Clock()

    # wave = load_image("waves2.jpg")
    # wave = pygame.transform.scale(wave, (500, 400))
    # waves = AnimatedSprite(wave, 9, 6, 320, 305)

    # wave = load_image("reversed.jpg")
    # wave1 = pygame.transform.scale(wave, (300, 200))
    # waves1 = AnimatedSprite(wave1, 9, 6, 180, 203)

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
                                ship_map2[i[0] - 1][i[1] - 1] = 1
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
                                ship_map2[i[0] - 1][i[1] - 1] = 1
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
                                ship_map2[i[0] - 1][i[1] - 1] = 1
                            filled_cells2.append(spisok)
                            print(filled_cells2)
                            cells2 -= 1

                if len(spisok) == 1 and cells1 > 0:
                    if spisok[0] not in new_near_cells2:
                        for i in spisok:
                            ship_map2[i[0] - 1][i[1] - 1] = 1
                        filled_cells2.append(spisok)
                        print(filled_cells2)
                        cells1 -= 1

                drawing = False

            if cells1 == 0 and cells2 == 0 and cells3 == 0 and cells4 == 0:
                new_near_cells = []
                print('over')
                print(ship_map1)
                print(ship_map2)   # здесь должен быть переход в режим игры

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


def draw_ship(filled_cells, near_cells, new_near_cells3):   # класс для отрисовки заполненных клеток
    global new_near_cells2
    global new_near_cells

    for i in range(len(filled_cells)):
        for y in range(len(filled_cells[i])):
            near_cells.append([filled_cells[i][y][0] - 1, filled_cells[i][y][1] - 1])
            near_cells.append([filled_cells[i][y][0], filled_cells[i][y][1] - 1])
            near_cells.append([filled_cells[i][y][0] + 1, filled_cells[i][y][1] - 1])
            near_cells.append([filled_cells[i][y][0] - 1, filled_cells[i][y][1]])
            near_cells.append([filled_cells[i][y][0] + 1, filled_cells[i][y][1]])
            near_cells.append([filled_cells[i][y][0] - 1, filled_cells[i][y][1] + 1])
            near_cells.append([filled_cells[i][y][0], filled_cells[i][y][1] + 1])
            near_cells.append([filled_cells[i][y][0] + 1, filled_cells[i][y][1] + 1])

    for i in near_cells:
        if i not in new_near_cells3:
            new_near_cells3.append(i)

    for i in sorted(new_near_cells3):
        if i[0] == 0 or i[0] > 10 or i[1] == 0 or i[1] > 10:
            del new_near_cells3[new_near_cells3.index(i)]

    for g in sorted(new_near_cells3):
        for i in range(len(filled_cells)):
            for y in range(len(filled_cells[i])):
                if g == filled_cells[i][y]:
                    del new_near_cells3[new_near_cells3.index(g)]
    if len(new_near_cells) == 0:
        x = 410
        near_color = '#2F0404'
        color = '#080101'
    else:
        x = 80
        near_color = '#0A5257'
        color = '#053538'
    for i in range(len(filled_cells)):
        for y in range(len(filled_cells[i])):
            board2 = Board(11, 11)
            board2.set_view(x, 100, 27)
            board2.fill_cell(filled_cells[i][y][0], filled_cells[i][y][1], color)
            indexx = near_cells

    for i in new_near_cells3:
        board2 = Board(11, 11)
        board2.set_view(x, 100, 27)
        board2.fill_cell(i[0], i[1], near_color)


class Board:   # класс для создания полей
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

running = True
x_pos1 = 800

while True:
    surf1 = pygame.Surface((130, 130))
    surf1.fill(('black'))
    screen.blit(surf1, (x_pos1, 70))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    start_screen()

    x_pos1 -= 4
    if x_pos1 <= -200:
        x_pos1 = 800

    pygame.display.flip()
    for object in objects:
        object.process()
