import pygame
import sys
from ChessBoard import *
from Renderer import *

pygame.init()
pygame.display.set_caption("Ancient Chess")
chess_board.setup_board()
renderer = Renderer(screen, chess_board)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            renderer.handle_click(pos)
    pygame.time.Clock().tick(15)
    screen.fill((0, 0, 0))
    renderer.draw_board()
    renderer.draw_pieces()
    if renderer.whiteWin or renderer.blackWin:
        if renderer.whiteWin:
            renderer.winner('Белые')
        else:
            renderer.winner('Черные')
        running = False
    renderer.pawnTransform()
    pygame.display.flip()

pygame.quit()
sys.exit()