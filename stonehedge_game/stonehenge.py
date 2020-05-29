"""
StonehengeGame class

"""
import string
from typing import Any
from game_state import GameState
from game import Game

"""
The StonehengeState superclass.
"""

class StonehengeState(GameState):
    """
    The state of a game at a certain point in time.

    WIN - score if player is in a winning position
    LOSE - score if player is in a losing position
    DRAW - score if player is in a tied position
    p1_turn - whether it is p1's turn or not
    """
    WIN: int = 1
    LOSE: int = -1
    DRAW: int = 0
    p1_turn: bool
    hori_lst: list
    left_lst: list
    right_lst: list
    hori_result: list
    left_result: list
    right_result: list

    def __init__(self, is_p1_turn: bool, side_length: int) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.

        Precondition: the side_length entered does not exceed 5

        """
        super().__init__(is_p1_turn)
        self.side_length = side_length
        # ISSUE: what if node is more than 26 --> no need to handle side more than 5
        # construct a list of uppercase and lower case letters
        alph_lst_upper = list(string.ascii_uppercase)
        alph_lst_lower = list(string.ascii_lowercase)
        # alph_lst has a length of 52
        alph_lst = alph_lst_upper + alph_lst_lower

        # assign original value for each ley-line
        hori_result = []
        for i in range(side_length + 1):
            hori_result.append("@")
        left_result = []
        for i in range(side_length + 1):
            left_result.append("@")
        right_result = []
        for i in range(side_length + 1):
            right_result.append("@")
        self.hori_result = hori_result
        self.left_result = left_result
        self.right_result = right_result

        self.hori_lst = []
        self.left_lst = []
        self.right_lst = []

        # construct horizontal ley-lines
        n = 2
        start_index = 0
        end_index = 0
        while n <= side_length + 1:
            end_index = start_index + n
            self.hori_lst.append(alph_lst[start_index:end_index])
            start_index = end_index
            n += 1
        end_index = start_index + side_length
        self.hori_lst.append(alph_lst[start_index:end_index])

        # copy hori_lst
        hori_copy = []
        for item in self.hori_lst:
            hori_copy.append(item)

        # construct left ley-lines
        for i in range(side_length + 1):
            temp = []
            for lst in hori_copy[:len(hori_copy) - 1]:
                if len(lst) > i:
                    temp.append(lst[i])
            self.left_lst.append(temp)
        for i in range(1, side_length + 1):
            self.left_lst[i].append(hori_copy[-1][i - 1])

        # construct right ley-lines
        for i in range(-1, side_length * (-1) - 2, -1):
            temp = []
            for lst in hori_copy[:len(hori_copy) - 1]:
                if len(lst) >= i * (-1):
                    temp.append(lst[i])
            self.right_lst.append(temp)
        self.right_lst = self.right_lst[::-1]
        for i in range(side_length):
            self.right_lst[i].append(hori_copy[-1][i])

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        side = self.side_length

        hori_lst = self.hori_lst
        hori_result = self.hori_result
        left_lst = self.left_lst
        left_result = self.left_result
        right_lst = self.right_lst
        right_result = self.right_result

        total_line=''
        for i in range(2 * side + 5):
            # empty line string
            line = ''
            if i % 2 == 0:
                lineindex = int(i / 2)
                if lineindex <= side:
                    # get the first 2 left result
                    if lineindex == 0:
                        # print('first line')
                        for ia in range(3*(side+1)):
                            line += ' '
                        line += left_result[0]
                        line += '   '
                        line += left_result[1]
                    # general case of combing the results and list together
                    else:
                        if lineindex == side:
                            line += ' '
                        for ib in range(side - lineindex):
                            line += '   '
                        line += hori_result[lineindex - 1]
                        for ic in range(len(hori_lst[lineindex - 1])):
                            line += ' - '
                            line += hori_lst[lineindex - 1][ic]
                        if lineindex != side:
                            line += '   '
                            line += left_result[lineindex + 1]
                else:
                    if lineindex == side + 1:
                        # for id in range():
                        line += '   '
                        line += hori_result[side]
                        for ie in range(side):
                            line += ' - '
                            line += hori_lst[side][ie]
                        line += '   '
                        line += right_result[side]
                    else:
                        # print the last row for all other right resutls
                        # print('right results')
                        for ig in range(9):
                            line += ' '
                        for ih in range(side):
                            line += right_result[ih]
                            line += '   '
                total_line += line + '\n'
            else:
                # print stuff for the '/'
                lineindex2 = int(i / 2)
                if lineindex2 == 0:
                    for iA in range(3*side+1):
                        line += ' '
                    line += ' / '
                    line += ' '
                    line += " / "
                elif lineindex2 < side:
                    for iA in range(3 * (1 + side - lineindex2)):
                        line += ' '
                        # print('lineindex2: '+str(lineindex2)+' '+str(3*(1+side-lineindex2)))
                    for iB in range(lineindex2 + 1):
                        line += '/ \\ '
                    line += '/'
                elif lineindex2 == side:
                    #for iC in range(side+1):
                    line += '      '
                    for iD in range(side):
                        line += '\\ / '
                    line += '\\'
                elif lineindex2 == side + 1:
                    for iE in range(8):
                        line += ' '
                    for iG in range(side):
                        line += '\\   '
                total_line += line + '\n'
        return total_line

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.
        """
        result = []
        for lst in self.hori_lst:
            for item in lst:
                if item.isalpha():
                    result.append(item)

        # add nodes to result if it's not taken and its line is not taken
        # for i in range(len(self.hori_lst)):
        #     if not self.hori_result[i].isdigit():
        #         for item in self.hori_lst[i]:
        #             if not item.isdigit():
        #                 result.append(item)
        # # remove the node from result if its line has been taken
        # for i in range(len(self.left_lst)):
        #     if self.left_result[i].isdigit():
        #         for item in self.left_lst[i]:
        #             if item in result:
        #                 result.remove(item)
        # # remove the node from result if its line has been taken
        # for i in range(len(self.right_lst)):
        #     if self.right_result[i].isdigit():
        #         for item in self.right_lst[i]:
        #             if item in result:
        #                 result.remove(item)
        return result

    def get_current_player_name(self) -> str:
        """
        Return 'p1' if the current player is Player 1, and 'p2' if the current
        player is Player 2.
        """
        if self.p1_turn:
            return 'p1'
        return 'p2'

    def make_move(self, move: Any) -> 'StonehengeState':
        """
        Return the GameState that results from applying move to this GameState.

        Precondition: the move entered is valid based on the play method of GameInterface class.
        """
        if type(move) == str:
            new_state = StonehengeState(not self.p1_turn, self.side_length)
            # copy the board information from current state
            # make copy of current state information
            hori_lst_copy = []
            for lst in self.hori_lst:
                temp = []
                for item in lst:
                    temp.append(item)
                hori_lst_copy.append(temp)
            left_lst_copy = []
            for lst in self.left_lst:
                temp = []
                for item in lst:
                    temp.append(item)
                left_lst_copy.append(temp)
            right_lst_copy = []
            for lst in self.right_lst:
                temp = []
                for item in lst:
                    temp.append(item)
                right_lst_copy.append(temp)

            hori_result_copy = []
            for item in self.hori_result:
                hori_result_copy.append(item)
            left_result_copy = []
            for item in self.left_result:
                left_result_copy.append(item)
            right_result_copy = []
            for item in self.right_result:
                right_result_copy.append(item)

            new_state.hori_lst = hori_lst_copy
            new_state.hori_result = hori_result_copy
            new_state.left_lst = left_lst_copy
            new_state.left_result = left_result_copy
            new_state.right_lst = right_lst_copy
            new_state.right_result = right_result_copy
            # update the new state with str move
            # parallel nested list data structure
            lst = [new_state.hori_lst, new_state.left_lst, new_state.right_lst]
            result = [new_state.hori_result, new_state.left_result, new_state.right_result]
            # update the cell
            for i in range(len(lst)):
                for j in range(len(lst[i])):
                    for k in range(len(lst[i][j])):
                        if lst[i][j][k] == move:
                            # should use the player name of last state, so opposite names
                            if new_state.p1_turn:
                                lst[i][j][k] = "2"
                            else:
                                lst[i][j][k] = "1"
                            # update ley-line marks
                            # the ley-line may belong to a player after this move
                            p1_taken = 0
                            p2_taken = 0
                            if result[i][j] != "@":
                                continue
                            for item in lst[i][j]:
                                if item == "1":
                                    p1_taken += 1
                                if item == "2":
                                    p2_taken += 1
                            if float(p1_taken) >= len(lst[i][j]) / 2:
                                result[i][j] = "1"
                            if float(p2_taken) >= len(lst[i][j]) / 2:
                                result[i][j] = "2"
            ###### CHECK FOR SHALLOW COPY PROBLEM, IF ATTRIBUTE IS UPDATE IN NEW STATE
            return new_state

    def is_valid_move(self, move: Any) -> bool:
        """
        Return whether move is a valid move for this GameState.
        """
        return move in self.get_possible_moves()

    def __repr__(self) -> Any:
        """
        Return a representation of this state (which can be used for
        equality testing).
        """
        game_board = self.__str__() + "\n"
        current_player_info = "Is p1 the current player? " + str(self.p1_turn)
        result = game_board + current_player_info
        return result

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.
        """
        # HUYNH YOU PRICK WHY THE FUCK DO YOU MAKE US WRITE THIS SHIT EVEN IT'S NOT USED ANYWHERE
        # pick move based on this may not be optimal but better than random
        # return 1 if win immediately
        # return -1 if all states reachable will result the other player win
        # return 0 if otherwise ??? what the fuck does this mean
        # look two states forward
        pass

class StonehengeGame(Game):
    """
    Abstract class for a game to be played with two players.
    """

    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this Game, using p1_starts to find who the first player is.
        """
        side_length = int(input("Enter the side length of the board: "))
        self.current_state = StonehengeState(p1_starts, side_length)

    def get_instructions(self) -> str:
        """
        Return the instructions for this Game.
        """
        instruction = "Duck need to fill this blank _____, which I have no idea what it is #$%^&*"
        return instruction

    def is_over(self, state: StonehengeState) -> bool:
        """
        Return whether or not this game is over at state.
        """
        total_result = state.hori_result + state.left_result + state.right_result
        total_line = len(total_result)
        p1_taken = 0
        p2_taken = 0
        # all_taken = True
        for item in total_result:
            if item == '1':
                p1_taken+=1
            elif item =='2':
                p2_taken += 1
            # else:
            #     all_taken = False
        # print('p1 taken:' + str(p1_taken))
        # print('p2 taken:' + str(p2_taken))
        # print('p1_taken more than half?')
        # print(float(p1_taken) >= total_line/2)
        # print('p2_taken more than half?')
        # print(float(p2_taken) >= total_line/2)
        return float(p1_taken) >= total_line/2 or float(p2_taken) >= total_line/2

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.
        """
        total_result = self.current_state.hori_result + self.current_state.left_result + self.current_state.right_result
        total_line = len(total_result)
        p1_taken = 0
        p2_taken = 0
        for item in total_result:
            if item == '1':
                p1_taken+=1
            elif item == '2':
                p2_taken += 1
        if player == "p1":
            return float(p1_taken) >= total_line/2
        return float(p2_taken) >= total_line/2

    def str_to_move(self, str1: str) -> Any:
        """
        Return the move that string represents. If string is not a move,
        return some invalid move.
        """
        if not str1.strip().isalpha():
            return -1
        return str1.strip()


if __name__ == "__main__":
    from python_ta import check_all
    # check_all(config="a2_pyta.txt")
    # print('length of 2:')
    # st = StonehengeState(True, 2)
    # print(st.hori_lst)
    # print(st.hori_result)
    # print(st.left_lst)
    # print(st.left_result)
    # print(st.right_lst)
    # print(st.right_result)
    # print('test @ reference by change mid: ')
    # st.hori_result[1] = '1'
    # print('hori mid should be 1')
    # print(st.hori_result)
    # print('left mid should be @')
    # print(st.left_result)
    # print('length of 3:')
    # st = StonehengeState(True, 3)
    # print(st.hori_lst)
    # print(st.hori_result)
    # print(st.left_lst)
    # print(st.left_result)
    # print(st.right_lst)
    # print(st.right_result)
    # print('length of 4:')
    # st = StonehengeState(True, 4)
    # print(st.hori_lst)
    # print(st.hori_result)
    # print(st.left_lst)
    # print(st.left_result)
    # print(st.right_lst)
    # print(st.right_result)
    # print('length of 5:')
    # st = StonehengeState(True, 5)
    # print(st.hori_lst)
    # print(st.hori_result)
    # print(st.left_lst)
    # print(st.left_result)
    # print(st.right_lst)
    # print(st.right_result)

    # st = StonehengeState(True, 1)
    # print(st)
    # st = StonehengeState(True, 2)
    # print(st)
    # st = StonehengeState(True, 3)
    # print(st)
    # st = StonehengeState(True, 4)
    # print(st)
    # st = StonehengeState(True, 5)
    # print(st)

    #test states
    # st = StonehengeState(True, 2)
    # print(st)
    # print(st.get_current_player_name())
    # print(st.get_possible_moves())
    # print('move made E')
    # st1 = st.make_move('E')
    # print(st1)
    # print(st1.hori_lst)
    # print(st.hori_lst)
    # print(st1.hori_result)
    # print(st1.left_lst)
    # print(st.left_lst)
    # print(st1.left_result)
    # print(st1.right_lst)
    # print(st.right_lst)
    # print(st1.right_result)
    # print('move made A')
    # st1 = st1.make_move('A')
    # print(st1)
    # print(st1.hori_lst)
    # print(st.hori_lst)
    # print(st1.hori_result)
    # print(st1.left_lst)
    # print(st.left_lst)
    # print(st1.left_result)
    # print(st1.right_lst)
    # print(st.right_lst)
    # print(st1.right_result)
    # print('move made B')
    # st1 = st1.make_move('B')
    # print(st1)
    # print(st1.hori_lst)
    # print(st.hori_lst)
    # print(st1.hori_result)
    # print(st1.left_lst)
    # print(st.left_lst)
    # print(st1.left_result)
    # print(st1.right_lst)
    # print(st.right_lst)
    # print(st1.right_result)
    # print('move made D')
    # st1 = st1.make_move('D')
    # print(st1)
    # print(st1.hori_lst)
    # print(st.hori_lst)
    # print(st1.hori_result)
    # print(st1.left_lst)
    # print(st.left_lst)
    # print(st1.left_result)
    # print(st1.right_lst)
    # print(st.right_lst)
    # print(st1.right_result)
    # print('move made G')
    # st1 = st1.make_move('G')
    # print(st1)
    # print(st1.hori_lst)
    # print(st.hori_lst)
    # print(st1.hori_result)
    # print(st1.left_lst)
    # print(st.left_lst)
    # print(st1.left_result)
    # print(st1.right_lst)
    # print(st.right_lst)
    # print(st1.right_result)
    # print('move made F')
    # st1 = st1.make_move('F')
    # print(st1)
    # print(st1.hori_lst)
    # print(st.hori_lst)
    # print(st1.hori_result)
    # print(st1.left_lst)
    # print(st.left_lst)
    # print(st1.left_result)
    # print(st1.right_lst)
    # print(st.right_lst)
    # print(st1.right_result)
    # g = StonehengeGame(True)
    # g.current_state = st1
    # print('HERE')
    # print(g.is_over(st1))