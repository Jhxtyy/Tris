import asyncio
import pygame
from pygame.locals import *

pygame.init()

pygame.font.init()

font1 = pygame.font.Font('font/Righteous-Regular.ttf', 50)
font2 = pygame.font.Font('font/Kanit-Semibold.ttf', 25)

bg_img = pygame.image.load('img/bg.png')
bg1_img = pygame.image.load('img/bg1.png')
bg2_img = pygame.image.load('img/bg2.png')
bg3_img = pygame.image.load('img/bg3.png')
p1_img = pygame.image.load('img/p1.png')
p2_img = pygame.image.load('img/p2.png')
gd_img = pygame.image.load('img/gamedesk.png')
g_img = pygame.image.load('img/griglia.png')

width = 540
height = 960

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("TIC TAC TOE")
img_icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(img_icon)

clock = pygame.time.Clock()

run = True
paused = False

x_turn = True

board = [[None, None, None],
         [None, None, None],
         [None, None, None]]

winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                        (0, 3, 6), (1, 4, 7), (2, 5, 8),
                        (0, 4, 8), (2, 4, 6)]

def check_winner(symbol):
    for combo in winning_combinations:
        if all(board[pos // 3][pos % 3] == symbol for pos in combo):
            return True
    return False

def draw_winning_line(screen, p1, p2, p3):
    pygame.draw.line(screen, (255, 0, 0), p1, p3, 8)

gd_rect = pygame.Rect(45, 250, gd_img.get_width(), gd_img.get_height())

run, x_turn, board, paused

while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            if not paused and not check_winner("X") and not check_winner("O"):
                if gd_rect.collidepoint(event.pos):
                    row = (event.pos[1] - gd_rect.top) // (gd_rect.height // 3)
                    col = (event.pos[0] - gd_rect.left) // (gd_rect.width // 3)
                    if 0 <= row < 3 and 0 <= col < 3 and board[row][col] is None:
                        board[row][col] = "X" if x_turn else "O"
                        x_turn = not x_turn
                        if check_winner("X"):
                            paused = True
                        elif check_winner("O"):
                            paused = True
                        elif all(board[row][col] is not None for row in range(3) for col in range(3)):
                            paused = True
        elif event.type == KEYDOWN:
            if paused:
                paused = False
                board = [[None, None, None], [None, None, None], [None, None, None]]
                x_turn = True

    textsurface = font2.render(("PREMERE UN TASTO PER CONTINUARE"), True, (255, 76, 101))
    bg = screen.blit(bg_img, (-0, 0))

    if x_turn:
        overlay = bg2_img.copy()
    else:
        overlay = bg1_img.copy()

    screen.blit(overlay, (0, 0))

    cell_size = gd_img.get_width() // 3

    for row in range(3):
        for col in range(3):
            cell_left = gd_rect.left + col * cell_size
            cell_top = gd_rect.top + row * cell_size

            if board[row][col] == "X":
                screen.blit(p1_img, (cell_left + cell_size // 6, cell_top + cell_size // 6))
            elif board[row][col] == "O":
                screen.blit(p2_img, (cell_left + cell_size // 6, cell_top + cell_size // 6))

    gd = screen.blit(gd_img, (45, 250))

    if paused:
        if check_winner("X"):
            for combo in winning_combinations:
                if all(board[pos // 3][pos % 3] == "X" for pos in combo):
                    paused = True
                    break
            winner_text = font1.render("IL BLU VINCE!", True, (105, 82, 255))
            screen.blit(winner_text, (115, 120))
            overlay = bg2_img.copy()
            screen.blit(overlay, (0, 0))
            textsurface = font2.render(("PREMERE UN TASTO PER CONTINUARE"), True, (105, 82, 255))

            screen.blit(textsurface, (55, 780))

        elif check_winner("O"):
            for combo in winning_combinations:
                if all(board[pos // 3][pos % 3] == "O" for pos in combo):
                    paused = True
                    break
            winner_text1 = font1.render("IL ROSSO VINCE!", True, (255, 76, 101))
            screen.blit(winner_text1, (80, 120))
            overlay = bg1_img.copy()
            screen.blit(overlay, (0, 0))
            textsurface = font2.render(("PREMERE UN TASTO PER CONTINUARE"), True, (255, 76, 101))

            screen.blit(textsurface, (55, 780))

        elif all(board[row][col] is not None for row in range(3) for col in range(3)):
            winner_text2 = font1.render("PAREGGIO!", True, (13, 204, 128))
            screen.blit(winner_text2, (140, 120))
            overlay = bg3_img.copy()
            screen.blit(overlay, (0, 0))
            textsurface = font2.render(("PREMERE UN TASTO PER CONTINUARE"), True, (13, 204, 128))

            screen.blit(textsurface, (55, 780))

    pygame.display.update()
    clock.tick(200)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    pygame.quit()