"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return heuristic3(game=game, player=player)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return heuristic3(game=game, player=player) / (1 - heuristic2(game=game, player=player))


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return heuristic3(game=game, player=player) * 4 + heuristic2(game=game, player=player)


def heuristic1(game, player):
    return float(len(game.get_legal_moves()))


def heuristic2(game, player):
    legal_moves = list()
    for m in game.get_legal_moves():
        legal_moves.extend(game.forecast_move(m).get_legal_moves())
    return -float(len(legal_moves))


def heuristic3(game, player):
    legal_moves = list()
    for m in game.get_legal_moves():
        legal_moves.extend(game.forecast_move(m).get_legal_moves(player))
    return float(len(legal_moves))


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, score_fn=custom_score, search_depth=3, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    @staticmethod
    def _terminal_test(game, depth):
        """Terminal test function to be used in minimax search and alphabeta search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding a state of the
            game with forecast moves (e.g., player locations and blocked cells).

        depth : int
            An integer (i.e., 1, 2, 3,...) for the number of
            layers in the game tree to explore for fixed-depth search.

        Returns : boolean
            True if depth == 0 or no legal moves else False
        -------

        """
        return len(game.get_legal_moves()) == 0 or depth == 0

    def get_move(self, game, time_left, search_fn):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        search_fn : callable
            A function that implements some search algorithm and returns the
            board coordinates of the best move found in the current search.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            best_move = search_fn(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        return super().get_move(game=game, time_left=time_left, search_fn=self.minimax)

    def minimax(self, game, depth=None):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        # handling timeout
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        # search depth
        if depth is None:
            depth = self.search_depth

        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return -1, -1
        else:
            return max(legal_moves,
                       key=lambda m: self._min_value(game=game.forecast_move(move=m), depth=depth))

    def _min_value(self, game, depth):
        if self._terminal_test(game=game, depth=depth):
            return self.score(game, self)
        else:
            v = float("inf")
            for m in game.get_legal_moves():
                v = min(v, self._max_value(game=game.forecast_move(m), depth=depth-1))
            return v

    def _max_value(self, game, depth):
        if self._terminal_test(game=game, depth=depth):
            return self.score(game, self)
        else:
            v = float("-inf")
            for m in game.get_legal_moves():
                v = max(v, self._min_value(game=game.forecast_move(m), depth=depth-1))
            return v


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        return super().get_move(game=game, time_left=time_left, search_fn=self.alphabeta)

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        # handling timeout
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        # search depth
        if depth is None:
            depth = self.search_depth

        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return -1, -1
        else:
            return max(legal_moves,
                       key=lambda m: self._min_value(game=game.forecast_move(move=m), depth=depth,
                                                     alpha=alpha, beta=beta))

    def _max_value(self, game, depth, alpha, beta):
        if self._terminal_test(game=game, depth=depth):
            return self.score(game, self)
        else:
            v = float("-inf")
            for m in game.get_legal_moves():
                v = max(v, self._min_value(game=game.forecast_move(m), depth=depth-1,
                                           alpha=alpha, beta=beta))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

    def _min_value(self, game, depth, alpha, beta):
        if self._terminal_test(game=game, depth=depth):
            return self.score(game, self)
        else:
            v = float("inf")
            for m in game.get_legal_moves():
                v = min(v, self._max_value(game=game.forecast_move(m), depth=depth - 1,
                                           alpha=alpha, beta=beta))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v


if __name__ == '__main__':
    pass