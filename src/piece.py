import pygame, os
from pygame import Vector2
class Piece():

    #constant vars
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

    WHITE = 8
    BLACK = 16

    def __init__(self, square, piece_type, color) -> None:
        self.color = color
        self.attached_square = square
        self.piece = piece_type
        self.image = self.initialize_image()

    def initialize_image(self):
        color = 'White' if color == Piece.WHITE else 'Black'

        if self.piece == Piece.PAWN:
            return pygame.image.load(os.path.join('..', 'resources', '{}Pawn.png'.format(color))).convert_alpha()
        elif self.piece == Piece.KNIGHT:
            return pygame.image.load(os.path.join('..', 'resources', '{}Knight.png'.format(color))).convert_alpha()
        elif self.piece == Piece.BISHOP:
            return pygame.image.load(os.path.join('..', 'resources', '{}Bishop.png'.format(color))).convert_alpha()
        elif self.piece == Piece.ROOK:
            return pygame.image.load(os.path.join('..', 'resources', '{}Rook.png'.format(color))).convert_alpha()
        elif self.piece == Piece.QUEEN:
            return pygame.image.load(os.path.join('..', 'resources', '{}Queen.png'.format(color))).convert_alpha()
        elif self.piece == Piece.KING:
            return pygame.image.load(os.path.join('..', 'resources', '{}King.png'.format(color))).convert_alpha()
    
    def draw_piece(self, board):
        board.board_surface.blit(self.image, (self.attached_square.pos.x, self.attached_square.pos.y))

    #Piece Moves -----------------------------------------
    def pawn_moves(self, board):
        pass
    
    def knight_moves(self, board):
        pass

    def bishop_moves(self, board):
        pass

    def rook_moves(self, board):
        pass

    def queen_moves(self, board):
        pass

    def king_moves(self, board):
        pass