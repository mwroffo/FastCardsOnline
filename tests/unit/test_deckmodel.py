"""
Aug 2018 mwroffo
test_deckmodel.py, a functional testing suite for FastCards' `DeckModel`
class, which provides a layer of abstraction between
view functions and SQLAlchemy.
"""

def test_deckmodel_init(test_client, test_db):
    """ GIVEN a `DeckModel` constructor,
    WHEN a deckname is passed to that constructor,
    THEN confirm that that DeckModel exists,
    AND that DeckModel """
    pass

def test_deckmodel_add_card():
    """ GIVEN `DeckModel`'s `addCard` method,
    WHEN a `Card` model is initialized and passed to addCard,
    THEN check whether the card exists in the DeckModel
    (i.e. that the table card contains a row where deckname=DeckModel.deckname) """
    pass

### Not worried about this functionality until later stories.
# def test_deckmodel_remove_card():
#     """ GIVEN `DeckModel`'s `removeCard` method,
#     WHEN a `Card` model is passed to `removeCard`,
#     THEN check that the card """
#     pass