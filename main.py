from typing import Tuple

import pygame, sys

pygame.font.init()


class Board:
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

    def get_cell(self, mouse_pos: Tuple[int, int]) -> Tuple[int, int]:
        x, y = mouse_pos
        if x < self.left or y < self.top:
            return None
        x -= self.left
        y -= self.top
        if x > self.width * self.cell_size or y > self.height * self.cell_size:
            return None
        x_i = x // self.cell_size
        y_i = y // self.cell_size
        return x_i, y_i


if __name__ == '__main__':
    size = width, height = 800, 500
    screen = pygame.display.set_mode(size)


    board = Board(11, 11)
    board.set_view(40, 80, 32)
    board1 = Board(11, 11)
    board1.set_view(410, 80, 32)
    running = True

    screen.fill((0, 0, 0))
    board.render(screen)
    board1.render(screen)

    # текст координат
    f1 = pygame.font.Font(None, 33)
    number = 0
    for i in range(82, 340, 32):
        number += 1
        text1 = f1.render(str(number), True, ('white'))
        screen.blit(text1, (i, 85))
        screen.blit(text1, (i + 370, 85))

    text1 = f1.render('10', True, ('white'))
    screen.blit(text1, (365, 85))
    screen.blit(text1, (365 + 370, 85))


    number = 0
    spisok = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'к']
    for i in range(114, 420, 32):
        text1 = f1.render(spisok[number], True, ('white'))
        screen.blit(text1, (50, i))
        screen.blit(text1, (50 + 370, i))

        number += 1




    # конец текста координат

    pygame.display.update()

    while 1:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()

    pygame.display.flip()
