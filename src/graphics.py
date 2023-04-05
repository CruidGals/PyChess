import pygame as py
from board import Square, Piece

#Handles extra graphics for the game
class Graphics:
    def __init__(self, board) -> None:
        self.board = board

        #Piece gfx variables
        self.selected_square = None
        self.orig_square = None
        self.new_square = None
    
    #Handles other graphic related properties when moved a piece
    def select_piece_gfx(self, square):
        pass

    def move_piece_gfx(self, orig_square, new_square):
        pass