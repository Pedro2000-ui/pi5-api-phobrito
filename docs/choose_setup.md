```python
def choose_setup(
    board: list[list[Cell]],
    professor_to_place: str,
) -> SetupResponse:
    
    """
    Fase de posicionamento: escolhe uma casa de nível 0 desocupada.
    """

    PAIRS = {
        "CLARO": "REY",
        "REY": "CLARO",
        "KARIN": "BEATRIZ",
        "BEATRIZ": "KARIN",
    }

    PRIORITIES = [
        (2, 2),

        (2, 1),
        (2, 3),
        (1, 2),
        (3, 2),

        (1, 1),
        (1, 3),
        (3, 1),
        (3, 3),
    ]

    def is_available(row: int, col: int) -> bool:
        return (
            0 <= row < BOARD_SIZE
            and 0 <= col < BOARD_SIZE
            and board[row][col].level == 0
            and board[row][col].professor is None
        )

    def find_best_priority() -> SetupResponse | None:
        for row, col in PRIORITIES:
            if is_available(row, col):
                return SetupResponse(
                    row=row,
                    col=col,
                )

        return None

    partner = PAIRS.get(professor_to_place)

    if partner:
        partner_pos = find_professor(
            board,
            partner,
        )

        #
        # Se o parceiro já está no tabuleiro,
        # tenta ficar adjacente a ele.
        #
        if partner_pos:
            row, col = partner_pos

            for dst_row, dst_col in adjacent_cells(
                row,
                col,
            ):
                if is_available(
                    dst_row,
                    dst_col,
                ):
                    return SetupResponse(
                        row=dst_row,
                        col=dst_col,
                    )

        #
        # Caso contrário, prioriza o centro.
        #
        priority_move = find_best_priority()

        if priority_move:
            return priority_move

    #
    # Fallback
    #
    candidates = [
        (r, c)
        for r in range(BOARD_SIZE)
        for c in range(BOARD_SIZE)
        if is_available(r, c)
    ]

    row, col = random.choice(candidates)

    return SetupResponse(
        row=row,
        col=col,
    )

```