import pygame
from pygame import Vector2
import numpy as np

class Board:

    cell_size = 150

    def __init__(self) -> None:
        board = []
        square_color = Square.LIGHT_SQUARE_COLOR

        #Set a board starting from 8a to 8h, down to 7a - 7h and so on

        for y_pos, rank in enumerate(range(8, 0, -1)): 
            row = []
            for x_pos, file in enumerate(range(ord('a'), ord('h') + 1)):

                square_notation = '{}{}'.format(str(rank), chr(file))
                row.append(Square(square_color, Vector2(x_pos * Board.cell_size, y_pos * Board.cell_size), square_notation))
                
                #Switches square color each time
                if x_pos == 7: break #makes sure colors alternate each row
                square_color = Square.DARK_SQUARE_COLOR if square_color == Square.LIGHT_SQUARE_COLOR else Square.LIGHT_SQUARE_COLOR

            board.append(row)
        self.board = np.array(board)
        self.board_surface = pygame.Surface((Board.cell_size * 8, Board.cell_size * 8))

    
    def draw_board(self, screen):
        for square in self.board.ravel():
            square.draw_square(self.board_surface)
        screen.blit(self.board_surface, (0,0))

class Square:

    LIGHT_SQUARE_COLOR = pygame.color.Color(238, 238, 213)
    DARK_SQUARE_COLOR = pygame.color.Color(125, 148, 93)

    def __init__(self, color, position: Vector2, notation: str) -> None:
        self.color = color
        self.pos = position
        self.notation = notation
        pass

    def draw_square(self, board) -> None:
        square_rect = pygame.Rect(self.pos.x, self.pos.y, Board.cell_size, Board.cell_size)
        pygame.draw.rect(board, self.color, square_rect)
        pass
