from board import Piece

class FenDecoder:

    def __init__(self, fen_str):
        fields = fen_str.split()

        #Make piece array
        piece_placements = fields[0].split('/')
        self.piece_placement = []
        for pieces in piece_placements:
            row = []
            for piece in pieces:
                if piece.isnumeric():
                    row.append(['' for i in range(int(piece))])
                    continue
                
                color = Piece.WHITE if piece.isupper() else Piece.BLACK

                piece = piece.lower()
                if piece == 'p': row.append((Piece.PAWN, color))
                elif piece == 'n': row.append((Piece.KNIGHT, color))
                elif piece == 'b': row.append((Piece.BISHOP, color))
                elif piece == 'r': row.append((Piece.ROOK, color))
                elif piece == 'q': row.append((Piece.QUEEN, color))
                elif piece == 'k': row.append((Piece.KING, color))
            
            self.piece_placement.append(row)


        self.side_to_move = fields[1]
        self.castling_ability = fields[2]
        self.en_passant_square = fields[3]
        self.half_move_counter = int(fields[4])
        self.full_move_counter = int(fields[5])

        print(self.piece_placement)
