# app/logic.py
import random
from typing import Optional

from app.schemas import Cell, Position, SetupResponse, PlayerTurnResponse

BOARD_SIZE = 5

# Professores de cada time
TEAM_PROFESSORS = {
    1: ["CLARO", "REY"],       # Turing
    2: ["KARIN", "BEATRIZ"],   # Lovelace
}


def adjacent_cells(row: int, col: int) -> list[tuple[int, int]]:
    """
    Retorna todas as casas vizinhas (incluindo diagonais).
    O tabuleiro e 5x5, entao filtra coordenadas fora dos limites.
    """
    cells = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                cells.append((nr, nc))
    return cells


def find_professor(board: list[list[Cell]], name: str) -> Optional[tuple[int, int]]:
    """Encontra a posicao (row, col) de um professor no tabuleiro."""
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c].professor == name:
                return (r, c)
    return None

def generate_moves(board, team_id):
    moves = []

    for professor in TEAM_PROFESSORS[team_id]:

        pos = find_professor(board, professor)

        if pos is None:
            continue

        cur_row, cur_col = pos
        cur_level = board[cur_row][cur_col].level

        for dst_row, dst_col in adjacent_cells(cur_row, cur_col):

            dst_cell = board[dst_row][dst_col]

            if dst_cell.professor is not None:
                continue

            if dst_cell.level == 4:
                continue

            if dst_cell.level > cur_level + 1:
                continue

            #
            # vitória imediata
            #
            if dst_cell.level == 3:
                moves.append(
                    PlayerTurnResponse(
                        professor=professor,
                        move_to=Position(
                            row=dst_row,
                            col=dst_col,
                        ),
                    )
                )
                continue

            #
            # mentorias possíveis
            #
            for men_row, men_col in adjacent_cells(dst_row, dst_col):

                men_cell = board[men_row][men_col]

                is_source = (
                    men_row == cur_row
                    and men_col == cur_col
                )

                if (
                    men_cell.level < 4
                    and (
                        men_cell.professor is None
                        or is_source
                    )
                ):
                    moves.append(
                        PlayerTurnResponse(
                            professor=professor,
                            move_to=Position(
                                row=dst_row,
                                col=dst_col,
                            ),
                            mentor_at=Position(
                                row=men_row,
                                col=men_col,
                            ),
                        )
                    )

    return moves

import copy

def apply_move(board, move):

    board = copy.deepcopy(board)

    pos = find_professor(
        board,
        move.professor,
    )

    if pos is None:
        return board

    src_row, src_col = pos

    dst_row = move.move_to.row
    dst_col = move.move_to.col

    board[src_row][src_col].professor = None

    board[dst_row][dst_col].professor = move.professor

    if move.mentor_at is not None:

        mr = move.mentor_at.row
        mc = move.mentor_at.col

        if board[mr][mc].level < 4:
            board[mr][mc].level += 1

    return board

def enemy_team(team_id):
    return 2 if team_id == 1 else 1

def enemy_has_immediate_win(board, team_id):

    enemy = enemy_team(team_id)

    for move in generate_moves(board, enemy):

        dst = board[
            move.move_to.row
        ][
            move.move_to.col
        ]

        if dst.level == 3:
            return True

    return False

def score_move(board, move, team_id):

    score = 0

    simulated = apply_move(
        board,
        move,
    )

    print(
        "AMEACA_INIMIGA",
        move.professor,
        move.move_to.row,
        move.move_to.col,
        enemy_has_immediate_win(
            simulated,
            team_id,
        )
    )

    #
    # PRIORIDADE 1
    # impedir vitória adversária
    #

    if not enemy_has_immediate_win(
        simulated,
        team_id,
    ):
        score += 10000

    #
    # PRIORIDADE 2
    # subir de nível
    #

    current_pos = find_professor(
        board,
        move.professor,
    )

    if current_pos:

        cur_row, cur_col = current_pos

        current_level = board[
            cur_row
        ][
            cur_col
        ].level

        destination_level = board[
            move.move_to.row
        ][
            move.move_to.col
        ].level

        delta = (
            destination_level
            - current_level
        )

        score += delta * 500

        score += (
            destination_level ** 2
        ) * 100

    #
    # PRIORIDADE 3
    # vitória própria
    #

    dst_level = board[
        move.move_to.row
    ][
        move.move_to.col
    ].level

    if dst_level == 3:
        score += 1000

    #
    # PRIORIDADE 4
    # criar torres úteis
    #

    if move.mentor_at:

        mr = move.mentor_at.row
        mc = move.mentor_at.col

        current = board[mr][mc].level
        future = min(
            current + 1,
            4,
        )

        if future == 2:
            score += 50

        elif future == 3:
            score += 150

        elif future == 4:
            score += 200

    score += random.randint(0, 10)

    return score

def choose_setup(
    board: list[list[Cell]],
    professor_to_place: str,
) -> SetupResponse:

    """
    Fase de posicionamento: escolhe uma casa de nivel 0 desocupada.
    """

    def is_available(row, col):

        return (
            0 <= row < BOARD_SIZE
            and 0 <= col < BOARD_SIZE
            and board[row][col].level == 0
            and board[row][col].professor is None
        )

    #
    # prioriza o centro se for o primeiro professor, senão prioriza ficar próximo ao seu parceiro
    #
    if professor_to_place == "CLARO":

        rey_pos = find_professor(
            board,
            "REY",
        )

        if rey_pos:
            row, col = rey_pos

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
        else:

            priorities = [
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

            for row, col in priorities:

                if is_available(row, col):
                    return SetupResponse(
                        row=row,
                        col=col,
                    )

    #
    # prioriza o centro se for o primeiro professor, senão prioriza ficar próximo ao seu parceiro
    #
    if professor_to_place == "REY":

        claro_pos = find_professor(
            board,
            "CLARO",
        )

        if claro_pos:

            row, col = claro_pos

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

        else:
            priorities = [
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

        for row, col in priorities:

            if is_available(row, col):
                return SetupResponse(
                    row=row,
                    col=col,
                )
    #
    # fallback
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