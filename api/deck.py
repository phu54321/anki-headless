from server import app
from api.connection import col
from api.emit import emitError, emitResult


@app.route('/deck/list')
def list_deck():
    """ Returns list of deck names """
    return emitResult(col().decks.allNames())


@app.route('/deck/due')
def deck_due_list():
    """ Returns dictionary mapping from deck name to deck due. """

    tree = col().sched.deckDueTree()
    print(tree)
    # Flatten tree

    def _format_due_tree(tree):
        r = {}
        for deck in tree:
            deckName, _, nCnt, lCnt, rCnt, subTree = deck
            r[deckName] = {
                'newCount': nCnt,
                'lrnCount': lCnt,
                'revCount': rCnt,
                'subDecks': _format_due_tree(subTree)
            }
        return r

    ret = _format_due_tree(tree)
    return emitResult(ret)


@app.route('/deck/current/<deckname>')
def set_current_deck(deckname):
    """ Set 'current' deck. This is used for reviewing. """
    deck = col().decks.byName(deckname)
    if not deck:
        return emitError('No such deck')
    did = deck['id']
    col().decks.select(did)
    return emitResult(1)


@app.route('/deck/current')
def get_current_deck():
    """ Get 'current' deck. """
    deck = col().decks.current()
    return emitResult(deck['name'])
