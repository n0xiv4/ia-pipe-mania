# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

import subprocess
from utils import * 
#

import copy
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

    def __init__(self, board, connection_board):
        self.board = board
        self.id = PipeManiaState.state_id
        self.connection_board = connection_board
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    def __init__(self, board:list):
        self.board = board
        self.size = len(board)
    
    def initial_relax(self):
        for row in range(0, self.size):
            for col in range(0, self.size):
                piece = self.get_value(row, col)
                upb, downb = self.adjacent_vertical_values(row, col)
                leftb, rightb = self.adjacent_horizontal_values(row, col)
                border = (upb, rightb, downb, leftb)

                if piece[0] != "L":
                    positions = POSITIONS
                else:
                    positions = ["H", "V"]

                if None in border:
                    x = 0
                    try_position = True
                    while try_position:
                        try_position = False
                        for i in indices(border,None):
                            if CONNECTIONS[piece][i]:
                                piece = piece[0] + positions[x]
                                try_position = True
                        x += 1
                        self.board[row][col] = piece


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

    def rotate(self, actions):
        """
        Roda uma qualquer peça para a orientação pedida,
        retornando posteriormente um novo Board.
        """
        new_board = copy.deepcopy(self.board)
        for action in actions:
            row, col, new_piece = action[0], action[1], action[2]
            new_board[row][col] = new_piece

        return Board(new_board)
    
    def print(self):
        representation = ""
        for r in range(0, self.size):
            representation += self.board[r][0]
            for c in range(1, self.size):
                representation += '\t' + self.board[r][c]
            representation = representation + '\n' if r != self.size - 1 else representation
        return representation
    
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
        subprocess.run(['python', 'visualizer.py', str(self.board)])

    def connected(self, row: int, col: int) -> int:
        """
        Verifica se uma peça está conectada a todas as peças à sua volta.
        """
        not_connected = 0
        piece = self.board[row][col]
        vertical = self.adjacent_vertical_values(row, col)
        horizontal = self.adjacent_horizontal_values(row, col)
        surroundings = (vertical[0], horizontal[1], vertical[1], horizontal[0])
        for side, p in enumerate(surroundings):
            if CONNECTIONS[piece][side] and (not p or not CONNECTIONS[p][side-2]):
                not_connected += -1 
        return not_connected

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
        
        for _ in range(1, board_size):
            line = sys.stdin.readline().strip().split('\t')
            line_input.append(line)

        return Board(line_input)

class ConnectionBoard:
    """Uma ConnectionBoard é uma board que contêm as conexões fixas
    do estado atual. Se uma peça não pode ser mais mexida, estará
    fixa no ConnectionBoard.
    """ 
    def __init__(self, board, size: int):
        self.board = board
        self.size = size

    def inside_board(self, row: int, col: int) -> bool:
        """Devolve o valor booleano que especifica se a posição
        dada faz parte do tabuleiro."""
        return -1 < row < self.size and -1 < col < self.size
    
    def get_value(self, row: int, col: int):
        """Devolve o valor na respetiva posição do tabuleiro."""
        if self.inside_board(row, col):
            return self.board[row][col]
        return None

    def confirm(self, actions):
        """Confirma uma determinada peça numa determinada posição.
        As conexões a partir dessa serão agora dadas como fixas.
        """
        for action in actions:
            self.board[action[0]][action[1]] = CONNECTIONS[action[2]]

    def confirm_with_copy(self, action):    
        new_board = copy.deepcopy(self.board)
        new_board[action[0]][action[1]] = CONNECTIONS[action[2]]

        return ConnectionBoard(new_board, self.size)

    def adjacent_connections(self, row: int, col: int) -> list:
        """Retorna o tuplo com as conexões adjacentes ao connection
        board.
        """    
        adjacent = []
        index = 0
        for position in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            border_row = row + position[0]
            border_col = col + position[1]
            if self.inside_board(border_row, border_col) and self.board[border_row][border_col] != None:
                adjacent.append(self.board[border_row][border_col][index-2])
            elif self.inside_board(border_row, border_col) == False:
                adjacent.append(False)
            else:
                adjacent.append(None)
            index += 1
        
        return adjacent

    def debug(self):
        """
        Imprime o board para fins de debugging.
        """
        for r in range(0, self.size):
            for c in range(0, self.size):
                print(self.board[r][c], end="\t")
            print()
      

class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = PipeManiaState(board, ConnectionBoard([[None for _ in range(0, board.size)] for _ in range(0, board.size)], board.size))

    def relax(self, state: PipeManiaState, actions):
        """Relaxa o problema a partir de ações únicas."""
        unique_actions = []
        for index, action in enumerate(actions):
            current_pos = (actions[index][0], actions[index][1])
            if index != 0:
                last_pos = (actions[index-1][0], actions[index-1][1])
            else:
                last_pos = None

            if index != len(actions) - 1:
                next_pos = (actions[index+1][0], actions[index+1][1])
            else:
                next_pos = None

            if last_pos != current_pos and current_pos != next_pos:
                unique_actions.append(action)
                
        state.connection_board.confirm(unique_actions)
        return unique_actions

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = []
        decided_actions = []
        board = self.initial.board
        board_size = self.initial.board.size
        
        need_relax = True 
        while need_relax == True:
            actions = []
            for row in range(0, board_size):
                for col in range(0, board_size):
                    piece = board.get_value(row, col)
                    upb, downb = board.adjacent_vertical_values(row, col)
                    leftb, rightb = board.adjacent_horizontal_values(row, col)
                    border = (upb, rightb, downb, leftb)
                    
                    if state.connection_board.get_value(row, col) != None:
                        continue

                    connection_border = state.connection_board.adjacent_connections(row, col)
                    if piece[0] != "L":
                        positions = POSITIONS
                    else:
                        positions = ["H", "V"]

                    for position in positions:
                        status = True
                        new_piece = piece[0] + position
                        for i in indices(connection_border, True):
                            if CONNECTIONS[new_piece][i] != True:
                                status = False
                        for j in indices(connection_border, False):
                            if CONNECTIONS[new_piece][j] == True:
                                status = False

                        if status == False:
                            if (position != positions[-1]):
                                continue
                            if len(actions) == 0:
                                return []
                            if actions[-1][0] != row and actions[-1][1] != col:
                                return []
                            continue

                        if new_piece[0] == "F":
                            opposite_piece = border[POSITIONS.index(new_piece[1])]
                            if opposite_piece and opposite_piece[0] == "F":
                                continue
                        
                        if new_piece[0] == "L":
                            if new_piece[1] == "H" and leftb != None and leftb[0] == "F" and rightb != None and rightb[0] == "F":
                                continue
                            if new_piece[1] == "V" and upb != None and upb[0] == "F" and downb != None and downb[0] == "F":
                                continue

                        actions.append((row, col, new_piece))
                        
            relaxed = self.relax(state, actions)
            decided_actions.extend(relaxed)
            need_relax = True if len(relaxed) != 0 else False

        if len(actions) == 0:
            return [decided_actions]

        row, col = actions[0][0], actions[0][1]
        i = 0
        diferent_actions = []
        all_actions = []
        while actions[i][0] == row and actions[i][1] == col:
            diferent_actions = copy.deepcopy(decided_actions)
            diferent_actions.append(actions[i])
            all_actions.append(diferent_actions)
            i += 1
            
        return all_actions

    def result(self, state: PipeManiaState, actions):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        return PipeManiaState(state.board.rotate(actions), state.connection_board.confirm_with_copy(actions[-1]))

    def value(self, state: PipeManiaState) -> int:
        size = state.board.size
        value = 0
        for row in range(0, size):
            for col in range(0, size):
                value += state.board.connected(row,col)
        return value

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        if (self.value(state) == 0):
           return True
        else:
            return False

if __name__ == "__main__":
    
    board = Board.parse_instance()
    problem = PipeMania(board)
    goal_node = depth_first_tree_search(problem)
    print(goal_node.state.board.print(), sep="")