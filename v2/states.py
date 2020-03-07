from time import sleep

# 0: empty
# 1: O
# 2: X

# 0 1 2
# 3 4 5
# 6 7 8


def empty_board():
    return list([0, 0, 0, 0, 0, 0, 0, 0, 0])
    
def board_to_state_hash(board):
    num = 0
    for i in range(9):
        num *= 3
        num += board[i]
    return num

def get_board_str(board):
    ret = ''
    for i in range(3):
        for j in range(3):
            tmp_char = ' OX'[board[i * 3 + j]]
            ret += tmp_char
        ret += '\n'
    return ret
    
def state_hash_to_board(num):
    x = int(num)
    ret = []
    for i in range(9):
        ret.append(x % 3)
        x = int((x - x % 3) / 3)
    return list(reversed(ret))
    
def get_all_next_board(board, next_player):
    ret = []
    for i in range(9):
        if board[i] == 0:
            tmp = list(board)
            tmp[i] = next_player
            ret.append(list(tmp))
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
    
#a = [0, 0, 0, 0, 1, 2, 0, 0, 0]
#b = [1, 1, 1, 2, 0, 2, 0, 2, 0]
#c = [1, 1, 1, 0, 0, 0, 2, 2, 2]
#d = [1, 1, 2, 2, 1, 1, 1, 2, 2]
#e = [1, 1, 0, 2, 2, 2, 0, 0, 1]
#print(get_board_str(a),describe_board(a))
#print(get_board_str(b),describe_board(b))
#print(get_board_str(c),describe_board(c))
#print(get_board_str(d),describe_board(d))
#print(get_board_str(e),describe_board(e))
def dfs(board, next_player):
    #print(get_board_str(board))
    num = board_to_state_hash(board)
    description = describe_board(board)
    if description == 'progress':
        next_boards = get_all_next_board(board,next_player)
    else:
        next_boards = []
    #print(num)
    #print(get_board_str(board), description, [board_to_state_hash(x) for x in next_boards])
    print(num, description, [board_to_state_hash(x) for x in next_boards])
    for x in next_boards:
        dfs(x, 3 - next_player)
    return
    
def get_best_state(next_player, next_boards_status, next_moves):
    best_state = 'invalid'
    strategy = []
    if next_player == 1:
        if 'player_one_always_win' in next_boards_status:
            best_state = 'player_one_always_win'
        elif 'tie' in next_boards_status:
            best_state = 'tie'
        else:
            best_state = 'player_two_always_win'
    elif next_player == 2:
        if 'player_two_always_win' in next_boards_status:
            best_state = 'player_two_always_win'
        elif 'tie' in next_boards_status:
            best_state = 'tie'
        else:
            best_state = 'player_one_always_win'
    strategy = [next_moves[i] for i in range(len(next_moves)) if next_boards_status[i] == best_state]
    return best_state, strategy

 

def dfs_brute_force(board, next_player):
    i_win = ['','player_one_win','player_two_win'][next_player]
    i_always_win = ['','player_one_always_win','player_two_always_win'][next_player]
    you_win = ['','player_one_win','player_two_win'][3-next_player]
    you_always_win = ['','player_one_always_win','player_two_always_win'][3-next_player]

    num = board_to_state_hash(board)
    description = describe_board(board)
    if description == 'progress':
        next_boards = get_all_next_board(board,next_player)
    else:
        next_boards = []
    #print(num)
    #print(get_board_str(board), description, [board_to_state_hash(x) for x in next_boards])
    #sleep(2)
    if description == i_win:
        return i_always_win
    elif description == you_win:
        return you_always_win
    elif description == 'tie':
        return 'tie'
    elif description == 'progress':
        next_boards = get_all_next_board(board,next_player)
        next_boards_status = []
        next_moves = []
        for x in next_boards:
            tmp_next_move = [i for i in range(len(board)) if board[i] != x[i]][0]
            tmp_next_board_status = dfs_brute_force(x, 3 - next_player)
            next_boards_status.append(tmp_next_board_status)
            next_moves.append(tmp_next_move)
        best_state, strategy = get_best_state(next_player, next_boards_status, next_moves)
        #if best_state == 'player_two_always_win':
        #    print(get_board_str(board), next_player, best_state, strategy)
        #    sleep(1)
        global all_strats
        all_strats[board_to_state_hash(board)] = strategy
        return best_state
    else:
        return 'invalid'
        
#my = dfs_brute_force([1,2,1,2,1,2,0,0,0],1)
#print(my)
#my = dfs_brute_force([1,1,2,2,1,2,0,0,0],1)
#print(my)
#my = dfs_brute_force([1,1,2,2,1,2,0,0,0],2)
#print(my)
all_strats = {}
my = dfs_brute_force([0,0,0,0,0,0,0,0,0],1)
print(my)

#print(all_strats[board_to_state_hash([0,0,0,0,1,2,0,0,0])])
#print(all_strats[board_to_state_hash([0,0,0,0,1,0,0,0,0])])

import json
all_strats_json = json.dumps(all_strats)
with open('all_strats.json','w') as f:
    f.write(all_strats_json)



