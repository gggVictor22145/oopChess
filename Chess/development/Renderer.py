import pygame
from ChessBoard import *

WIDTH: int = 800
HEIGHT: int = 800
SQUARE_SIZE: int = WIDTH // 8

class Renderer:
    """
    Класс, отвечающий за визуализацию шахматной доски и фигур, а также за обработку взаимодействия с пользователем.
    """
    def __init__(self, screen, board):
        """
        Инициализация рендера.

        :param screen: Поверхность Pygame для отображения.
        :param board: Экземпляр класса ChessBoard.
        """
        self.screen = screen
        self.board = board.board
        self.selected_piece = None
        self.piece_images = self.load_images()
        self.valid_moves = []
        self.turn = board.turn
        self.whiteWin: bool = False
        self.blackWin: bool = False

    def draw_board(self):
        """
        Отрисовка шахматной доски.
        """
        for row in range(8):
            for col in range(8):
                color = (255, 255, 255) if (row + col) % 2 == 0 else (125, 135, 150)
                pygame.draw.rect(self.screen, color,
                                 (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def load_images(self):
        """
        Загрузка изображений для всех шахматных фигур.

        :return: Словарь, связывающий названия фигур с их изображениями Pygame.
        """
        pieces = {
            'white_pawn': pygame.image.load('pictures/wp.gif'),
            'black_pawn': pygame.image.load('pictures/bp.gif'),
            'white_rook': pygame.image.load('pictures/wr.gif'),
            'black_rook': pygame.image.load('pictures/br.gif'),
            'white_knight': pygame.image.load('pictures/wn.gif'),
            'black_knight': pygame.image.load('pictures/bn.gif'),
            'white_bishop': pygame.image.load('pictures/wb.gif'),
            'black_bishop': pygame.image.load('pictures/bb.gif'),
            'white_queen': pygame.image.load('pictures/wq.gif'),
            'black_queen': pygame.image.load('pictures/bq.gif'),
            'white_king': pygame.image.load('pictures/wk.gif'),
            'black_king': pygame.image.load('pictures/bk.gif'),
        }
        return pieces

    def draw_pieces(self):
        """
        Отрисовка всех шахматных фигур на доске.
        """
        self.blackWin = True
        self.whiteWin = True
        for row in range(8):
            for col in range(8):
                piece = self.board[col][row]
                if not isinstance(piece, EmptyField):
                    if isinstance(piece, Pawn):
                        image_key = f"{piece.color}_pawn"
                    elif isinstance(piece, Rook):
                        image_key = f"{piece.color}_rook"
                    elif isinstance(piece, Knight):
                        image_key = f"{piece.color}_knight"
                    elif isinstance(piece, Bishop):
                        image_key = f"{piece.color}_bishop"
                    elif isinstance(piece, Queen):
                        image_key = f"{piece.color}_queen"
                    elif isinstance(piece, King):
                        image_key = f"{piece.color}_king"
                        if piece.color == 'white':
                            self.blackWin = False
                        else:
                            self.whiteWin = False

                    image = self.piece_images[image_key]
                    new_size = (image.get_width() * 3, image.get_height() * 3)
                    scaled_image = pygame.transform.scale(image, new_size)
                    self.screen.blit(scaled_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def pawnTransform(self):
        """
        Превращение пешки в ферзя при достижении противоположного конца доски.
        """
        for row in range(8):
            if isinstance(self.board[row][0], Pawn) and self.board[row][0].color == 'white':
                self.board[row][0] = Queen('white', row, 0)
            if isinstance(self.board[row][7], Pawn) and self.board[row][7].color == 'black':
                self.board[row][0] = Queen('black', row, 7)

    def winner(self, winner: str):
        """
        Отображение победителя на экране.

        :param winner: Цвет победившей стороны ('Белые' или 'Черные').
        """
        font = pygame.font.Font(None, 74)
        text = font.render(f'{winner} победили!', True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 300))
        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)
        pygame.display.flip()

        pygame.time.delay(1500)

    def handle_click(self, pos):
        """
        Обработка событий щелчка мыши.

        :param pos: Позиция щелчка мыши.
        """
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE

        if self.selected_piece is None:
            if not isinstance(self.board[col][row], EmptyField):
                if self.board[col][row].color == 'white' and self.turn % 2 == 0:
                    self.selected_piece = self.board[col][row]
                if self.board[col][row].color == 'black' and self.turn % 2 == 1:
                    self.selected_piece = self.board[col][row]
                if self.selected_piece is not None:
                    self.valid_moves = self.selected_piece.takeAttackFields(col, row)
        else:
            if [col, row] in self.valid_moves:
                pr_x = self.selected_piece.x
                pr_y = self.selected_piece.y
                self.selected_piece.x = col
                self.selected_piece.y = row
                self.board[pr_x][pr_y], self.board[col][row] = self.board[col][row], self.board[pr_x][pr_y]
                if not isinstance(self.board[pr_x][pr_y], EmptyField):
                    self.board[pr_x][pr_y] = EmptyField(pr_x, pr_y)
                self.selected_piece = None
                self.valid_moves = []
                self.turn += 1
            elif not isinstance(self.board[col][row], EmptyField):
                if self.board[col][row].color == 'white' and self.turn % 2 == 0:
                    self.selected_piece = self.board[col][row]
                if self.board[col][row].color == 'black' and self.turn % 2 == 1:
                    self.selected_piece = self.board[col][row]
                if self.selected_piece is not None:
                    self.valid_moves = self.selected_piece.takeAttackFields(col, row)

screen = pygame.display.set_mode((WIDTH, HEIGHT))