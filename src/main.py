import pygame
from board import *
from gamelogic import GameLogic
from fendecoder import FenDecoder
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
        self.board = Board(self.fen_decoder.piece_placement)
        self.logic = GameLogic(self.board.board)

        self.selected_square = None
        self.held_piece = None
        self.movable_squares = []
    
    def select_piece(self, pos):
        square = ([sq for sq in self.logic.board.ravel() if sq.rect.collidepoint(pos)])[0]
        if square.attached_piece != None and square.attached_piece.color == self.fen_decoder.side_to_move:
            self.selected_square = square
            self.held_piece = square.attached_piece
            self.movable_squares = self.logic.piece_moves(square, self.fen_decoder.castling_ability)

    def drag_piece(self, pos):
        if self.held_piece == None: return
        self.held_piece.pos.x = pos[0] - (Board.CELL_SIZE // 2)
        self.held_piece.pos.y = pos[1] - (Board.CELL_SIZE // 2)
        self.held_piece.update_rect()

    def release_piece(self, pos):
        if self.selected_square == None: return

        square = ([sq for sq in self.board.board.ravel() if sq.rect.collidepoint(pos)])[0]

        if square in self.movable_squares:
            if square.attached_piece != None:
                self.fen_decoder.half_move_counter = 0

            #If rook moves, it eliminates the castling ability for that king's rook
            if self.held_piece.piece == Piece.ROOK:
                if self.selected_square.notation == 'h1' and 'K' in self.fen_decoder.castling_ability: self.fen_decoder.castling_ability = self.fen_decoder.castling_ability.replace('K', '')
                elif self.selected_square.notation == 'a1'and 'Q' in self.fen_decoder.castling_ability: self.fen_decoder.castling_ability = self.fen_decoder.castling_ability.replace('Q', '')
                elif self.selected_square.notation == 'h8'and 'k' in self.fen_decoder.castling_ability: self.fen_decoder.castling_ability = self.fen_decoder.castling_ability.replace('k', '')
                elif self.selected_square.notation == 'a8'and 'q' in self.fen_decoder.castling_ability: self.fen_decoder.castling_ability = self.fen_decoder.castling_ability.replace('q', '')
            
            #Castling function; Swaps the rooks (rook gets sent from original position to new position):
            #If king moves away from original square or castles, it loses all of its castling ability
            if self.held_piece.piece == Piece.KING:
                if self.held_piece.color == Piece.WHITE and self.selected_square.notation == 'e1':
                    if square.notation == 'g1':
                        self.board.swap_pieces(self.board.board[7][7], self.board.board[7][5])
                    elif square.notation == 'c1':
                        self.board.swap_pieces(self.board.board[7][0], self.board.board[7][3])
                    self.fen_decoder.castling_ability = self.fen_decoder.castling_ability.replace('K', '')
                    self.fen_decoder.castling_ability = self.fen_decoder.castling_ability.replace('Q', '')

                if self.held_piece.color == Piece.BLACK and self.selected_square.notation == 'e8':
                    if square.notation == 'g8':
                        self.board.swap_pieces(self.board.board[0][7], self.board.board[0][5])
                    elif square.notation == 'c8':
                        self.board.swap_pieces(self.board.board[0][0], self.board.board[0][3])
                    self.fen_decoder.castling_ability = self.fen_decoder.castling_ability.replace('k', '')
                    self.fen_decoder.castling_ability = self.fen_decoder.castling_ability.replace('q', '')

            self.board.pieces_list.remove(square.attached_piece)

            self.board.swap_pieces(self.selected_square, square)

            #self.held_piece.update_position(square)
            #square.attached_piece = self.selected_square.attached_piece
            #self.selected_square.attached_piece = None

            if square.attached_piece.piece == Piece.PAWN:
                if (square.attached_piece.color == Piece.WHITE and square in self.board.board[0]) or (square.attached_piece.color == Piece.BLACK and square in self.board.board[7]):
                    square.attached_piece.piece = Piece.QUEEN
                    square.attached_piece.update_image()
                self.fen_decoder.half_move_counter = 0

            if self.fen_decoder.side_to_move == Piece.BLACK:
                self.fen_decoder.full_move_counter

            self.fen_decoder.side_to_move = Piece.opposite_color(self.fen_decoder.side_to_move)
        else:
            self.board.swap_pieces(self.selected_square, self.selected_square)
        
        
        #for sq in self.board.board.ravel():
        #    if sq.selected and (sq != self.selected_square and sq != square): sq.selected = False

        self.selected_square = None
        self.held_piece = None
        self.movable_squares = []
    
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
                game.release_piece(pygame.mouse.get_pos())
            if pygame.mouse.get_pressed()[0]:
                game.drag_piece(pygame.mouse.get_pos())
        
        screen.fill('Grey')
        game.draw_elements(screen)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()