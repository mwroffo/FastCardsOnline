from Card import Card

"""
Representing a deck of flash`Card`s.

There are plenty of prebaked structures for this purpose, but for the sake
of data structures practice, I built this from scratch. 

In data structures terms, this is most like a List. It allows inserts and
removals at head, tail, or anywhere in the middle, in addition to sets and
contains, indexOf, etc.

2018-07-22 mwroffo
"""
class Deck:
    """ Models a deck of flash`Card`s.
    
    Knows the deck's name and the cards in it. Iterable. Allows dups.
    """

    def __init__(self, name, cards=[]):
        """ init a deck with list of cards as arg, or empty list """
        self._name = name
        self._cards = cards  # a `Deck` is a `list` of `Card`s
        self._size = len(cards)

    def getSize(self):
        return self._size
    
    def doesContain(self, other):
        for i in range(len(self._cards)):
            if self._cards[i] == other:
                return True # should `break` automatically with retur
        return False

    def set(self, index, card):
        """ sets the card at index `index` to equal `card` """
        self._cards[index] = card

    def indexOf(self, card):
        """ return index of `card`. if not found, return -1 """
        for i in range(len(self._cards)):
            if self._cards[i] == card:
                return i
        return -1
    
    def tailInsert(self, card):
        """ add a `Card` to the end of the deck """
        self._cards.append(card)
        self._size += 1
    
    def headInsert(self, card):
        """ add a `Card` to the front of the deck """
        self._cards.insert(0, card)
        self._size += 1

    def insertAt(self, card, index):
        """ add a `Card` before index `index` """
        self._cards.insert(index, card)
        self._size += 1
    
    def remove(self, card):
        """ remove the matching `Card` from the deck """
        self._cards.remove(card)
        self._size -= 1

    def clear(self):
        """ empties the `Deck` """
        self._cards = []
        self._size = 0

    def getName(self):
        """ returns the name of the `Deck` """
        return self._name

    def setName(self, name):
        """ sets the name of the `Deck` """
        self._name = name

    def getCards(self):
        """ returns the `Card`s in the `Deck` as a `list`. """
        return self._cards

    def setCards(self, cards):
        """ sets the `Card`s in the `Deck` to `cards`. """
        self._cards = cards
        self._size = len(cards)

    def __str__(self):
        """ returns a str representation of the deck """
        cardstrs = []
        for card in self.getCards():
            cardstrs.append(str(card))
        return "{} CARDS IN DECK {}: {}".format(str(self._size),
            self.getName().upper(), cardstrs)

def _main():
    """ test client """
    # test card constructor
    card = Card("Who murdered a man for Annagret?",
                "Andreas Wolf did. He\'s very charismatic.")
    card2 = Card("What is Purity\'s mother\'s name?",
                "Anabel.")
    deck = Deck("Purity Trivia", [card, card2]) # test constructor: init deck with a list
    card3 = Card("Who is it that knows Andreas Wolf\'s great secret?",
                "Tom. And his daughter, Purity.")
    deck.tailInsert(card3)

    # test set:
    deck.set(1, Card("I am now", "The second card"))
    print(deck)
    print()
    # test insertAt:
    card4 = Card("I will be inserted", "third")
    deck.insertAt(card4, 2)
    print(deck)
    print()
    # test index of 
    index = deck.indexOf(card4)
    print("EXPECTED 2, ACTUAL {}".format(str(index)))

    # test card set methods:
    card4.setTerm("I will be")
    card4.setDefinition("gone")
    deck.set(index, card4)
    print("EXPECTED third card to change, ACTUAL {}".format(str(deck)))
    
    # test removal
    deck.remove(card4)
    print("EXPECTED third card to be removed, ACTUAL {}".format(deck))

if __name__ == '__main__':
    _main()
