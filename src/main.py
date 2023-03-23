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
    
    def select_piece(self, pos):
        #probably make it select the piece itself, instead of square
        square = ([sq for sq in self.board.board.ravel() if sq.rect.collidepoint(pos)])[0]
        if square.attached_piece != None: 
            self.selected_square = square
            self.held_piece = square.attached_piece
    
    def drag_piece(self, pos):
        if self.held_piece == None: return
        self.held_piece.pos.x = pos[0] - (Board.CELL_SIZE // 2)
        self.held_piece.pos.y = pos[1] - (Board.CELL_SIZE // 2)
        self.held_piece.update_rect()

    def release_piece(self, pos):
        #TO-DO add so that the piece can be dropped onto a diff square, but only the valid squares it can go on
        self.held_piece.pos.x = self.selected_square.pos.x
        self.held_piece.pos.y = self.selected_square.pos.y
        self.held_piece.update_rect()

        self.selected_square = None
        self.held_piece = None
    
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
        
        screen.fill('Beige')
        game.draw_elements(screen)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()