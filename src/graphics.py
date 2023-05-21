import pygame as py
from pygame import Vector2
from board import Square, Piece

#Handles extra graphics for the game
class Graphics:

    #Reference
    board_size = 0

    def __init__(self, board, size, piece_list) -> None:
        self.board = board
        Graphics.board_size = size

        self.pawn_promotion_screen = py.surface.Surface((size, size * 4))
        self.promotion_screen_pieces = py.sprite.Group([Piece(Vector2(0 * size, 0 * size), Piece.QUEEN, Piece.WHITE), \
                                                        Piece(Vector2(0 * size, 0 * size), Piece.KNIGHT, Piece.WHITE), \
                                                        Piece(Vector2(0 * size, 0 * size), Piece.ROOK, Piece.WHITE), \
                                                        Piece(Vector2(0 * size, 0 * size), Piece.BISHOP, Piece.WHITE)])

        #Piece gfx variables
        self.selected_square = None 
        self.orig_square = board[0][0] #Makes it some random square
        self.new_square = board[0][0]  #Same with this

        self.piece_layer = piece_list
    
    #Handles other graphic related properties when moved a piece
    def select_piece_gfx(self, square):
        if self.selected_square != None and self.selected_square != self.new_square and self.selected_square != self.orig_square:
            self.selected_square.selected = False

        if square != self.new_square and square.attached_piece != None and square != self.orig_square:
            square.selected = True
        
        self.selected_square = square

        if square.attached_piece != None: self.piece_layer.change_layer(square.attached_piece, 1)

    def move_piece_gfx(self, orig_square, new_square):
        if orig_square.attached_piece != None: self.piece_layer.change_layer(orig_square.attached_piece, 0)
        
        self.orig_square.selected = False
        self.new_square.selected = False

        self.orig_square = orig_square
        self.orig_square.selected = True
        
        self.new_square = new_square
        self.new_square.selected = True

        self.selected_square = None
    
    def draw_pawn_promotion(self, screen, square: Square, color):
        sq_x = square.pos.x
        sq_y = square.pos.y

        if color == Piece.WHITE:
            for index, piece in enumerate(self.promotion_screen_pieces.sprites()):
                piece.color = Piece.WHITE
                piece.pos.x = sq_x
                piece.pos.y = (index) * Graphics.board_size
                piece.update_rect()
                piece.update_image()
        elif color == Piece.BLACK:
            sq_y -= 3 * Graphics.board_size
            for index, piece in enumerate(self.promotion_screen_pieces.sprites()):
                piece.color = Piece.BLACK
                piece.pos.x = sq_x
                piece.pos.y = (7-index) * Graphics.board_size
                piece.update_rect()
                piece.update_image()

        self.pawn_promotion_screen.fill('lightgray')

        #Border
        py.draw.rect(self.pawn_promotion_screen, 'gray', py.Rect(0,0, Graphics.board_size, Graphics.board_size / 10))
        py.draw.rect(self.pawn_promotion_screen, 'gray', py.Rect(0,0, Graphics.board_size / 10, Graphics.board_size * 4))
        py.draw.rect(self.pawn_promotion_screen, 'gray', py.Rect(0,(Graphics.board_size * 4) - (Graphics.board_size / 10), Graphics.board_size, Graphics.board_size / 10))
        py.draw.rect(self.pawn_promotion_screen, 'gray', py.Rect(Graphics.board_size - (Graphics.board_size / 10), 0, Graphics.board_size / 10, Graphics.board_size * 4))
        
        screen.blit(self.pawn_promotion_screen, (sq_x, sq_y))
        self.promotion_screen_pieces.draw(screen)
            