from board import Piece

class FenDecoder:

    piece_placement = []
    side_to_move = None
    castling_ability = None
    half_move_counter = None
    full_move_counter = None

    def __init__(self, fen_str):
        fields = fen_str.split()

        #Make piece array
        #Makes a 2d array of tuples (Piece_Type, Piece_Color). If there is no piece on the square, inserts an empty string
        piece_placements = fields[0].split('/')
        for pieces in piece_placements:
            row = []
            for piece in pieces:
                if piece.isnumeric():
                    for i in range(int(piece)):
                        row.append(None)
                    continue
                
                color = Piece.WHITE if piece.isupper() else Piece.BLACK

                piece = piece.lower()
                if piece == 'p': row.append((Piece.PAWN, color))
                elif piece == 'n': row.append((Piece.KNIGHT, color))
                elif piece == 'b': row.append((Piece.BISHOP, color))
                elif piece == 'r': row.append((Piece.ROOK, color))
                elif piece == 'q': row.append((Piece.QUEEN, color))
                elif piece == 'k': row.append((Piece.KING, color))
            
            FenDecoder.piece_placement.append(row)

        FenDecoder.side_to_move = Piece.WHITE if fields[1] == 'w' else Piece.BLACK
        FenDecoder.castling_ability = fields[2]
        FenDecoder.en_passant_square = fields[3]
        FenDecoder.half_move_counter = int(fields[4])
        FenDecoder.full_move_counter = int(fields[5])