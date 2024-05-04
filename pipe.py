# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 07:
# 106192 Filipe Oleacu
# 106505 Rodrigo Salgueiro

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

# SKETCH for STATES
ACTIONS = {
    "C": ("E", "D"),
    "B": ("D", "E"),
    "E": ("B", "C"),
    "D": ("C", "B"),
    "H": ("V", "V"),
    "V": ("L", "L")
}


class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    def __init__(self, board: list):
        self.board = board
        self.size = len(board)

    def inside_board(self, row: int, col: int) -> bool:
        """Devolve o valor booleano que especifica se a posição
        dada faz parte do tabuleiro."""
        return -1 < row < self.size and -1 < col < self.size

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if self.inside_board(row, col):
            return self.board[row][col]
        return None

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        above_value = None
        below_value = None
        if self.inside_board(row+1, col):
            above_value = self.board[row-1][col]
        if self.inside_board(row-1, col):
            below_value = self.board[row+1][col]
            
        return (above_value, below_value)

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        left_value = None
        right_value = None
        if self.inside_board(row, col-1):
            left_value = self.board[row][col-1]
        if self.inside_board(row, col+1):
            right_value = self.board[row][col+1]
            
        return (left_value, right_value)

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        line_input = []

        first_line = sys.stdin.readline().strip().split('\t')
        line_input.append(first_line)

        board_size = len(first_line)
        # First line has already been read
        for _ in range(1, board_size):
            line = sys.stdin.readline().strip().split('\t')
            line_input.append(line)

        return Board(line_input)

    # TODO: outros metodos da classe


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO: add more attributes (if needed)
        self.board = board

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # Depends on second letter ONLY, which specifies the orientation.
        # There are always two possible moves: counterclockwise and clockwise.
        # L piece works differently (naturally).
        
        # Não percebo o que é suposto isto retornar ?
        pass

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()
    print(board.adjacent_vertical_values(0, 0))
    print(board.adjacent_vertical_values(1, 0))
    pass
