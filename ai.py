import torch
import torch.nn as nn
import chess
import numpy as np
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = nn.Sequential(
    nn.Conv2d(29, 32, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.BatchNorm2d(32),
    nn.Conv2d(32, 32, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.BatchNorm2d(32),
    nn.Conv2d(32, 64, kernel_size=3, stride=2),
    nn.ReLU(),
    nn.BatchNorm2d(64),
    nn.Conv2d(64, 64, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.BatchNorm2d(64),
    nn.Conv2d(64, 64, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.BatchNorm2d(64),
    nn.Conv2d(64, 128, kernel_size=3, stride=2),
    nn.ReLU(),
    nn.BatchNorm2d(128),
    nn.Conv2d(128, 128, kernel_size=2, padding=1),
    nn.ReLU(),
    nn.BatchNorm2d(128),
    nn.Conv2d(128, 128, kernel_size=2, padding=1),
    nn.ReLU(),
    nn.BatchNorm2d(128),
    nn.Conv2d(128, 256, kernel_size=2, stride=2),
    nn.Flatten(),
    nn.Dropout(.5),
    nn.Linear(256, 1)
).to(device)

def init_weights(m):
    try:
        nn.init.xavier_uniform_(m.weight)
        m.bias.data.fill_(0.01)
    except Exception:
        return

model.apply(init_weights)


def to_bitboard(fen):
    boards = np.zeros((29, 8, 8), dtype=np.uint8)
    board = chess.Board(fen)

    piece_to_layer = {
        'R': 1,
        'N': 2,
        'B': 3,
        'Q': 4,
        'K': 5,
        'P': 6,
        'p': 7,
        'k': 8,
        'q': 9,
        'b': 10,
        'n': 11,
        'r': 12
    }

    piece_to_material = {
        'R': 5,
        'N': 3,
        'B': 3,
        'Q': 9,
        'K': 0,
        'P': 1,
        'p': -1,
        'k': 0,
        'q': -9,
        'b': -3,
        'n': -3,
        'r': -5
    }

    color = bool(board.turn)

    cr = board.castling_rights
    wkcastle = bool(cr & chess.H1)
    wqcastle = bool(cr & chess.A1)
    bkcastle = bool(cr & chess.H8)
    bqcastle = bool(cr & chess.A8)

    boards[0, :, :]  = color
    boards[25, :, :] = wkcastle
    boards[26, :, :] = wqcastle
    boards[27, :, :] = bkcastle
    boards[28, :, :] = bqcastle

    material = 0

    piece_map = board.piece_map()
    for i, p in piece_map.items():
        rank, file = to_square(i)
        piece = p.symbol()
        # Mark the position of the piece on the bitboard
        boards[piece_to_layer[piece], rank, file] = 1
        material += piece_to_material[piece]
        # Attack maps
        for sq in board.attacks(i):
            attack_rank, attack_file = to_square(sq)
            boards[piece_to_layer[piece]+12, attack_rank, attack_file] = 1

    return boards

def to_square(number):
    rank, file = divmod(number, 8)
    return 7 - rank, file

def check_mate_single(board):
    board = board.copy()
    legal_moves = list(board.legal_moves)
    for move in legal_moves:
        board.push_uci(str(move))
        if board.is_checkmate():
            move = board.pop()
            return move
        board.pop()

def get_ai_move(model, board):
    move = check_mate_single(board)
    beginning_score =  model(torch.from_numpy(np.expand_dims(to_bitboard(board.fen()), 0)).to(device).float())
    if not move:
        best_move = None
        best_score = None
        for i in board.legal_moves:
            board.push(i)
            board_copy = board.copy()
            encoded_board = torch.from_numpy(np.expand_dims(to_bitboard(board.fen()), 0)).to(device)
            score = model(encoded_board.float())
            board.pop()
            if not best_move or score < best_score:
                flag = True
                for j in board_copy.legal_moves:
                    board_copy.push(j)
                    encoded_board_copy = torch.from_numpy(np.expand_dims(to_bitboard(board_copy.fen()), 0)).to(device)
                    score_copy = model(encoded_board_copy.float())
                    board_copy.pop()
                    if beginning_score + score_copy > beginning_score + 0.5:
                        flag = False
                if flag:
                    best_move = i
                    best_score = score
        if not best_move:
            for i in board.legal_moves:
                board.push(i)
                board_copy = board.copy()
                encoded_board = torch.from_numpy(np.expand_dims(to_bitboard(board.fen()), 0)).to(device)
                score = model(encoded_board.float())
                board.pop()
                if not best_move or score < best_score:
                    best_move = i
                    best_score = score
    else:
        best_move = move
        best_score = -1.5
    return best_move, best_score

import re
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


piece_to_layer = {
        'R': 1,
        'N': 2,
        'B': 3,
        'Q': 4,
        'K': 5,
        'P': 6,
        'p': 7,
        'k': 8,
        'q': 9,
        'b': 10,
        'n': 11,
        'r': 12
    }

def to_square(number):
    rank, file = divmod(number, 8)
    return 7 - rank, file

# example: e3 -> (3, 4)
def square_to_index(square):
  letter = chess.square_name(square)
  return 8 - int(letter[1]), squares_index[letter[0]]

def board_2_rep(board):
    board3d = np.zeros((26, 8, 8), dtype=np.int8)
    piece_map = board.piece_map()
    for i, p in piece_map.items():
        rank, file = to_square(i)
        piece = p.symbol()
        # Mark the position of the piece on the bitboard
        board3d[piece_to_layer[piece] - 1, rank, file] = 1
        for sq in board.attacks(i):
            attack_rank, attack_file = to_square(sq)
            board3d[piece_to_layer[piece]+11, attack_rank, attack_file] = 1
    aux = board.turn
    board.turn = chess.WHITE
    for move in board.legal_moves:
      i, j = square_to_index(move.to_square)
      board3d[24][i][j] = 1
    board.turn = chess.BLACK
    for move in board.legal_moves:
      i, j = square_to_index(move.to_square)
      board3d[25][i][j] = 1
    board.turn = aux
    return board3d


def get_ai_move(model, board):
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


def fen_to_bit_vector(fen):
    # piece placement - lowercase for black pieces, uppercase for white pieces. numbers represent consequtive spaces. / represents a new row
    # active color - whose turn it is, either 'w' or 'b'
    # castling rights - which castling moves are still legal K or k for kingside and Q or q for queenside, '-' if no legal castling moves for either player
    # en passant - if the last move was a pawn moving up two squares, this is the space behind the square for the purposes of en passant
    # halfmove clock - number of moves without a pawn move or piece capture, after 50 of which the game is a draw
    # fullmove number - number of full turns starting at 1, increments after black's move

    # Example FEN of starting position
    # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

    parts = re.split(" ", fen)
    piece_placement = re.split("/", parts[0])
    active_color = parts[1]
    castling_rights = parts[2]
    en_passant = parts[3]
    halfmove_clock = int(parts[4])
    fullmove_clock = int(parts[5])

    bit_vector = np.zeros((13, 8, 8), dtype=np.uint8)

    # piece to layer structure taken from reference [1]
    piece_to_layer = {
        'R': 1,
        'N': 2,
        'B': 3,
        'Q': 4,
        'K': 5,
        'P': 6,
        'p': 7,
        'k': 8,
        'q': 9,
        'b': 10,
        'n': 11,
        'r': 12
    }

    castling = {
        'K': (7, 7),
        'Q': (7, 0),
        'k': (0, 7),
        'q': (0, 0),
    }

    for r, row in enumerate(piece_placement):
        c = 0
        for piece in row:
            if piece in piece_to_layer:
                bit_vector[piece_to_layer[piece], r, c] = 1
                c += 1
            else:
                c += int(piece)

    if en_passant != '-':
        bit_vector[0, ord(en_passant[0]) - ord('a'), int(en_passant[1]) - 1] = 1

    if castling_rights != '-':
        for char in castling_rights:
            bit_vector[0, castling[char][0], castling[char][1]] = 1

    if active_color == 'w':
        bit_vector[0, 7, 4] = 1
    else:
        bit_vector[0, 0, 4] = 1

    if halfmove_clock > 0:
        c = 7
        while halfmove_clock > 0:
            bit_vector[0, 3, c] = halfmove_clock % 2
            halfmove_clock = halfmove_clock // 2
            c -= 1
            if c < 0:
                break

    if fullmove_clock > 0:
        c = 7
        while fullmove_clock > 0:
            bit_vector[0, 4, c] = fullmove_clock % 2
            fullmove_clock = fullmove_clock // 2
            c -= 1
            if c < 0:
                break

    return bit_vector