import pygame
from pygame import Vector2
import numpy as np
from board import Piece, Square

#In this class, it uses a list of squares to access the pieces on the board. This means that
#you should assume every variable that seems to contain a piece to contain a Square,
#Ex. variale white_king will store the SQUARE of the white king, not the piece itself.
class GameLogic:
    def __init__(self, board):
        self.board = board
        self.white_king = None
        self.black_king = None

        #Noting king positions
        for square in self.board.ravel():
            piece = square.attached_piece
            if piece == None: continue
            elif piece.piece == Piece.KING:
                if piece.color == Piece.WHITE: self.white_king = square
                else: self.black_king = square
    
    def piece_moves(self, square: Square):
        piece = square.attached_piece
        if piece == None: return

        if piece.piece == Piece.PAWN: return self.pawn_moves(square)
        elif piece.piece == Piece.KNIGHT: return self.knight_moves(square)
        elif piece.piece == Piece.BISHOP: return self.bishop_moves(square)
        elif piece.piece == Piece.ROOK: return self.rook_moves(square)
        elif piece.piece == Piece.QUEEN: return self.queen_moves(square)
        elif piece.piece == Piece.KING: return self.king_moves(square)

    #Piece Moves -----------------------------------------
    # (Assume that piece does not equal None) ------------
    def pawn_moves(self, square: Square):
        piece = square.attached_piece

        row = np.argwhere(self.board == square)[0][0]
        col = np.argwhere(self.board == square)[0][1]
        range_of_motion = []
        direction = 1 if piece.color == Piece.BLACK else -1

        for i in range(-1, 2):
            if not self.within_bounds(row + direction, col + i):
                continue
            
            if i == 0:
                if self.board[row + direction][col].attached_piece == None:
                    if self.test_move((row, col), (row + direction, col), piece.color): 
                        range_of_motion.append(self.board[row + direction][col])

                    #Checking double move:
                    if (row == 1 and piece.color == Piece.BLACK) or (row == 6 and piece.color == Piece.WHITE) and self.board[row + (2 * direction)][col].attached_piece == None:
                        if self.test_move((row, col), (row + (2 * direction), col), piece.color):
                            range_of_motion.append(self.board[row + (2 * direction)][col])
            elif self.board[row + direction][col + i].attached_piece != None and self.board[row + direction][col + i].attached_piece.color == Piece.opposite_color(piece.color):
                if self.test_move((row, col), (row + direction, col + i), piece.color):
                    range_of_motion.append(self.board[row + direction][col + i])
        
        return range_of_motion
    
    def knight_moves(self, square: Square):
        piece = square.attached_piece

        row = np.argwhere(self.board == square)[0][0]
        col = np.argwhere(self.board == square)[0][1]
        range_of_motion = []

        for x_dir in range(-1, 2, 2):
            for y_dir in range(-1, 2, 2):
                if GameLogic.within_bounds(row + y_dir * 2, col + x_dir):
                    targeted_piece = self.board[row + y_dir * 2][col + x_dir].attached_piece

                    if targeted_piece != None and targeted_piece.color != piece.color:
                        if self.test_move((row, col), (row + y_dir * 2, col + x_dir), piece.color):
                            range_of_motion.append(self.board[row + y_dir * 2][col + x_dir])

                if GameLogic.within_bounds(row + y_dir, col + x_dir * 2):
                    targeted_piece = self.board[row + y_dir][col + x_dir * 2].attached_piece

                    if targeted_piece != None and targeted_piece.color != piece.color:
                        if self.test_move((row, col), (row + y_dir, col + x_dir * 2), piece.color):
                            range_of_motion.append(self.board[row + y_dir][col + x_dir * 2])
            
        return range_of_motion
                    
    def bishop_moves(self, square: Square):
        piece = square.attached_piece

        row = np.argwhere(self.board == square)[0][0]
        col = np.argwhere(self.board == square)[0][1]
        range_of_motion = []

        for dx in range(-1, 2, 2):
            for dy in range(-1, 2, 2):
                for i in range(1, 8):
                    if not GameLogic.within_bounds(row + (i * dy), col + (i * dx)): break
                    
                    targeted_piece = self.board[row + (i * dy)][col + (i * dx)].attached_piece
                    if targeted_piece == None and self.test_move((row, col), (row + (i * dy), col + (i * dx)), Piece.NO_COLOR):
                        range_of_motion.append(self.board[row + (i * dy)][col + (i * dx)])
                        continue

                    if targeted_piece.color == piece.color:
                        break
                    else:
                        if self.test_move((row, col), (row + (i * dy), col + (i * dx)), piece.color):
                            range_of_motion.append(self.board[row + (i * dy)][col + (i * dx)])
                        if targeted_piece.color == Piece.opposite_color(piece.color):
                            break
        
        return range_of_motion

    def rook_moves(self, square: Square):
        piece = square.attached_piece

        row = np.argwhere(self.board == square)[0][0]
        col = np.argwhere(self.board == square)[0][1]
        range_of_motion = []

        #Check vertically
        for dir in range(-1, 2, 2):
            for i in range(1,8):
                if not GameLogic.within_bounds(row + i * dir, col): break

                targeted_piece = self.board[row + i * dir][col].attached_piece
                if targeted_piece == None and self.test_move((row, col), (row + i * dir, col), Piece.NO_COLOR):
                    range_of_motion.append(self.board[row + i * dir][col])
                    continue
                
                if targeted_piece.color == piece.color:
                    break
                else:
                    if self.test_move((row, col), (row + i * dir, col), piece.color):
                        range_of_motion.append(self.board[row + i * dir][col])
                    
                    if targeted_piece.color == Piece.opposite_color(piece.color):
                            break

        #Check Horizontally
        for dir in range(-1, 2, 2):
            for i in range(1,8):
                if not GameLogic.within_bounds(row, col + i * dir): break

                targeted_piece = self.board[row][col + i * dir].attached_piece
                if targeted_piece == None and self.test_move((row, col), (row, col + i * dir), Piece.NO_COLOR):
                    range_of_motion.append(self.board[row][col + i * dir])
                    continue
                
                if targeted_piece.color == piece.color:
                    break
                else:
                    if self.test_move((row, col), (row, col + i * dir), piece.color):
                        range_of_motion.append(self.board[row][col + i * dir])
                    
                    if targeted_piece.color == Piece.opposite_color(piece.color):
                            break
        
        return range_of_motion

    def queen_moves(self, square: Square):
        range_of_motion = []

        for square in self.bishop_moves(square):
            range_of_motion.append(square)
        for square in self.rook_moves(square):
            range_of_motion.append(square)
        
        return range_of_motion

    def king_moves(self, square: Square):
        piece = square.attached_piece

        row = np.argwhere(self.board == square)[0][0]
        col = np.argwhere(self.board == square)[0][1]
        range_of_motion = []

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if (dx == 0 and dy == 0) or not GameLogic.within_bounds(row + dy, col + dx): continue

                targeted_piece = self.board[row + dy][col + dx].attached_piece
                if targeted_piece == None and self.test_move((row, col), (row + dy, col + dx), Piece.NO_COLOR):
                    range_of_motion.append(self.board[row + dy][col + dx])
                    continue

                if targeted_piece.color == piece.color:
                    continue
                else:
                    if self.test_move((row, col), (row + dy, col + dx), piece.color):
                        range_of_motion.append(self.board[row + dy][col + dx])
                    
                    if targeted_piece.color == Piece.opposite_color(piece.color):
                        continue
        
        return range_of_motion

    def is_checked(self, color, ignore_square: Square | None, king_coords: tuple | None) -> bool:
        if self.white_king == None or self.black_king == None: return False

        king_square = self.white_king if color == Piece.WHITE else self.black_king
        row = np.argwhere(self.board == king_square)[0][0]
        col = np.argwhere(self.board == king_square)[0][1]

        if king_coords != None:
            row = king_coords[0]
            col = king_coords[1]
 
        #Check vertical: negative means up, positive means down
        for direction in range(-1, 2, 2):
            for i in range(direction, direction * 8, direction):
                if not GameLogic.within_bounds(row + i, col) or self.board[row + i][col] == ignore_square: break

                targeted_piece = self.board[row + i][col].attached_piece
                if targeted_piece == None: continue

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

                    if not GameLogic.within_bounds(row + dy, col + dx) or self.board[row + dy][col + dx] == ignore_square: break

                    targeted_piece = self.board[row + dy][col + dx].attached_piece
                    if targeted_piece == None: continue

                    if targeted_piece.color == color:
                        break
                    elif targeted_piece.color == Piece.opposite_color(color):
                        #Check Pawn
                        if targeted_piece == Piece.PAWN:
                            if dy == -1 and color == Piece.WHITE: return True
                            elif dy == 1 and color == Piece.BLACK : return True    

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

                    if self.board[row + y_dir * 2][col + x_dir] == ignore_square: break
                    targeted_piece = self.board[row + y_dir * 2][col + x_dir].attached_piece

                    if targeted_piece != None:
                        if targeted_piece.color == Piece.opposite_color(color) and targeted_piece.piece == Piece.KNIGHT:
                            return True
                
                if GameLogic.within_bounds(row + y_dir, col + x_dir * 2):
                    
                    if self.board[row + y_dir * 2][col + x_dir] == ignore_square: break
                    targeted_piece = self.board[row + y_dir][col + x_dir * 2].attached_piece
                    
                    if targeted_piece != None:
                        if targeted_piece.color == Piece.opposite_color(color) and targeted_piece.piece == Piece.KNIGHT:
                            return True
        
        return False

    def test_move(self, original_coords, new_coords, color):
        orig_square = self.board[original_coords[0]][original_coords[1]]
        target_square = self.board[new_coords[0]][new_coords[1]]
        status = False
        ignore_square = None
        king_coords = None

        if target_square.attached_piece != None:
            #Ignore piece used to ignore the piece that is being swapped that would be removed from the board
            if target_square.attached_piece.color == Piece.opposite_color(color):
                ignore_square = target_square

            #Checks if this function was called by king moves
            if orig_square.attached_piece.piece == Piece.KING:
                king_coords = (np.argwhere(self.board == target_square)[0][0], np.argwhere(self.board == target_square)[0][1])

        orig_square, target_square = target_square, orig_square
        
        if not self.is_checked(color, ignore_square, king_coords):
            status = True
        orig_square, target_square = target_square, orig_square

        return status
    #------------------------------------------------------
    @staticmethod               
    def within_bounds(x, y) -> bool:
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        else:
            return True