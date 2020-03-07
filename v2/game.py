def empty_board():
    return list([0, 0, 0, 0, 0, 0, 0, 0, 0])
    
def board_to_state_hash(board):
    num = 0
    for i in range(9):
        num *= 3
        num += board[i]
    return num

def get_board_str(board):
    ret = '''
 %s | %s | %s
-----------
 %s | %s | %s
-----------
 %s | %s | %s
 ''' % tuple([' OX'[x] for x in board])
    return ret

def player_win(board, player):
    winner_lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    is_winner = False
    for i in range(len(winner_lines)):
        tmp_winner_line = winner_lines[i]
        all_this_player = True
        for j in range(len(tmp_winner_line)):
            if board[tmp_winner_line[j]] != player:
                all_this_player = False
        if all_this_player:
            is_winner = True
    return is_winner
   
def describe_board(board):
    player_one_win = player_win(board, 1)
    player_two_win = player_win(board, 2)
    num_empty_spaces = len([x for x in board if x==0])
    if not player_one_win and not player_two_win:
        if num_empty_spaces > 0:
            return 'progress'
        else:
            return 'tie'
    elif not player_one_win and player_two_win:
        return 'player_two_win'
    elif player_one_win and not player_two_win:
        return 'player_one_win'
    else:
        return 'both_win'

def get_AI_move(current_board,ai_number,all_strats):
    import random
    possible_moves = [i for i in range(len(current_board)) if current_board[i] == 0]
    good_moves = all_strats[str(board_to_state_hash(current_board))]
    if ai_number == 1:
        # perfect AI
        return random.choice(good_moves)
    elif ai_number == 2:
        return random.choice(possible_moves)
    elif ai_number == 3:
        chance_perfect = 0.7
        if random.uniform(0,1) < chance_perfect:
            return random.choice(good_moves)
        else:
            return random.choice(possible_moves)
    else:
        return random.choice(possible_moves)
    
def one_game(all_strats, your_color=1, ai_number=1):
    board_usage = '''
 0 | 1 | 2
-----------
 3 | 4 | 5
-----------
 6 | 7 | 8
'''
    current_board = empty_board()
    wait_for_valid_input = True
    AI_color = 3 - your_color

    if your_color == 2:
        ai_move = get_AI_move(current_board,1,all_strats)
        current_board[ai_move] = AI_color
        

    while describe_board(current_board) == 'progress':
        # your move:
        print(board_usage)
        print('Current board:')
        print(get_board_str(current_board))
        while wait_for_valid_input:
            move = input('You play %s, your move?[0-8] ' % ' OX'[your_color])
            if move in [str(i) for i in range(9)]:
                if current_board[int(move)] != 0:
                    print('Invalid move!')
                else:
                    move = int(move)
                    wait_for_valid_input = False
            else:
                print('Invalid input!')
        current_board[move] = your_color
        if describe_board(current_board) != 'progress':
            break
        
        # AI's move
        ai_move = get_AI_move(current_board,ai_number,all_strats)
        current_board[ai_move] = AI_color
        
        wait_for_valid_input = True

    print(get_board_str(current_board))    
    if describe_board(current_board) == 'player_two_win':
        print('X wins!')
    elif describe_board(current_board) == 'player_one_win':
        print('O wins!')
    else:
        print(describe_board(current_board))

def game_mode_select():
    wait_for_valid_input = True
    intro = '''

Tic-Tac-Toe New Game
Game mode:
0. Quit.
1. You play O. Perfect AI.
2. You play X. Perfect AI.
3. You play O. Bad AI.
4. You play X. Bad AI.
5. You play O. So-so AI.
6. You play X. So-so AI.
'''
    print(intro)
    while wait_for_valid_input:
        mode = input('Select game mode[1-6] or enter 0 to quit: ')
        if mode in [str(i) for i in range(0,7)]:
            mode = int(mode)
            wait_for_valid_input = False
        else:
            print('Invalid input!')
    if mode == 0:
        exit(0) # exit normally
    elif mode == 1:
        your_color = 1
        ai_number = 1
    elif mode == 2:
        your_color = 2
        ai_number = 1
    elif mode == 3:
        your_color = 1
        ai_number = 2
    elif mode == 4:
        your_color = 2
        ai_number = 2
    elif mode == 5:
        your_color = 1
        ai_number = 3
    elif mode == 6:
        your_color = 2
        ai_number = 3
    return your_color, ai_number

def main():
    import json
    import random
    with open('all_strats.json','r') as f:
        all_strats = json.load(f)
    while True:
        your_color, ai_number = game_mode_select()
        one_game(all_strats, your_color, ai_number)

main()
