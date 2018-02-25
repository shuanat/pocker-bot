from PIL import Image
import PIL

class Hand(object):
    NE = 'HAND_NE'
    SE = 'HAND_SE'
    S = 'HAND_S'
    SW = 'HAND_SW'
    NW = 'HAND_NW'
    N = 'HAND_N'

offsets_sizes = {
    'SUIT': ((0, 34), ((34, 36))),
    'RANK': ((7, 9), (20, 26)),
    'CARD': ((100, 0), (100, 140)),
    'BOARD': ((572, 420), (550, 140)),
    Hand.NE: ((1356, 187), (200, 140)),
    Hand.SE: ((1356, 545), (200, 140)),
    Hand.S: ((735, 749), (200, 140)),
    Hand.SW: ((116, 545), (200, 140)),
    Hand.NW: ((116, 187), (200, 140)),
    Hand.N: ((734, 61), (200, 140))
}

def crop(canvas, offset, size):
    (offset_x, offset_y) = offset
    (width, height) = size
    return canvas.crop((offset_x, offset_y, offset_x + width, offset_y + height))

def crop_suit(canvas):
    offset, size = offsets_sizes['SUIT']
    return crop(canvas, offset, size)

def crop_rank(canvas):
    offset, size = offsets_sizes['RANK']
    return crop(canvas, offset, size)

def crop_card(canvas, idx, padding):
    (left, top), size = offsets_sizes['CARD']
    width, _ = size
    offset = ((left + padding) * idx, top)
    return crop(canvas, offset, size)

def prescale_crop(table, name):
    table = table.resize((1675, 1193), resample=Image.BICUBIC)
    offset, size = offsets_sizes[name]
    return crop(table, offset, size)

def crop_board(table):
    return prescale_crop(table, 'BOARD')

def crop_hand(table, name):
    return prescale_crop(table, name)

class Cards(object):
    @staticmethod
    def board(table):
        cards = crop_board(table)
        cards = [crop_card(cards, idx, padding = 9) for idx in range(0, 5)]
        cards = [(crop_rank(c), crop_suit(c)) for c in cards]
        return zip(*cards)

    @staticmethod
    def hand(table, spot):
        cards = crop_hand(table, spot)
        cards = [crop_card(cards, idx, padding = 0) for idx in range(0, 2)]
        cards = [(crop_rank(c), crop_suit(c)) for c in cards]
        return zip(*cards)