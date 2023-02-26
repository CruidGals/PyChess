from piece import Piece

class FenDecoder:

    def __init__(self, fen_str):
        fields = fen_str.split()

        #Make piece array
        piece_placements = fields[0].split('/')
        


        self.side_to_move = fields[1]
        self.castling_ability = fields[2]
        self.en_passant_square = fields[3]
        self.half_move_counter = fields[4]
        self.full_move_counter = fields[5]

        print(self.piece_placements)
