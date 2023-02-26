import pygame
from board import Board, Square
from sys import exit

class GameLogic:
    def __init__(self):
        self.board = Board()
    
    def draw_elements(self, screen):
        self.board.draw_board(screen)

def main():
    pygame.init()
    game = GameLogic()

    #Chess board has 8 squares. 1 & a start at bottom left rook, 8 & h at top right black rook
    cell_size = Board.CELL_SIZE
    screen = pygame.display.set_mode((8 * cell_size, 8 * cell_size))
    pygame.display.set_caption('Chess')
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        screen.fill('Beige')
        game.draw_elements(screen)

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()