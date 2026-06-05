```python
def choose_turn(
    board,
    team_id,
) -> Optional[PlayerTurnResponse]:

    moves = generate_moves(
        board,
        team_id,
    )

    if not moves:
        return None

    best_move = None
    best_score = float("-inf")

    for move in moves:

        score = score_move(
            board,
            move,
            team_id,
        )

        print(
        {
            "professor": move.professor,
            "row": move.move_to.row,
            "col": move.move_to.col,
            "mentor": (
                None
                if move.mentor_at is None
                else (
                    move.mentor_at.row,
                    move.mentor_at.col,
                )
            ),
            "score": score,
        })

        if score > best_score:

            best_score = score
            best_move = move

    print("================================")
    print("MELHOR SCORE:", best_score)
    print("MELHOR JOGADA:", best_move)
    print("================================")

    return best_move
```