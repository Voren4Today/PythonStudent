import sys
import copy
import random
import time

winning_sets = ({0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6},
                {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6})
coor_map = {(1, 3): 0, (2, 3): 1, (3, 3): 2,
            (1, 2): 3, (2, 2): 4, (3, 2): 5,
            (1, 1): 6, (2, 1): 7, (3, 1): 8}
players = ('user', 'easy', 'medium', 'hard')


def parsing_cmd(inp_str):
    global p1, p2, players
    if inp_str == 'exit':
        return 'exit'
    else:  # not 'exit' command
        try:
            cmd1, p1, p2 = inp_str.split()
            if cmd1 != 'start':
                print('Bad command')
                return 'reenter'
            elif p1 not in players or p2 not in players:
                print('Bad command')
                return 'reenter'
            else:
                return 'start'
        except ValueError:
            print('Bad command')
            return 'reenter'


def reset_game_field():
    global available_moves, x_loc, o_loc, game_pos, game_condi, latest_move
    available_moves = {0, 1, 2, 3, 4, 5, 6, 7, 8}
    x_loc = set()
    o_loc = set()
    game_pos = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    latest_move = ''
    game_condi = ''


def move_invalid():
    global game_pos, coor_map, latest_move, current_XO
    try:
        x_coor, y_coor = input('Enter the coordinates: ').split()
        try:
            x_coor = int(x_coor)
            y_coor = int(y_coor)
        except ValueError:
            print('You should enter numbers!')
            return True
    except ValueError:
        print('You should enter numbers!')
        return True
    try:
        latest_move = coor_map[(x_coor, y_coor)]
        if game_pos[latest_move] == ' ':  # allowed location
            game_pos[latest_move] = current_XO
            return False  # only way to return False
        else:
            print('This cell is occupied! Choose another one!')
            return True
    except KeyError:
        print('Coordinates should be from 1 to 3!')
        return True


def draw_board(to_draw):
    global x_loc, o_loc, available_moves
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
    available_moves -= (x_loc | o_loc)
    return


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


def test_score(XO, eval_x_loc, eval_o_loc):
    condi = game_status(eval_x_loc, eval_o_loc)
    if condi != '':
        if condi == 'D':
            return 0
        else:
            return 256 if XO == current_XO else -256
    else:
        XO_flip = 'X' if XO == 'O' else 'O'
        score_holder = -256 if XO_flip == current_XO else 256
        for move in available_moves - eval_o_loc - eval_x_loc:
            added_to_o = {move} if XO_flip == 'O' else {}
            added_to_x = {move} if XO_flip == 'X' else {}
            score = test_score(XO_flip, eval_x_loc.union(added_to_x),
                               eval_o_loc.union(added_to_o))/2
            if XO_flip == current_XO:  # keeping max score
                if score > score_holder:
                    score_holder = copy.copy(score)
            else:  # evaluating opponents' move. keep the min score
                if score < score_holder:
                    score_holder = copy.copy(score)
        return score_holder


def computer_play(level):
    global current_XO, o_loc, x_loc, latest_move, available_moves
    latest_move = ''
    best_move = ''
    if level == 'hard':
        best_score = -256
        for move in available_moves:
            added_to_x = {move} if current_XO == 'X' else {}
            added_to_o = {move} if current_XO == 'O' else {}
            eval_score = test_score(current_XO, x_loc.union(added_to_x),
                                    o_loc.union(added_to_o))/2
            if eval_score > best_score:  # best outcome so far
                best_move = move
                best_score = copy.copy(eval_score)
        if best_move != '':  # has some idea on the next move
            latest_move = copy.copy(best_move)
    if level == 'medium' or latest_move == '':
        for move in available_moves:
            if one_move_to_win(current_XO, move):
                latest_move = move
                break
        if latest_move == '':  # prevent losing in one move
            the_other_player = 'X' if current_XO == 'O' else 'O'
            for move in available_moves:
                if one_move_to_win(the_other_player, move):
                    latest_move = move
    if level == 'easy' or latest_move == '':  # random play
        latest_move = random.sample(available_moves, 1)[0]
    print(f'Making move level "{current_p}"')
    game_pos[latest_move] = current_XO
    if current_XO == 'O':
        o_loc = o_loc | {latest_move}
    else:
        x_loc = x_loc | {latest_move}


def one_move_to_win(p, m):
    if p == 'X':
        for lucky_set in winning_sets:
            if lucky_set.issubset(x_loc | {m}):
                return True
    else:  # current_p is O
        for lucky_set in winning_sets:
            if lucky_set.issubset(o_loc | {m}):
                return True


def switch_player():
    global current_XO, current_p
    current_XO = copy.copy('O' if current_XO == 'X' else 'X')
    current_p = copy.copy(p1 if current_p == p2 else p2)


game_cmd = parsing_cmd(input('Input command: '))
if game_cmd == 'exit':
    exit(0)
while game_cmd != 'exit':
    if game_cmd == 'start':
        reset_game_field()
        random.seed(time.time())
        current_p = copy.copy(p1)
        current_XO = 'X'
        draw_board(game_pos)
        while game_condi == '':
            if current_p == 'user':
                while move_invalid():
                    pass  # looping back for another move
            else:
                computer_play(current_p)
            draw_board(game_pos)
            game_condi = game_status(x_loc, o_loc)
            if game_condi != '':  # game decided
                if game_condi == 'D':
                    print('Draw')
                else:
                    print(f'{game_condi} wins')
            switch_player()
    game_cmd = parsing_cmd(input('Input command: '))
sys.exit(0)
