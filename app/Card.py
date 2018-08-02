import sqlite3

"""
Models a flash card. That's it. (remember: single responsibility principle)
2018-07-22 mwroffo

update 2018-07-25: this class isn't necessary. just represent 
term and definition with sqlite columns. sqlchemy won't cooperate with
__conform__, either. (has no attribute _set_parent_with_dispatch)
"""

class Card:
    """
    Models a flash card.
    """
    def __init__(self, term, definition):
        """ initialized a new flash card object. empty fields are not allowed."""
        self._term = term
        self._definition = definition
        # self._set_parent_with_dispatch

    def __conform__(self, protocol):
        """ defines `Card`s str representation in a sqlite3 row """
        if protocol is sqlite3.PrepareProtocol:
            return "%s; %s" % (self.getTerm(), self.getDefinition())

    def getTerm(self):
        """ returns front of card as string """
        return str(self._term)

    def setTerm(self, term):
        self._term = term
    
    def getDefinition(self):
        """ return back of card as string """
        return str(self._definition)

    def setDefinition(self, definition):
        self._definition = definition

    def editCard(self, term, definition):
        self._term, self._definition = term, definition

    def __str__(self):
        return "TERM: {} DEFINITION: {}".format(self.getTerm(), self.getDefinition())

    def __eq__(self, other):
        """ equal cards are defined as having identical term and definition """
        if self.__str__() == other.__str__():
            return True
        else: False

def _main():
    """ TEST CLIENT """
    # test init:
    card = Card("Who murdered a man for Annagret?", "Andreas Wolf did. He\'s very charismatic.")
    # test __str__:
    print(card)
    print()

    # test set term:
    card.setTerm("Who murdered Annagret\'s stepfather?")
    print(card)

    # test set definition:
    card.setDefinition("Andreas Wolf.")
    print()
    print(card)

if __name__ == '__main__':
    _main()
