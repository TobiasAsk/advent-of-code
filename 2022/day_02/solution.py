OUTCOMES = [
    [3, 0, 6],
    [6, 3, 0],
    [0, 6, 3]
]


PLAYER_SHAPE = [
    [2, 0, 1],
    [0, 1, 2],
    [1, 2, 0]
]


def main():
    with open('dag 2/input.txt') as strategy_guide_file:
        strategy_guide = strategy_guide_file.readlines()

    player_score = 0
    for round in strategy_guide:
        opponent_move, desired_outcome = round.split()
        opponent_shape, mapped_desired_outcome = 'ABC'.index(opponent_move), 'XYZ'.index(
            desired_outcome)

        player_shape = PLAYER_SHAPE[opponent_shape][mapped_desired_outcome]
        player_score += player_shape + 1 + 3*mapped_desired_outcome

    print(f'Player score is {player_score}')


if __name__ == '__main__':
    main()
