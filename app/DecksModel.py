import sqlite3
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.sql import select
from app.DeckModel import DeckModel

class DecksModel:
    """
    creates, destroys, and displays a user's decks
    maintains _decks, a dictionary containing all of the user's decks.
    _decks is a dict with `DeckModel`s of all decks in user's database
    """
    def __init__(self, username):
        self._username = username
        self._engine = create_engine('sqlite:///{}.db'.format(username), echo=False)
        self._meta = MetaData(self._engine)
        self._decks = {} # keys=decknames, values DeckModels
        self.update_decks_dict()

    def addDeck(self, newdeckname):
        """ Creates a new deck with `newdeckname` in `self._username.db` """
        DeckModel(newdeckname, self._username)
        self.update_decks_dict()

    def removeDeck(self, deckname):
        """ removes `deckname` from the database """
        try:
            deck_to_remove = self._decks[deckname].getTable()
        except KeyError:
            print("KeyError: the table {} does not exist".format(deckname))
            return
        self._meta = MetaData(self._engine)
        self._meta.reflect()
        deck_to_remove.drop(self._engine)
        self.update_decks_dict()

    def getDecks(self):
        """ returns the dictionary of 'deckname': `DeckModel` object pairs """
        return self._decks
    def getDeck(self, deckname):
        """ takes deckname and returns deck as DeckModel object """
        return self._decks[deckname]
    
    def update_decks_dict(self):
        """
        Helper method maintains dict of deckname: DeckModel
        Call this every time a deck is added or removed from database.
        """
        self._decks = {} # empty that dictionary, man.
        self._meta = MetaData()
        self._meta.reflect(self._engine) # reinit meta
        # and then refill it with all db tables in meta
        for tablename in self._meta.tables.keys():
            self._decks[tablename] = DeckModel(tablename, self._username)

    def __str__(self):
        result = ''
        self.update_decks_dict()
        for value in self._decks.values():
            result += str(value) + '\n'
        return result

def _testInit():
    decksmodel = DecksModel('mwroffo')
    print(decksmodel.getDecks()) # print the master dict

def _testAddDeck():
    mwroffo = DecksModel('mwroffo')
    # print('BEFORE:\n', mwroffo)
    mwroffo.addDeck('chekov')
    # mwroffo.addDeck('dostoyevsky')
    mwroffo.addDeck('david foster wallace')

def _testRemoveDeck():
    mwroffo = DecksModel('mwroffo')
    mwroffo.removeDeck('david foster wallace')
    mwroffo.removeDeck('chekov')
    # print('AFTER:\n', mwroffo)

def _testBench():
    # _testInit()
    # _testAddDeck()
    # _testRemoveDeck()
    pass

if __name__ == '__main__':
    _testBench()
