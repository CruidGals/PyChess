import pygame
import numpy as np
from board import Piece

class GameLogic:
    def __init__(self, piece_placement):
        self.piece_placement = piece_placement
    
    #Piece Moves -----------------------------------------
    def pawn_moves(self, piece: Piece):
        row = np.argwhere(self.piece_placement == piece)[0][0]
        col = np.argwhere(self.piece_placement == piece)[0][1]
        range_of_motion = []
        direction = 1 if piece.color == Piece.BLACK else -1

        for i in range(-1, 2):
            if not (0 <= (row + direction) < 8) or not (0 <= (col + i) < 8):
                continue
            
            if i == 0 and self.piece_placement[row + direction][col].piece == Piece.NO_PIECE:
                range_of_motion.append(self.piece_placement[row + direction][col].attached_square)

                #Checking double move:
                if (row == 1 and piece.color == Piece.BLACK) or (row == 6 and piece.color == Piece.WHITE) and self.piece_placement[row + (2 * direction)][col].piece == Piece.NO_PIECE:
                    range_of_motion.append(self.piece_placement[row + (2 * direction)][col].attached_square)
            elif self.piece_placement[row + direction][col + i].color == Piece.opposite_color(piece.color):
                range_of_motion.append(self.piece_placement[row + direction][col + i].attached_square)
        
        return range_of_motion
    
    def knight_moves(self, piece):
        pass

    def bishop_moves(self, piece):
        pass

    def rook_moves(self, piece):
        pass

    def queen_moves(self, piece):
        pass

    def king_moves(self, piece):
        pass

    def is_check(self) -> bool:
        pass