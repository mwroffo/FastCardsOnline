import sqlite3
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.sql import select
from . import db # access the sessionmaker
from flask import current_app, g

class DeckModel:
    """
    encapsulates sqlalchemy methods and represents a 
    connection to a particular `Deck`, which constitutes all rows in
    table `card` that share a `deck_id`.

    SECURITY CONSIDERATIONS: remember to validate input.
    Reject term and definition inputs that look like SQL commands, html tags, javascript, etc.
    Write a testbench for security specifically.
    """
    def __init__(self, tablename, username):
        self._tablename, self._username = tablename, username
        self._engine = create_engine('sqlite:///{}.db'.format(username), echo=False)
        self._con = self._engine.connect()
        self._metadata = MetaData(self._engine)
        self._table = Table(tablename, self._metadata,
                                Column('id', Integer, primary_key=True),
                                Column('term', String),
                                Column('definition', String)
                                )
        self._metadata.create_all(self._engine)

    def getCards(self):
        """
        Returns the `list` resulting from `session.query(self._table).all()`
        """
        with db.get_db() as session:
            return session.query(self._table).all()
    
    def addCard(self, term, definition):
        """ add a new card to the deck. DO NOT allow duplicate terms. """
        ins = self._table.insert().values(term=term, definition=definition)
        self._con.execute(ins)

    def selectCard(self, rowid):
        """ Returns the row that has `rowid`, with columns delimited by semicolons """
        s = select([self._table])
        result_proxy = self._con.execute(s)
        tup_array = result_proxy.fetchall()
        result_tup = tup_array[rowid - 1]
        result_str = ''
        for i in range(1, len(result_tup)):
            if result_tup[i] != result_tup[len(result_tup) - 1]:
                result_str += str(result_tup[i]) + ' ; '
            else:
                result_str += str(result_tup[i])
        return result_str

    def removeCardByTerm(self, term):
        """
        deletes from the deck all cards with term `term`.
        """
        delete = self._table.delete().where(
            self._table.c.term == term)
        self._con.execute(delete)

    def removeCard(self, rowid):
        """ delete from the deck the card with rowid `id` """
        delete = self._table.delete().where(
            self._table.c.id == rowid)
        self._con.execute(delete)

    def editCard(self, rowid, newterm, newdefinition):
        """
        give rowid as parameter to identify card,
        then give newterm and newdefinition as edits.
        there must be a better way to id cards... 
        TODO again, how to return rowids in columns?
        TODO could some default parameters reduce the code repetition in the editCard methods?
        """
        update = self._table.update().where(
            self._table.c.id == rowid).\
            values(term = newterm, definition = newdefinition)
        self._con.execute(update)
        # return the card...? this would be so much better if I could
        # be representing this card pythonically in the database...
    
    def editCardTerm(self, rowid, newterm):
        """ id the card with rowid, then update term to newterm. """
        update = self._table.update().where(
            self._table.c.id == rowid).\
            values(term=newterm)
        self._con.execute(update)
    
    def editCardDefinition(self, rowid, newdefinition):
        """ id by rowid, pass newdefinition as parameter. """
        update = self._table.update().where(
            self._table.c.id == rowid).\
            values(definition=newdefinition)
        self._con.execute(update)

    def __str__(self):
        con = sqlite3.connect('{}.db'.format(self._username))
        cur = con.cursor()

        # for tablenames with spaces, add quotes so that sql can understand:
        if ' ' in self._tablename:
            self._tablename = '\'' + self._tablename + '\''

        # run the query:
        view_table_query = 'SELECT * FROM {};'.format(self._tablename)
        cur.execute(view_table_query)
        columns = cur.fetchall()

        # now remove the quotes:
        tablename_de_quoted = ''
        for c in self._tablename:
            if c == '\'':
                c = ''
            tablename_de_quoted += c
        self._tablename = tablename_de_quoted
        toReturn = self._tablename.upper() + ':\n'
        for row in columns:
            for entry in row:
                # if it's the last entry but not the last row,
                if entry == row[len(row)-1] and row != columns[len(columns)-1]:
                    toReturn += str(entry) + '\n'
                # if it's the last entry in the last row,
                elif entry == row[len(row)-1]:
                    toReturn += str(entry)
                else: # if it's a middle entry:
                    toReturn += str(entry) + ' | '
        con.commit()  # database is locked from other connections unless changes are committed
        con.close()   # close the database connection
        con = None    # release memory        
        cur = None    # release memory
        return toReturn

    def getTable(self):
        return self._table
    def getTablename(self):
        return self._tablename
    def getEngine(self):
        return self._engine
    def getMetaData(self):
        return self._metadata
    def getConn(self):
        return self._con

############################## TEST BENCH ###################################
def _testInit():
    print("should create new table franzen")
    deck = DeckModel('franzen', 'mwroffo')
    print(deck, '\n')
    print("should change nothing since franzen already exists:")
    deck = DeckModel('franzen', 'mwroffo')
    print(deck)

def _testAdd():
    deck = DeckModel('franzen', 'mwroffo')
    # deck.addCard('who is purity\'s father?', 'Tom, the editor.')
    # deck.addCard('who commited a murder for Annagret?', 'Andreas Wolf.')
    deck.addCard('what is Purity\'s mother\'s name?', 'Anabel.')
    deck.addCard('what will Anabel never allow Tom to do?', 'Be an artist. \'Compete\' with her.')
    print(deck)

def _testSelect():
    deck = DeckModel('franzen', 'mwroffo')
    deck.selectCard(2)

def _testRemove():
    deck = DeckModel('franzen', 'mwroffo')
    deck.removeCardByTerm('who is purity\'s father?')
    print(deck) # should show 'Tom, the editor.' removed

    deck.removeCard(2)
    print(deck) # should show andreas card removed

def _testEdit():
    deck = DeckModel('franzen', 'mwroffo')
    print('INITIAL: ', deck, '\n')
    deck.editCardDefinition(1, newdefinition='Tom.')
    deck.editCardTerm(2, newterm='who murdered Annagret\'s stepfather?')
    deck.editCard(3, 'Purity\'s mother is?', '... Anabel.')
    print('FINAL: ', deck)

def _testAllTogether():
    pass

def _testBench():
    _testInit()
    # _testAdd()
    # _testSelect()
    # _testRemove()
    # _testEdit()
    pass

if __name__ == '__main__':
    _testBench()
