import pygame, os
from pygame import Vector2
import numpy as np

class Board:

    CELL_SIZE = 100 # dictates the size of the board

    def __init__(self, piece_placement) -> None:
        board = []
        pieces = []
        square_color = Square.LIGHT_SQUARE_COLOR

        #Set a board starting from 8a to 8h, down to 7a - 7h and so on

        for y_pos, rank in enumerate(range(8, 0, -1)): 
            square_row = []
            piece_row = []
            for x_pos, file in enumerate(range(ord('a'), ord('h') + 1)):

                square_notation = '{}{}'.format(chr(file), str(rank))
                square = Square(square_color, Vector2(x_pos * Board.CELL_SIZE, y_pos * Board.CELL_SIZE), square_notation)
                square_row.append(square)

                piece = piece_placement[y_pos][x_pos]
                piece_row.append(Piece(square, piece[0], piece[1])) if piece != '' else piece_row.append('')
                
                #Switches square color each time
                if x_pos == 7: break #makes sure colors alternate each row
                square_color = Square.DARK_SQUARE_COLOR if square_color == Square.LIGHT_SQUARE_COLOR else Square.LIGHT_SQUARE_COLOR

            board.append(square_row)
            pieces.append(piece_row)
        self.board = np.array(board)
        self.board_surface = pygame.Surface((Board.CELL_SIZE * 8, Board.CELL_SIZE * 8))

        self.pieces = np.array(pieces)
        self.piece_surface = pygame.Surface((Board.CELL_SIZE * 8, Board.CELL_SIZE * 8), pygame.SRCALPHA, 32)

    #Retrieve square from code (ie a1, e2)
    def retrieve_square(self, code):
        return self.board[8 - int(code[1:])][ord(code[:1]) - 97]

    def draw_board(self, screen):
        for square in self.board.ravel():
            square.draw_square(self.board_surface)
        screen.blit(self.board_surface, (0,0))

    def draw_pieces(self, screen):
        for piece in self.pieces.ravel():
            if piece != '': piece.draw_piece(self.piece_surface)
        screen.blit(self.piece_surface, (0,0))

class Square:

    LIGHT_SQUARE_COLOR = pygame.color.Color(238, 238, 213)
    DARK_SQUARE_COLOR = pygame.color.Color(125, 148, 93)

    def __init__(self, color, position: Vector2, notation: str) -> None:
        self.color = color
        self.pos = position
        self.notation = notation
    
    def __str__(self):
        return self.notation

    def draw_square(self, board) -> None:
        square_rect = pygame.Rect(self.pos.x, self.pos.y, Board.CELL_SIZE, Board.CELL_SIZE)
        pygame.draw.rect(board, self.color, square_rect)

class Piece:

    #constant vars
    NO_PIECE = 0
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

    WHITE = 8
    BLACK = 16

    def __init__(self, square: Square, piece_type, color) -> None:
        self.color = color
        self.attached_square = square
        self.piece = piece_type
        self.initialize_image()

    def initialize_image(self):
        color = 'White' if self.color == Piece.WHITE else 'Black'

        if self.piece == Piece.PAWN:
            self.image = pygame.image.load(os.path.join('..', 'resources', '{}Pawn.png'.format(color))).convert_alpha()
        elif self.piece == Piece.KNIGHT:
            self.image = pygame.image.load(os.path.join('..', 'resources', '{}Knight.png'.format(color))).convert_alpha()
        elif self.piece == Piece.BISHOP:
            self.image = pygame.image.load(os.path.join('..', 'resources', '{}Bishop.png'.format(color))).convert_alpha()
        elif self.piece == Piece.ROOK:
            self.image = pygame.image.load(os.path.join('..', 'resources', '{}Rook.png'.format(color))).convert_alpha()
        elif self.piece == Piece.QUEEN:
            self.image = pygame.image.load(os.path.join('..', 'resources', '{}Queen.png'.format(color))).convert_alpha()
        elif self.piece == Piece.KING:
            self.image = pygame.image.load(os.path.join('..', 'resources', '{}King.png'.format(color))).convert_alpha()
        
        self.image = pygame.transform.smoothscale(self.image, (Board.CELL_SIZE, Board.CELL_SIZE))

    def draw_piece(self, board: Board):
        board.blit(self.image, (self.attached_square.pos.x, self.attached_square.pos.y))

    @staticmethod
    def opposite_color(color):
        return Piece.WHITE if color == Piece.BLACK else Piece.BLACK