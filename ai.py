import chess
import numpy as np
import tensorflow as tf
squares_index = {
  'a': 0,
  'b': 1,
  'c': 2,
  'd': 3,
  'e': 4,
  'f': 5,
  'g': 6,
  'h': 7
}


# example: e3 -> (3, 4)
def square_to_index(square):
  letter = chess.square_name(square)
  return 8 - int(letter[1]), squares_index[letter[0]]


def board_2_rep(board):
    board3d = np.zeros((14, 8, 8), dtype=np.int8)
    for piece in chess.PIECE_TYPES:
        for square in board.pieces(piece, chess.WHITE):
            idx = np.unravel_index(square, (8, 8))
            board3d[piece - 1][7 - idx[0]][idx[1]] = 1
        for square in board.pieces(piece, chess.BLACK):
            idx = np.unravel_index(square, (8, 8))
            board3d[piece + 5][7 - idx[0]][idx[1]] = 1
    aux = board.turn
    board.turn = chess.WHITE
    for move in board.legal_moves:
      i, j = square_to_index(move.to_square)
      board3d[12][i][j] = 1
    board.turn = chess.BLACK
    for move in board.legal_moves:
      i, j = square_to_index(move.to_square)
      board3d[13][i][j] = 1
    board.turn = aux
    return board3d


def get_ai_move(model, board):
    # chooses the best move based on the AI Eval Score
    # play as black

    best_move = None
    best_score = None
    move = check_mate_single(board)
    if not move:
        for i in board.legal_moves:
            board.push(i)
            score = ai_eval(model, board)
            board.pop()
            if not best_move or best_score > score:
                best_move = i
                best_score = score
    else:
        best_move = move
        best_score = 1
    return best_move, best_score

def check_mate_single(board):
    board = board.copy()
    legal_moves = list(board.legal_moves)
    for move in legal_moves:
        board.push_uci(str(move))
        if board.is_checkmate():
            move = board.pop()
            return move
        board.pop()


def ai_eval(model, board):
    data = board_2_rep(board)
    return model.predict(tf.transpose(np.expand_dims(data, 0), [0, 2, 3, 1]))[0][0]
    # return model.predict(np.expand_dims(data, 0))[0][0]