import random
# import kdice
#
# dcs = Dices("2d6")

class Card(object):

    def __init__(self, name='', weigth=1, theme=None, multiThemed=False):
        self.name = name # name.lower().capitalize()
        if multiThemed:
            self._theme = []
            self._theme.append(theme)
        else:
            self._theme = theme
        self._weigth = weigth

    def __str__(self):
        if isinstance(self._theme, list):
            if self._theme[0] is None:
                return "{0._weigth}: {0.name}".format(self).strip('– ')
            else:
                themes = ""
                for theme in self._theme:
                    themes += theme + ", "
                return "{0._weigth}: {1} – {0.name}".format(self, themes.strip(', ')).strip('– ')
        elif self._theme == None:
            return "{0._weigth}: {0.name}".format(self).strip('– ')
        else:
            return "{0._weigth}: {0._theme} – {0.name}".format(self).strip('– ')

    def _get_weigth(self):
        return self._weigth

    weigth = property(_get_weigth)


class Deck(object):

    def __init__(self, name='basic'):
        self.cards = []
        self.undecked = []
        self.total = 0
        if name == 'basic':
            self.buildBasic(52)
        self.name = name
        self.multiThemed=False

    def buildBasic(self, n=54):
        for theme in ["Spades", "Clubs", "Hearts", "Diamonds"]:
            for face in range(1,14):
                if face == 1: # 2 = Deuce, but...
                    self.cards.append(Card('Ace',face,theme))
                elif face == 11:
                    self.cards.append(Card('Jack',face,theme))
                elif face == 12:
                    self.cards.append(Card('Queen',face,theme))
                elif face == 13:
                    self.cards.append(Card('King',face,theme))
                else:
                    self.cards.append(Card('',face,theme))
        if len(self.cards) < n:
            self.cards.append(Card('Joker color', 0, 'special'))
        if len(self.cards) < n:
            for i in range(len(self.cards), n):
                self.cards.append(Card('Joker grey', 0, 'special'))
        self.get_total()

    def __str__(self, div=' + '):
        cardsprint = ""
        for card in self.cards:
            cardsprint += card.__str__() + div
        return cardsprint.strip('+ ').replace('  ', ' ')

    def get_total(self):
        i = 0
        for card in self.cards:
            i += card.weigth
        self.total = i

    def shuffle(self):
        random.shuffle(self.cards)
        return self

    def draw_next(self):
        self.undecked.append(self.cards.pop())
        self.total += self.undecked[-1].weigth
        return self.undecked[-1]

    def add_card(self, name='', weigth=1, theme=None, num_times=1, multiThemed=False):
        if multiThemed:
            setMulti()
        for i in range(num_times):
            self.cards.append(Card(name, weigth, theme, multiThemed))
            self.total += weigth

    def append_card(self, card):
        self.cards.append(card)
        self.total += card.weigth

    def setMulti(self):
        multiThemed=True # TODO: saneCheck() # check if all cards are with list of themes instead of just one


class Blackjack(object):
    """Plays blackjack aka 21. Uses special count total"""

    def __init__(self):
        self._table = Deck('table')
        self._player = Deck('hand')
        self._deck = Deck().shuffle()
        print("Welcome to Blackjack!")
        self._firstPass()
        print('.' * 18)
        self.print_table()

    def _firstPass(self):
        self._table.append_card(self._deck.draw_next())
        self._player.append_card(self._deck.draw_next())
        self._player.append_card(self._deck.draw_next())

    def print_table(self):
        print("table:")
        print("[ Croupier's total: {1:2}] {0}".format(self._table, self._count_points(self._table)))
        print("[Your hand's total: {1:2}] {0}".format(self._player, self._count_points(self._player)))

    def _count_points(self, hand_deck):
        count = 0
        ace_special = 0
        for card in hand_deck.cards:
            if card.name.lower() == 'ace':
                ace_special += 1
            if card.weigth < 11:
                count += card.weigth
            else:
                count += 11
        if ace_special == 1:
            count += 9
        return count


if __name__ == '__main__':
    pass
    # game = Blackjack()

    # trying = Deck('hand')
    # trying.add_card('cinco guerreiros', 99, num_times=3)
    # print("{0} . {1}".format(trying, trying.total()))

    # table = Deck()
    # print(table.total)
