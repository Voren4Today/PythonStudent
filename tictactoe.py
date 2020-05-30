import sys
import copy
import random
import time

winning_sets = ({0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6},
                {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6})


def parsing_cmd(inp_str):
    players = ('user', 'easy', 'medium', 'hard')
    if inp_str == 'exit':
        return ['exit']
    else:  # not 'exit' command
        try:
            cmd1, p1, p2 = inp_str.split()
            if cmd1 != 'start':
                print('Bad command')
                return ['reenter']
            elif p1 not in players or p2 not in players:
                print('Bad command')
                return ['reenter']
            else:
                return ['start', p1, p2]
        except ValueError:
            print('Bad command')
            return ['reenter']


def reset_game_field():
    global available_moves, x_loc, o_loc, game_pos, game_condi, latest_move
    available_moves = {m for m in range(9)}
    x_loc = set()
    o_loc = set()
    game_pos = [' ']*9
    latest_move = ''
    game_condi = ''


def move_invalid(g_pos, c_xo):
    coor_map = {(1, 3): 0, (2, 3): 1, (3, 3): 2,
            (1, 2): 3, (2, 2): 4, (3, 2): 5,
            (1, 1): 6, (2, 1): 7, (3, 1): 8}
    try:
        x_coor, y_coor = input('Enter the coordinates: ').split()
        x_coor = int(x_coor)
        y_coor = int(y_coor)
    except ValueError:
        print('You should enter numbers!')
        return ['Bad', '', '']
    try:
        l_move = coor_map[(x_coor, y_coor)]
        if g_pos[l_move] == ' ': # allowed location
            g_pos[l_move] = c_xo
            return ['Valid', l_move, g_pos]  # updated moves returned
        else:
            print('This cell is occupied! Choose another one!')
            return ['Bad', '', g_pos]
    except KeyError:
        print('Coordinates should be from 1 to 3!')
        return ['Bad', '', g_pos]


def draw_board(to_draw):
    for ii in range(9):
        if to_draw[ii] == 'X':
            x_loc.add(ii)
        elif to_draw[ii] == 'O':
            o_loc.add(ii)
    print('---------')
    for ii in range(0, 3):
        print(f'| {to_draw[ii * 3]} '
              f'{to_draw[ii * 3 + 1]} {to_draw[ii * 3 + 2]} |')
    print('---------')


def game_status(temp_x_loc, temp_o_loc):
    x_win_flag = 0
    o_win_flag = 0
    for lucky_set in winning_sets:
        if lucky_set.issubset(temp_x_loc):
            x_win_flag += 1
        if lucky_set.issubset(temp_o_loc):
            o_win_flag += 1
    if x_win_flag:
        return 'X'
    elif o_win_flag:
        return 'O'
    elif len(temp_x_loc) + len(temp_o_loc) == 9:
        return 'D'
    else:
        return ''  # no result yet


def test_score(xo, eval_x_loc, eval_o_loc):
    condi = game_status(eval_x_loc, eval_o_loc)
    if condi:  #  game finished
        if condi == 'D':
            return 0
        else:  # the game has a winner
            return 256 if xo == current_xo else -256
    else:
        xo_flip = 'X' if xo == 'O' else 'O'
        score_holder = -256 if xo_flip == current_xo else 256
        for move in available_moves - eval_o_loc - eval_x_loc:
            added_to_o = {move} if xo_flip == 'O' else {}
            added_to_x = {move} if xo_flip == 'X' else {}
            score = test_score(xo_flip, eval_x_loc.union(added_to_x),
                               eval_o_loc.union(added_to_o)) / 2
            if xo_flip == current_xo:  # keeping max score
                if score > score_holder:
                    score_holder = copy.copy(score)
            else:  # evaluating opponents' move. keep the min score
                if score < score_holder:
                    score_holder = copy.copy(score)
        return score_holder


def computer_play(level):
    global current_xo, o_loc, x_loc, latest_move, available_moves
    latest_move = ''
    best_move = ''
    if level == 'hard':
        best_score = -256
        for move in available_moves:
            added_to_x = {move} if current_xo == 'X' else {}
            added_to_o = {move} if current_xo == 'O' else {}
            eval_score = test_score(current_xo, x_loc.union(added_to_x),
                                    o_loc.union(added_to_o)) / 2
            if eval_score > best_score:  # best outcome so far
                best_move = move
                best_score = copy.copy(eval_score)
        if best_move != '':  # has some idea on the next move
            latest_move = copy.copy(best_move)
    if level == 'medium' or latest_move == '':
        for move in available_moves:
            if one_move_to_win(current_xo, move):
                latest_move = move
                break
        if latest_move == '':  # prevent losing in one move
            the_other_player = 'X' if current_xo == 'O' else 'O'
            for move in available_moves:
                if one_move_to_win(the_other_player, move):
                    latest_move = move
    if level == 'easy' or latest_move == '':  # random play
        latest_move = random.sample(available_moves, 1)[0]
    print(f'Making move level "{current_p}"')
    game_pos[latest_move] = current_xo
    if current_xo == 'O':
        o_loc = o_loc | {latest_move}
    else:
        x_loc = x_loc | {latest_move}


def one_move_to_win(p, m):
    if p == 'X':
        for lucky_set in winning_sets:
            if lucky_set.issubset(x_loc | {m}):
                return True
        return False
    else:  # current_p is O
        for lucky_set in winning_sets:
            if lucky_set.issubset(o_loc | {m}):
                return True
        return False


def switch_player(c_xo, c_p):
    c_xo = copy.copy('O' if c_xo == 'X' else 'X')
    c_p = copy.copy(p1 if c_p == p2 else p2)
    return [c_xo, c_p]


game_cmd = parsing_cmd(input('Input command: '))
if game_cmd[0] == 'exit':
    sys.exit(0)
while game_cmd[0] != 'exit':
    if game_cmd[0] == 'start':
        [p1, p2] = game_cmd[1:]
        reset_game_field()
        random.seed(time.time())
        current_p = copy.copy(p1)
        current_xo = 'X'
        draw_board(game_pos)
        available_moves -= (x_loc | o_loc)
        while not game_condi:
            if current_p == 'user':
                while True:  # loop until valid position entered
                    [move_val, latest_move, game_pos] = \
                        move_invalid(game_pos, current_xo)
                    if move_val != 'Bad':
                        break
            else:
                computer_play(current_p)
            draw_board(game_pos)
            available_moves -= (x_loc | o_loc)
            game_condi = game_status(x_loc, o_loc)
            if game_condi != '':  # game decided
                if game_condi == 'D':
                    print('Draw')
                else:
                    print(f'{game_condi} wins')
            [current_xo, current_p] = switch_player(current_xo, current_p)
    game_cmd = parsing_cmd(input('Input command: '))
sys.exit(0)
