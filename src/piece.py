import pygame, os

WHITE = 0
BLACK = 1

class Pawn:
    WHITE_PIECE = pygame.image.load(os.path.join('..', 'resources', 'WhitePawn.png'))
    BLACK_PIECE = pygame.image.load(os.path.join('..', 'resources', 'BlackPawn.png'))

    def __init__(self, color) -> None:
        self.color = color
        self.image = Pawn.WHITE_PIECE if color == 0 else Pawn.BLACK_PIECE

class Knight:
    WHITE_PIECE = pygame.image.load(os.path.join('..', 'resources', 'WhiteKnight.png'))
    BLACK_PIECE = pygame.image.load(os.path.join('..', 'resources', 'BlackKnight.png'))

    def __init__(self, color) -> None:
        self.color = color
        self.image = Knight.WHITE_PIECE if color == 0 else Knight.BLACK_PIECE

class Bishop:
    WHITE_PIECE = pygame.image.load(os.path.join('..', 'resources', 'WhiteBishop.png'))
    BLACK_PIECE = pygame.image.load(os.path.join('..', 'resources', 'BlackBishop.png'))

    def __init__(self, color) -> None:
        self.color = color
        self.image = Bishop.WHITE_PIECE if color == 0 else Bishop.BLACK_PIECE

class Rook:
    WHITE_PIECE = pygame.image.load(os.path.join('..', 'resources', 'WhiteRook.png'))
    BLACK_PIECE = pygame.image.load(os.path.join('..', 'resources', 'BlackRook.png'))

    def __init__(self, color) -> None:
        self.color = color
        self.image = Rook.WHITE_PIECE if color == 0 else Rook.BLACK_PIECE

class Queen:
    WHITE_PIECE = pygame.image.load(os.path.join('..', 'resources', 'WhiteQueen.png'))
    BLACK_PIECE = pygame.image.load(os.path.join('..', 'resources', 'BlackQueen.png'))

    def __init__(self, color) -> None:
        self.color = color
        self.image = Queen.WHITE_PIECE if color == 0 else Queen.BLACK_PIECE

class King:
    WHITE_PIECE = pygame.image.load(os.path.join('..', 'resources', 'WhiteKing.png'))
    BLACK_PIECE = pygame.image.load(os.path.join('..', 'resources', 'BlackKing.png'))

    def __init__(self, color) -> None:
        self.color = color
        self.image = King.WHITE_PIECE if color == 0 else King.BLACK_PIECE


