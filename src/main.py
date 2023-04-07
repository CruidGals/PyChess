import pygame
from board import *
from gamelogic import GameLogic
from fendecoder import FenDecoder
from graphics import Graphics
from sys import exit

class Game:
    def __init__(self):
        self.fen_str = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        #Test Cases
        #self.fen_str = 'rnbqkbnr/pppppppp/8/8/8/4p3/PPPP1PPP/RNBQKBNR w KQkq - 0 1'
        #self.fen_str = 'rnbqkbnr/pppppppp/8/8/8/rP1r1Prr/3PK3/RNB2BNR w KQkq - 0 1'
        #self.fen_str = '8/8/2P3p1/8/4b3/8/2p3P1/8 w KQkq - 0 1'
        #self.fen_str = '8/8/4p3/8/1P2r2p/8/4pn2/8 w KQkq - 0 1'

        self.fen_decoder = FenDecoder(self.fen_str)
        self.board = Board(FenDecoder.piece_placement)
        self.logic = GameLogic(self.board.board)
        self.graphics = Graphics(self.board.board)

        self.selected_square = None
        self.held_piece = None
        self.movable_squares = []

        #for click moving
        self.previous_square = None
    
    def select_piece(self, pos):
        square = ([sq for sq in self.logic.board.ravel() if sq.rect.collidepoint(pos)])[0]
        if square in self.movable_squares:
            self.release_piece(pos)
        elif square.attached_piece != None:
            self.selected_square = square
            self.held_piece = square.attached_piece

            #Allows movement of opposite color piece, but won't do anything
            self.movable_squares = self.logic.piece_moves(square, self.board.retrieve_square(FenDecoder.en_passant_square)) if FenDecoder.side_to_move == self.held_piece.color else []
        
        self.graphics.select_piece_gfx(square)

    def drag_piece(self, pos):
        if self.held_piece == None: return
        self.held_piece.pos.x = pos[0] - (Board.CELL_SIZE // 2)
        self.held_piece.pos.y = pos[1] - (Board.CELL_SIZE // 2)
        self.held_piece.update_rect()

    def release_piece(self, pos):
        if self.selected_square == None: return
        if self.held_piece == None: self.held_piece = self.selected_square.attached_piece

        game_over = False
        square = ([sq for sq in self.board.board.ravel() if sq.rect.collidepoint(pos)])[0]

        if square in self.movable_squares:
            if square.attached_piece != None:
                FenDecoder.half_move_counter = 0
            
            self.graphics.move_piece_gfx(self.selected_square, square)
            self.logic.update_castling_ability(self.selected_square) #If a king or rook move is made, checks to see if it affects castling ability
            
            #Castling function; Swaps the rooks (rook gets sent from original position to new position):
            #If king moves away from original square or castles, it loses all of its castling ability
            if self.held_piece.piece == Piece.KING:
                if self.held_piece.color == Piece.WHITE and self.selected_square.notation == 'e1':
                    if square.notation == 'g1':
                        self.board.swap_pieces(self.board.board[7][7], self.board.board[7][5])
                    elif square.notation == 'c1':
                        self.board.swap_pieces(self.board.board[7][0], self.board.board[7][3])

                if self.held_piece.color == Piece.BLACK and self.selected_square.notation == 'e8':
                    if square.notation == 'g8':
                        self.board.swap_pieces(self.board.board[0][7], self.board.board[0][5])
                    elif square.notation == 'c8':
                        self.board.swap_pieces(self.board.board[0][0], self.board.board[0][3])
                
                self.logic.update_king_square(self.held_piece.color, square) #Need to update the position of the square for GameLogic

            #Handles Pawn Queening and En Passant functions
            if self.held_piece.piece == Piece.PAWN:
                FenDecoder.half_move_counter = 0

                #Queening
                if (self.held_piece.color == Piece.WHITE and square in self.board.board[0]) or (self.held_piece.color == Piece.BLACK and square in self.board.board[7]):
                    self.held_piece.piece = Piece.QUEEN
                    self.held_piece.update_image()
                
                #Checks if a pawn does en passant: (If enpassant square is on file 6, white must take. If on 3, black must take)
                if square.notation == FenDecoder.en_passant_square:
                    target_square = None
                    if FenDecoder.en_passant_square[1] == '6' and self.held_piece.color == Piece.WHITE:
                        target_square = self.board.retrieve_square('{}5'.format(FenDecoder.en_passant_square[0]))
                    elif FenDecoder.en_passant_square[1] == '3' and self.held_piece.color == Piece.BLACK:
                        target_square = self.board.retrieve_square('{}4'.format(FenDecoder.en_passant_square[0]))

                    self.board.pieces_list.remove(target_square.attached_piece)
                    target_square.attached_piece = None
                
                #Checks for an en passant square: if pawn double moves, make the enpassant square the square below the pawn
                self.logic.update_en_passant_square(self.held_piece.color, self.selected_square, square)             
            elif FenDecoder.en_passant_square != '-':
                FenDecoder.en_passant_square = '-'
            
            if FenDecoder.side_to_move == Piece.BLACK: FenDecoder.full_move_counter += 1

            self.board.pieces_list.remove(square.attached_piece)
            self.board.swap_pieces(self.selected_square, square)

            #Handles checkmate function (Just closes the game at the moment)
            game_over = self.logic.is_checkmate(FenDecoder.side_to_move)
            FenDecoder.side_to_move = Piece.opposite_color(FenDecoder.side_to_move)

            self.selected_square = None
            self.movable_squares = []
            self.previous_square = None
        else:
            self.board.swap_pieces(self.selected_square, self.selected_square)

            if self.previous_square == square and self.previous_square != self.graphics.new_square:
                self.selected_square.selected = False
                self.selected_square = None
                self.movable_squares = []
                self.previous_square = None
            else:
                self.previous_square = self.selected_square

        self.held_piece = None
        
        return game_over
    
    def draw_elements(self, screen):
        self.board.draw_board(screen)
        self.board.draw_pieces(screen)

def main():
    pygame.init()

    #Chess board has 8 squares. 1 & a start at bottom left rook, 8 & h at top right black rook
    cell_size = Board.CELL_SIZE
    screen = pygame.display.set_mode((8 * cell_size, 8 * cell_size))
    pygame.display.set_caption('Chess')
    clock = pygame.time.Clock()

    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.select_piece(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONUP:
                game_over = game.release_piece(pygame.mouse.get_pos())
                if game_over:
                    running = False
            if pygame.mouse.get_pressed()[0]:
                game.drag_piece(pygame.mouse.get_pos())
        
        screen.fill('Grey')
        game.draw_elements(screen)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()