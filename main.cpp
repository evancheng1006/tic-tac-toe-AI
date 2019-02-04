#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include "GameStatus.h"

int main() {
	GameStatus gameStatus;
	
	gameStatus.setCurrentPlayer(1);
	while(!gameStatus.gameEnded()) {
		gameStatus.printBoard();
		gameStatus.stdinInput();
		gameStatus.nextPlayer();
	}
	gameStatus.printBoard();
	int winner = gameStatus.getWinner();
	if (winner == 0) {
		printf("it's a tie\n");
	} else {
		printf("Player %c wins\n", symbol[winner]);
	}

	return 0;
}