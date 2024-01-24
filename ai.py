import torch
import torch.nn as nn
import chess
import numpy as np
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = nn.Sequential(
    nn.Conv2d(31, 32, kernel_size=3, padding=1),
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
    nn.Conv2d(128, 256, kernel_size=2, padding=1),
    nn.ReLU(),
    nn.BatchNorm2d(256),
    nn.Conv2d(256, 256, kernel_size=2, padding=1),
    nn.ReLU(),
    nn.BatchNorm2d(256),
    nn.Conv2d(256, 512, kernel_size=2, stride=2),
    nn.ReLU(),
    nn.BatchNorm2d(512),
    nn.Conv2d(512, 512, kernel_size=2, padding=1),
    nn.ReLU(),
    nn.BatchNorm2d(512),
    nn.Conv2d(512, 512, kernel_size=2, padding=1),
    nn.ReLU(),
    nn.BatchNorm2d(512),
    nn.Conv2d(512, 1024, kernel_size=2, stride=2),
    nn.Flatten(),
    nn.Dropout(.5),
    nn.Linear(4096, 1)
).to(device)


def init_weights(m):
    try:
        nn.init.xavier_uniform_(m.weight)
        m.bias.data.fill_(0.01)
    except Exception:
        return

model.apply(init_weights)


def to_bitboard(fen):
    boards = np.zeros((31, 8, 8), dtype=np.uint8)
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
    if board.is_check():
        if color:
            boards[1, :, :] = 1
        else:
            boards[2, :, :] = 1
    cr = board.castling_rights
    wkcastle = bool(cr & chess.H1)
    wqcastle = bool(cr & chess.A1)
    bkcastle = bool(cr & chess.H8)
    bqcastle = bool(cr & chess.A8)

    boards[0, :, :] = color

    boards[27, :, :] = wkcastle
    boards[28, :, :] = wqcastle
    boards[29, :, :] = bkcastle
    boards[30, :, :] = bqcastle

    material = 0

    piece_map = board.piece_map()
    for i, p in piece_map.items():
        rank, file = to_square(i)
        piece = p.symbol()
        # Mark the position of the piece on the bitboard
        boards[piece_to_layer[piece] + 2, rank, file] = 1
        material += piece_to_material[piece]
        # Attack maps
        for sq in board.attacks(i):
            attack_rank, attack_file = to_square(sq)
            boards[piece_to_layer[piece] + 14, attack_rank, attack_file] = 1

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
    encoded_board = torch.from_numpy(np.expand_dims(to_bitboard(board.fen()), 0)).to(device)
    score = model(encoded_board.float())
    move = check_mate_single(board)
    beginning_score =  model(torch.from_numpy(np.expand_dims(to_bitboard(board.fen()), 0)).to(device).float())
    if not move:
        best_move = None
        best_score = None
        print(board.fen())
        for i in board.legal_moves:
            board.push(i)
            encoded_board = torch.from_numpy(np.expand_dims(to_bitboard(board.fen()), 0)).to(device)
            score = model(encoded_board.float())
            board_copy = board.copy()
            board.pop()
            if not best_move or score < best_score:
                flag = True
                for j in board_copy.legal_moves:
                    board_copy.push(j)
                    encoded_board_copy = torch.from_numpy(np.expand_dims(to_bitboard(board_copy.fen()), 0)).to(device)
                    score_copy = model(encoded_board_copy.float())
                    board_copy.pop()
                    if score_copy - beginning_score > 0.8:
                        # print(i, score_copy, beginning_score, score_copy - beginning_score, False)
                        flag = False
                if flag:
                    best_move = i
                    best_score = score
        if not best_move:
            for i in board.legal_moves:
                board.push(i)
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

