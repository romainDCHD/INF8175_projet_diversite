
from player_divercite import PlayerDivercite
from game_state_divercite import GameStateDivercite
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from seahorse.utils.custom_exceptions import MethodNotImplementedError

class MyPlayer(PlayerDivercite):
    """
    Player class for Divercite game that makes random moves.

    Attributes:
        piece_type (str): piece type of the player
    """

    def __init__(self, piece_type: str, name: str = "MyPlayer"):
        """
        Initialize the PlayerDivercite instance.

        Args:
            piece_type (str): Type of the player's game piece
            name (str, optional): Name of the player (default is "bob")
            time_limit (float, optional): the time limit in (s)
        """
        super().__init__(piece_type, name)
    
    def is_terminal(self, state: GameState, depth, max_depth):
        """
        Fonction nous permettant de savoir si on a atteint la profondeur souhaitée
        """
        
        return depth == max_depth or state.is_done()
        
    def max_value(self, state: GameState, depth, max_depth, alpha, beta, n):
        """
        Incarne notre Max player
        """
        if self.is_terminal(state, depth, max_depth):
            score = state.scores[self.get_id()]
            return score, None

        v_star = float('-inf')
        m_star = None
        
        possible_actions = state.generate_possible_light_actions()
        action_scores=[]

        for action in possible_actions : 
            state_temp = state.apply_action(action)
            action_scores.append((action, state_temp.scores[self.get_id()]))
        action_scores.sort(key=lambda x: x[1], reverse=True)  # Trier par score décroissant
        best_actions = [action for action, score in action_scores[:n]]

        for action in best_actions:
            new_state = state.apply_action(action)
            v, _ = self.min_value(new_state, depth + 1, max_depth, alpha, beta, n)

            if v > v_star:
                v_star = v
                m_star = action
            
            if v_star >= beta:
                break
            
        alpha = max(alpha, v_star)
        return v_star, m_star
    

    # Minimize value for MIN player
    def min_value(self, state: GameState, depth, max_depth, alpha, beta, n):
        if self.is_terminal(state, depth, max_depth):
            score = state.scores[self.get_id()]
            return score, None

        v_star = float('inf')
        m_star = None
        
        action_scores=[]
        possible_actions = state.generate_possible_light_actions()
        for action in possible_actions : 
            state_temp = state.apply_action(action)
            action_scores.append((action, state_temp.scores[self.get_id()]))
        action_scores.sort(key=lambda x: x[1])  # Trier par score croissant
        best_actions = [action for action, score in action_scores[:n]]

        for action in best_actions:
            new_state = state.apply_action(action)
            v, _ = self.max_value(new_state, depth + 1, max_depth, alpha, beta, n)

            if v < v_star:
                v_star = v
                m_star = action

            if v_star <= alpha:
                break

            beta = min(beta, v_star)

        return v_star, m_star
    

    def compute_action(self, current_state: GameState, remaining_time: int = 1e9, n=10, **kwargs) -> Action:
        """
        Use the minimax algorithm to choose the best action based on the heuristic evaluation of game states.

        Args:
            current_state (GameState): The current game state.

        Returns:
            Action: The best action as determined by minimax.
        """

        #TODO
        # On commence par un minmax d'une profondeur de 2
        
                
        value, move = self.max_value(current_state, 0, 4, float('-inf'), float('inf'), n)
        return move
                
        raise MethodNotImplementedError()
