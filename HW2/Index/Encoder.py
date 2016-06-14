class DeltaEncoder( object ):

    @staticmethod
    def encode(values):
        encoded = []
        last = 0
        for v in values:
            current = v
            new_v = current - last
            encoded.append(new_v)
            last = current

        return encoded


    # TODO : DECODER
    @staticmethod
    def decode(values):
        decoded = []
        last = 0
        for v in values:
            delta = v
            decoded.append(delta + last)
            last = v

        return decoded
