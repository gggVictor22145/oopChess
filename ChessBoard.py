import abc

class ChessPiece(abc.ABC):
    """
    Абстрактный базовый класс, представляющий шахматную фигуру.
    """
    def __init__(self, color: str, x: int, y: int):
        """
        Инициализация шахматной фигуры.

        :param color: Цвет фигуры ('white', 'black' или 'empty').
        :param x: Координата x (столбец) на доске.
        :param y: Координата y (строка) на доске.
        """
        self.x: int = x
        self.y: int = y
        self.color: str = color
        self.paths = None
        self.alive: bool = True

    def takeAttackFields(self, x: int, y: int):
        """
        Вычисляет все возможные поля для атаки фигуры с позиции (x, y).

        :param x: Координата x (столбец) фигуры.
        :param y: Координата y (строка) фигуры.
        :return: Список доступных позиций для атаки в формате [x, y].
        """
        attack_fields = []
        for i in range(len(self.paths)):
            if not self.canRepeatMoves:
                new_x = x + self.paths[i][0]
                new_y = y + self.paths[i][1]
                if 0 <= new_x <= 7 and 0 <= new_y <= 7 and chess_board.board[new_x][new_y].color != self.color:
                    attack_fields.append([new_x, new_y])
                continue
            k = 1
            while True:
                new_x = x + k * self.paths[i][0]
                new_y = y + k * self.paths[i][1]
                if 0 <= new_x <= 7 and 0 <= new_y <= 7 and chess_board.board[new_x][new_y].color == 'empty':
                    attack_fields.append([new_x, new_y])
                    k += 1
                elif 0 <= new_x <= 7 and 0 <= new_y <= 7 and chess_board.board[new_x][new_y].color != self.color:
                    attack_fields.append([new_x, new_y])
                    break
                else:
                    break
        return attack_fields

class EmptyField(ChessPiece):
    """
    Класс, представляющий пустое поле на шахматной доске.
    """
    def __init__(self, x: int, y: int):
        """
        Инициализация пустого поля.

        :param x: Координата x (столбец) на доске.
        :param y: Координата y (строка) на доске.
        """
        super().__init__('empty', x, y)
        self.color = 'empty'
        self.paths = [[0, 0]]
        self.canRepeatMoves: bool = False

class Pawn(ChessPiece):
    """
    Класс, представляющий пешку.
    """
    def __init__(self, color: str, x: int, y: int):
        """
        Инициализация пешки.

        :param color: Цвет пешки ('white' или 'black').
        :param x: Координата x (столбец) на доске.
        :param y: Координата y (строка) на доске.
        """
        super().__init__(color, x, y)
        self.canRepeatMoves: bool = False
        self.paths = [[0, -1]] if color == "white" else [[0, 1]]

    def takeAttackFields(self, x: int, y: int):
        """
        Вычисляет все возможные поля для атаки пешки с позиции (x, y).

        :param x: Координата x (столбец) пешки.
        :param y: Координата y (строка) пешки.
        :return: Список доступных позиций для атаки в формате [x, y].
        """
        attack_fields = []
        new_x = x + self.paths[0][0]
        new_y = y + self.paths[0][1]
        if 0 <= new_x <= 7 and 0 <= new_y <= 7 and chess_board.board[new_x][new_y].color == 'empty':
            attack_fields.append([new_x, new_y])
        if self.color == 'white' and y == 6:
            attack_fields.append([x, 4])
        if self.color == 'black' and y == 1:
            attack_fields.append([x, 3])

        for direct in [1, -1]:
            if 0 <= x + direct <= 7 and chess_board.board[x+direct][y+self.paths[0][1]].color != 'empty' and chess_board.board[x+direct][y+self.paths[0][1]] != self.color:
                attack_fields.append([x+direct, y+self.paths[0][1]])
        return attack_fields

class Rook(ChessPiece):
    """
    Класс, представляющий ладью.
    """
    def __init__(self, color: str, x: int, y: int):
        """
        Инициализация ладьи.

        :param color: Цвет ладьи ('white' или 'black').
        :param x: Координата x (столбец) на доске.
        :param y: Координата y (строка) на доске.
        """
        super().__init__(color, x, y)
        self.paths = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        self.canRepeatMoves: bool = True
        self.moved: bool = False

class Knight(ChessPiece):
    """
    Класс, представляющий коня.
    """
    def __init__(self, color: str, x: int, y: int):
        """
        Инициализация коня.

        :param color: Цвет коня ('white' или 'black').
        :param x: Координата x (столбец) на доске.
        :param y: Координата y (строка) на доске.
        """
        super().__init__(color, x, y)
        self.paths = [[i, j] for i in [2, -2] for j in [1, -1]] + [[i, j] for j in [2, -2] for i in [1, -1]]
        self.canRepeatMoves: bool = False

class Bishop(ChessPiece):
    """
    Класс, представляющий слона.
    """
    def __init__(self, color: str, x: int, y: int):
        """
        Инициализация слона.

        :param color: Цвет слона ('white' или 'black').
        :param x: Координата x (столбец) на доске.
        :param y: Координата y (строка) на доске.
        """
        super().__init__(color, x, y)
        self.paths = [[i, j] for i in [1, -1] for j in [1, -1]]
        self.canRepeatMoves: bool = True

class Queen(ChessPiece):
    """
    Класс, представляющий ферзя.
    """
    def __init__(self, color: str, x: int, y: int):
        """
        Инициализация ферзя.

        :param color: Цвет ферзя ('white' или 'black').
        :param x: Координата x (столбец) на доске.
        :param y: Координата y (строка) на доске.
        """
        super().__init__(color, x, y)
        self.paths = [[i, j] for i in [1, -1] for j in [1, -1]] + [[1, 0], [-1, 0], [0, 1], [0, -1]]
        self.canRepeatMoves: bool = True

class King(ChessPiece):
    """
    Класс, представляющий короля.
    """
    def __init__(self, color: str, x: int, y: int):
        """
        Инициализация короля.

        :param color: Цвет короля ('white' или 'black').
        :param x: Координата x (столбец) на доске.
        :param y: Координата y (строка) на доске.
        """
        super().__init__(color, x, y)
        self.paths = [[i, j] for i in [1, -1] for j in [1, -1]] + [[1, 0], [-1, 0], [0, 1], [0, -1]]
        self.canRepeatMoves: bool = False

class ChessBoard:
    """
    Класс, представляющий шахматную доску и управляющий состоянием игры.
    """
    def __new__(cls):
        instance = super().__new__(cls)
        instance.board = [[EmptyField(x, y) for x in range(8)] for y in range(8)]
        instance.setup_board()
        return instance

    def __init__(self):
        """
        Инициализация шахматной доски.
        """
        self.turn: int = 0

    def setup_board(self):
        """
        Устанавливает начальные позиции фигур на доске.
        """
        for i in range(8):
            self.board[i][1] = Pawn('black', i, 1)
            self.board[i][6] = Pawn('white', i, 6)

        pieces_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i in range(8):
            self.board[i][0] = pieces_order[i]('black', i, 0)
            self.board[i][7] = pieces_order[i]('white', i, 7)
            
chess_board = ChessBoard()