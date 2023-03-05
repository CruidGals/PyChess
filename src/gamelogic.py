import pygame
from pygame import Vector2
import numpy as np
from board import Piece

class GameLogic:
    def __init__(self, piece_placement):
        self.piece_placement = piece_placement

        #Noting king positions
        for piece in piece_placement.ravel():
            if piece.piece == Piece.KING:
                if piece.color == Piece.WHITE: self.white_king = piece
                else: self.black_king = piece
    
    #Piece Moves -----------------------------------------
    def pawn_moves(self, piece: Piece):
        row = np.argwhere(self.piece_placement == piece)[0][0]
        col = np.argwhere(self.piece_placement == piece)[0][1]
        range_of_motion = []
        direction = 1 if piece.color == Piece.BLACK else -1

        for i in range(-1, 2):
            if not self.within_bounds(row + direction, col + i):
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

    def is_checked(self, king: Piece, scenario) -> bool:
        color = king.color
        row = np.argwhere(scenario == king)[0][0]
        col = np.argwhere(scenario == king)[0][1]

        #Check vertical: negative means up, positive means down
        for direction in range(-1, 2, 2):
            for i in range(direction, direction * 8, direction):
                if not self.within_bounds(row + i, col): break

                targeted_piece = scenario[row + i][col]

                if targeted_piece.color == color:
                    break
                elif targeted_piece.color == Piece.opposite_color(color):
                    if (targeted_piece.piece == Piece.ROOK) or (targeted_piece.piece == Piece.QUEEN):
                        return True
                    break
        
        #Check Horizontal and Diagonals: negative means left, postive means right
        #Starts top left diagonal. ends bottom right diagonal
        # (Remember, row is accessed from top to bottom, col is accessed from left to right)
        for x_dir in range(-1, 2, 2):
            for y_dir in range(-1, 2):
                for i in range(1, 8):
                    dx = i * x_dir
                    dy = i * y_dir

                    if not self.within_bounds(row + dy, col + dx): break

                    targeted_piece = scenario[row + dy][col + dx]

                    if targeted_piece.color == color:
                        break
                    elif targeted_piece.color == Piece.opposite_color(color):
                        #Check Pawn
                        if dy == -1 and color == Piece.WHITE:
                            return True         
                        elif dy == 1 and color == Piece.BLACK:
                            return True

                        #Check Rook
                        if dy == 0 and targeted_piece.piece == Piece.ROOK:
                            return True

                        if (targeted_piece.piece == Piece.BISHOP) or (targeted_piece.piece == Piece.QUEEN):
                            return True
                        break
        
        #Check for knights: go on each diagnoal, then check outer sides of each diagonal
        for x_dir in range(-1, 2, 2):
            for y_dir in range(-1, 2, 2):
                if self.within_bounds(row + y_dir * 2, col + x_dir):
                    targeted_piece = scenario[row + y_dir * 2][col + x_dir]
                    if targeted_piece.color == Piece.opposite_color(color) and targeted_piece.piece == Piece.KNIGHT:
                        return True
                
                if self.within_bounds(row + y_dir, col + x_dir * 2):
                    targeted_piece = scenario[row + y_dir][col + x_dir * 2]
                    if targeted_piece.color == Piece.opposite_color(color) and targeted_piece.piece == Piece.KNIGHT:
                        return True
        
        return False
                       
    def within_bounds(self, x, y) -> bool:
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        else:
            return True