#ifndef GAMESTATUS_H
#define GAMESTATUS_H

#define MAX_BOARD_SIZE (3)

static const char symbol[3] = {' ', 'X', 'O'};

class GameStatus {
private:
	int currentPlayer; // who's turn
	int boardSize;
	int board[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
	int stdinInputCheck(const char *s, int *X, int *Y) {
		//ok: return 0
		//not ok: return 1
		if (strlen(s) != 3) {
			// including '\n'
			return 1;
		}
		if ((s[0]=='A'||s[0]=='B'||s[0]=='C'||s[0]=='a'||s[0]=='b'||s[0]=='c')&& 
		(s[1]=='1'||s[1]=='2'||s[1]=='3')) {
			if (s[0]=='A'||s[0]=='B'||s[0]=='C') {
				*X = s[0] - 'A';
			} else {
				*X = s[0] - 'a';
			}
			*Y = s[1] - '1';
			return 0;
		} else {
			return 1;
		}
		return 0;
	}
	int stdinInputLoop() {
		//ok: return 0
		//not ok: return 1
		printf("You are %c, Next Move=? (Ex. A1, b3)\n", symbol[currentPlayer]);
		fflush(stdout);
		char buff[64];
		fgets(buff, 64, stdin);
		int x, y;
		if (!stdinInputCheck(buff, &x, &y)) {
			// ok
			// printf("%d,%d\n", x, y);
			if (board[x][y] == 0) {
				board[x][y] = currentPlayer;
			} else {
				printf("Invalid input, need to put in somewhere empty\n");
				return 1; // already something there
			}
			return 0;
		} else {
			// invalid input
			printf("Invalid input format\n");
			return 1;
		}
		return 0;
	}
	bool hasEmptySpace() {
		for (int i = 0; i < boardSize; i++) {
			for (int j = 0; j < boardSize; j++) {
				if (board[i][j] == 0) {
					return true;
				}
			}
		}
		return false;
	}
	bool playerWin(int player) {
		bool allSame;
		// Type 1 win
		for (int i = 0; i < boardSize; i++) {
			allSame = true;
			for (int j = 0; j < boardSize; j++) {
				if (board[i][j] != player) {
					allSame = false;
				}
			}
			if (allSame) {
				return true;
			}
		}
		// Type 2 win
		for (int j = 0; j < boardSize; j++) {
			allSame = true;
			for (int i = 0; i < boardSize; i++) {
				if (board[i][j] != player) {
					allSame = false;
				}
			}
			if (allSame) {
				return true;
			}
		}
		// Type 3 win
		allSame = true;
		for (int i = 0; i < boardSize; i++) {
			if (board[i][i] != player) {
				allSame = false;
			}
		}
		if (allSame) {
			return true;
		}
		// Type 4 win
		allSame = true;
		for (int i = 0; i < boardSize; i++) {
			if (board[i][boardSize-1-i] != player) {
				allSame = false;
			}
		}
		if (allSame) {
			return true;
		}
		return false;
	}
public:
	GameStatus() {
		reset();
	}
	void setCurrentPlayer(int player) {
		if (player >= 3) {
			fprintf(stderr, "Invalid Player %d\n", player);
		}
		currentPlayer = player;
	}

	int getCurrentPlayer() {
		return currentPlayer;
	}
	void reset(int bS = 3) {
		clearBoard();
		boardSize = bS;
		currentPlayer = 0;
	}
	void clearBoard() {
		for (int i = 0; i < MAX_BOARD_SIZE; i++) {
			for (int j = 0; j < MAX_BOARD_SIZE; j++) {
				board[i][j] = 0;
			}
		}
	}
	void printBoard() {
		printf(" |A|B|C\n");
		printf("-------\n");
		printf("1|%c|%c|%c\n", symbol[board[0][0]], symbol[board[1][0]], symbol[board[2][0]]);
		printf("-------\n");
		printf("2|%c|%c|%c\n", symbol[board[0][1]], symbol[board[1][1]], symbol[board[2][1]]);
		printf("-------\n");
		printf("3|%c|%c|%c\n", symbol[board[0][2]], symbol[board[1][2]], symbol[board[2][2]]);
		printf("-------\n");
	}
	void stdinInput() {
		// return until get a valid input
		while(stdinInputLoop());
		return;
	}
	void nextPlayer() {
		if (currentPlayer == 1) {
			currentPlayer = 2;
		} else if (currentPlayer == 2) {
			currentPlayer = 1;
		} else {
			fprintf(stderr, "nextPlayer Error\n");
		}
		return;
	}
	
	bool gameEnded() {
		if (!hasEmptySpace()) {
			return true;
		} else {
			if (getWinner() != 0) {
				return true;
			}
		}
		return false;
	}
	int getWinner() {
		// 0: no winner
		for (int player = 1; player <= 2; player++) {
			if (playerWin(player)) {
				return player;
			}
		}
		return 0;
	}

};

#endif