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

        self.held_piece = None
    
    def select_piece(self, pos):
        piece = ([p for p in self.board.pieces.ravel() if p.rect.collidepoint(pos)])[0]
        if piece.piece != Piece.NO_PIECE: self.held_piece = piece
    
    def drag_piece(self, pos):
        if self.held_piece == None: return
        self.held_piece.pos.x = pos[0] - (Board.CELL_SIZE // 2)
        self.held_piece.pos.y = pos[1] - (Board.CELL_SIZE // 2)

    def release_piece(self, pos):
        #To-DO: if carrying piece, drop it at the desiired location
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