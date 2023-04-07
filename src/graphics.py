import pygame as py
from board import Square, Piece

#Handles extra graphics for the game
class Graphics:
    def __init__(self, board) -> None:
        self.board = board

        #Piece gfx variables
        self.selected_square = None 
        self.orig_square = board[0][0] #Makes it some random square
        self.new_square = board[0][0]  #Same with this
    
    #Handles other graphic related properties when moved a piece
    def select_piece_gfx(self, square):
        if self.selected_square != None and self.selected_square != self.new_square:
            self.selected_square.selected = False

        if square != self.new_square and square.attached_piece != None:
            square.selected = True
        
        self.selected_square = square

    def move_piece_gfx(self, orig_square, new_square):
        self.orig_square.selected = False
        self.new_square.selected = False

        self.orig_square = orig_square
        self.orig_square.selected = True
        
        self.new_square = new_square
        self.new_square.selected = True

        self.selected_square = None