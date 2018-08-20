"""
test_core.py
Functional testing suite for FastCards' core functionalities, 
including generating the browse/edit view of a deck, and reviewing a deck.
"""

def test_browse_edit(test_client, init_db):
    """ GIVEN app.main.routes.browse_edit(),
    WHEN browse_edit is called for a new deck,
    THEN show that:
        - The FastCards header rendered.
        - a deckname textfield rendered.
        - an entry_row with new_term field and new_definition field rendered
        - a "remove" button rendered, which calls deckmodel.removeCard() to 
            use HiddenField to pass card_id to Submit('Remove'), which use calls
            Card.query.get(card_id).delete()
        - an "add card" button rendered, which does the following:
            - confirms that a deck object associated with current_user exists.
            - It inits the new card and appends it to Deck, commits the change.
            - submitting the change should cause a page reload, causing the 
                new card to render in an editable textfield. No need for AJAX, right?
        - a "save this deck" button commits changes to db.
        - a "done" link sends a request that receives the index page as response.
    """

    response = test_client.post('/browse_edit',
        data=dict(deckname_field='Fall Out Boy songs'),
        follow_redirects=True)
    assert b'FastCards' in response.data # confirm header rendered
    assert b'<input type' in response.data # confirm text fields
    assert b'This is side one.' in response.data # confirm default text rendered
    assert b'Remove' in response.data # confirm remove buttons rendered
    assert b'Enter a new term' in response.data # confirm entry_row rendered term
    assert b'Enter a new definition' in response.data # confirm entry_row render definition
    # TODO write tests for requests that come from the now-loaded browse_edit page.

def test_browse_edit_preexisting_deck(test_client):
    """ 
    GIVEN app.main.routes.browse_edit() AND a deck with previous cards,
    WHEN browse_edit is called for a preexisting deck,
    THEN show that:
        - an "add card" button rendered, which does the following:
            - confirms that a deck object associated with current_user exists.
            - It appends the new card to Deck.
            - and finally, clears the textfields for a new card entry.
        - a "save this deck" button does the following:
            + for each CardForm, if there are changes to either term or definition,
                update the corresponding Card. 
            + updates User via `u.update({"Ligt that smoke.": "Light that smoke."})
        - a "done" link sends a request that receives the index page as response.
    """
    pass
