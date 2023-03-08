import pygame
from pygame import Vector2
import numpy as np
from board import Piece

class GameLogic:
    def __init__(self, piece_placement):
        self.piece_placement = piece_placement
        self.white_king = None
        self.black_king = None

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
                if self.test_move((row, col), (row + direction, col), piece.color): 
                    range_of_motion.append(self.piece_placement[row + direction][col].attached_square)

                #Checking double move:
                if (row == 1 and piece.color == Piece.BLACK) or (row == 6 and piece.color == Piece.WHITE) and self.piece_placement[row + (2 * direction)][col].piece == Piece.NO_PIECE:
                    if self.test_move((row, col), (row + (2 * direction), col), piece.color):
                        range_of_motion.append(self.piece_placement[row + (2 * direction)][col].attached_square)
            elif self.piece_placement[row + direction][col + i].color == Piece.opposite_color(piece.color):
                if self.test_move((row, col), (row + direction, col + i), piece.color):
                    range_of_motion.append(self.piece_placement[row + direction][col + i].attached_square)
        
        return range_of_motion
    
    def knight_moves(self, piece: Piece):
        row = np.argwhere(self.piece_placement == piece)[0][0]
        col = np.argwhere(self.piece_placement == piece)[0][1]
        range_of_motion = []

        for x_dir in range(-1, 2, 2):
            for y_dir in range(-1, 2, 2):
                if GameLogic.within_bounds(row + y_dir * 2, col + x_dir):
                    targeted_piece = self.piece_placement[row + y_dir * 2][col + x_dir]

                    if targeted_piece.color != piece.color:
                        if self.test_move((row, col), (row + y_dir * 2, col + x_dir), piece.color):
                            range_of_motion.append(targeted_piece.attached_square)

                if GameLogic.within_bounds(row + y_dir, col + x_dir * 2):
                    targeted_piece = self.piece_placement[row + y_dir][col + x_dir * 2]

                    if targeted_piece.color != piece.color:
                        if self.test_move((row, col), (row + y_dir, col + x_dir * 2), piece.color):
                            range_of_motion.append(targeted_piece.attached_square)
            
        return range_of_motion
                    
    def bishop_moves(self, piece: Piece):
        row = np.argwhere(self.piece_placement == piece)[0][0]
        col = np.argwhere(self.piece_placement == piece)[0][1]
        range_of_motion = []

        for dx in range(-1, 2, 2):
            for dy in range(-1, 2, 2):
                for i in range(1, 8):
                    if GameLogic.within_bounds(row + (i * dy), col + (i * dx)):
                        targeted_piece = self.piece_placement[row + (i * dy)][col + (i * dx)]
                        
                        if targeted_piece.color == piece.color:
                            break
                        else:
                            if self.test_move((row, col), (row + (i * dy), col + (i * dx)), piece.color):
                                range_of_motion.append(targeted_piece.attached_square)
        
        return range_of_motion

    def rook_moves(self, piece):
        row = np.argwhere(self.piece_placement == piece)[0][0]
        col = np.argwhere(self.piece_placement == piece)[0][1]
        range_of_motion = []

    def queen_moves(self, piece):
        row = np.argwhere(self.piece_placement == piece)[0][0]
        col = np.argwhere(self.piece_placement == piece)[0][1]
        range_of_motion = []

    def king_moves(self, piece):
        row = np.argwhere(self.piece_placement == piece)[0][0]
        col = np.argwhere(self.piece_placement == piece)[0][1]
        range_of_motion = []

    def is_checked(self, color, ignore_piece: Piece | None) -> bool:
        if self.white_king == None or self.black_king == None: return False

        king = self.white_king if color == Piece.WHITE else self.black_king
        row = np.argwhere(self.piece_placement == king)[0][0]
        col = np.argwhere(self.piece_placement == king)[0][1]

        #Check vertical: negative means up, positive means down
        for direction in range(-1, 2, 2):
            for i in range(direction, direction * 8, direction):
                if not GameLogic.within_bounds(row + i, col): break

                targeted_piece = self.piece_placement[row + i][col]
                if targeted_piece == ignore_piece: break

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

                    if not GameLogic.within_bounds(row + dy, col + dx): break

                    targeted_piece = self.piece_placement[row + dy][col + dx]
                    if targeted_piece == ignore_piece: break

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
                if GameLogic.within_bounds(row + y_dir * 2, col + x_dir):
                    targeted_piece = self.piece_placement[row + y_dir * 2][col + x_dir]
                    if targeted_piece == ignore_piece: break
                    if targeted_piece.color == Piece.opposite_color(color) and targeted_piece.piece == Piece.KNIGHT:
                        return True
                
                if GameLogic.within_bounds(row + y_dir, col + x_dir * 2):
                    targeted_piece = self.piece_placement[row + y_dir][col + x_dir * 2]
                    if targeted_piece == ignore_piece: break
                    if targeted_piece.color == Piece.opposite_color(color) and targeted_piece.piece == Piece.KNIGHT:
                        return True
        
        return False

    def test_move(self, original_coords, new_coords, color):
        orig_piece = self.piece_placement[original_coords[0]][original_coords[1]]
        target_piece = self.piece_placement[new_coords[0]][new_coords[1]]
        status = False
        ignore_piece = None

        #Ignore piece used to ignore the piece that is being swapped that would be removed from the board
        if target_piece.color == Piece.opposite_color(color):
            ignore_piece = target_piece

        orig_piece, target_piece = target_piece, orig_piece
        if not self.is_checked(color, ignore_piece):
            status = True
        orig_piece, target_piece = target_piece, orig_piece

        return status


    @staticmethod               
    def within_bounds(x, y) -> bool:
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        else:
            return True