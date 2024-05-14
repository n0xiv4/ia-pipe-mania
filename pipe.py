# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 07:
# 106192 Filipe Oleacu
# 106505 Rodrigo Salgueiro

# TODO: REMOVER IMPORT SUBPROCESS NO FIM!!!
import subprocess
#

import sys
import copy
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

UP = "C"
RIGHT = "D"
DOWN = "B"
LEFT = "E"
HRZ = "H"
VRT = "V"

POSITIONS = (UP, RIGHT, DOWN, LEFT)

CONNECTIONS = {
    "FC": (True, False, False, False),
    "FD": (False, True, False, False),
    "FB": (False, False, True, False),
    "FE": (False, False, False, True),
    "BC": (True, True, False, True),
    "BD": (True, True, True, False),
    "BB": (False, True, True, True),
    "BE": (True, False, True, True),
    "VC": (True, False, False, True),
    "VD": (True, True, False, False),
    "VB": (False, True, True, False),
    "VE": (False, False, True, True),
    "LH": (False, True, False, True),
    "LV": (True, False, True, False)
}

def indices(lst, item):
    return [i for i, x in enumerate(lst) if x == item]


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
        if self.inside_board(row-1, col):
            above_value = self.board[row-1][col]
        if self.inside_board(row+1, col):
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
    
    def connected(self, row: int, col: int) -> bool:
        """
        Verifica se uma peça está conectada a todas as peças à sua volta.
        """
        piece = self.board[row][col]
        vertical = self.adjacent_vertical_values(row, col)
        horizontal = self.adjacent_horizontal_values(row, col)
        surroundings = (vertical[0], horizontal[1], vertical[1], horizontal[0])
        # Checks surrondings of the current piece
        for side, p in enumerate(surroundings):
            # If the current piece has a connection on this side, and the other 
            # piece doesn't, it's not connected
            # (side-2 means the opposite side)
            if CONNECTIONS[piece][side] and (not p or not CONNECTIONS[p][side-2]):
                return False
        return True
    
    def rotate(self, action):
        """
        Roda uma qualquer peça para a orientação pedida,
        retornando posteriormente um novo Board.
        """
        row, col, orientation = action[0], action[1], action[2]
        new_board = copy.deepcopy(self.board)
        old_piece = new_board[row][col]
        new_piece = old_piece[0] + orientation
        new_board[row][col] = new_piece

        return Board(new_board)
    
    def debug(self):
        """
        Imprime o board para fins de debugging.
        """
        for r in range(0, self.size):
            for c in range(0, self.size):
                print(self.board[r][c], end="\t")
            print()
            
    def show(self):
        """
        Mostra o board num formato de imagem.
        """
        subprocess.run(['python3', 'visualizer.py', str(self.board)])

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
        
        actions = []

        board = state.board
        board_size = state.board.size
        for row in range(0, board_size):
            for col in range(0, board_size):
                print(row, col)
                # DESCOBRIR FRONTEIRA DE CADA PEÇA, ANTES DE TUDO...
                piece = board.get_value(row, col)
                upb, downb = board.adjacent_vertical_values(row, col)
                leftb, rightb = board.adjacent_horizontal_values(row, col)
                border = (upb, rightb, downb, leftb)

                # Diferentes hipóteses de peças nessa posição
                if piece[0] != "L":
                    positions = POSITIONS
                else:
                    positions = ["H", "V"]

                for position in positions:
                    print((row, col, piece, position))
                    if position == piece[1]:
                        # ignore own position
                        continue

                    status = True
                    new_piece = piece[0] + position
                    if None in border:
                        for i in indices(border, None):
                            if CONNECTIONS[new_piece][i] and (row, col, position) not in actions:
                                status = False

                    if status:
                        # Case if there are two F's next to each other
                        if new_piece[0] == "F":
                            opposite_piece = border[POSITIONS.index(new_piece[1])]
                            if opposite_piece and opposite_piece[0] == "F":
                                continue
                        
                        actions.append((row, col, position))
        
        return actions

    def result(self, state: PipeManiaState, action: tuple) -> PipeManiaState:
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        return PipeManiaState(state.board.rotate(action))

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
    problem = PipeMania(board)
    initial_state = PipeManiaState(board)
    
    # TESTES
    initial_state.board.debug()
    initial_state.board.show()
    print(problem.actions(initial_state))
    pass
