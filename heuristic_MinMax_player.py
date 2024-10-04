from player_divercite import PlayerDivercite
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from game_state_divercite import GameStateDivercite
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
    
    def is_terminal(self, depth, max_depth):
        """
        Fonction nous permettant de savoir si on a atteint la profondeur souhaitée
        """
        return depth == max_depth
    
    
    def heuristic_score(self, state: GameState):
        """
        Fonction d'heuristique personnalisée pour évaluer un état du jeu.

        Args:
            state (GameState): L'état actuel du jeu.

        Returns:
            int: Le score évalué basé sur l'heuristique.
        """
        # 1. Accéder au score actuel du joueur
        player_score = state.scores[self.get_id()]

        # 2. Accéder aux pièces restantes du joueur
        pieces_left = state.players_pieces_left[self.get_id()]

        # 3. Vérifier le nombre de tuiles restantes pour la couleur spécifique
        tiles_left_for_color = pieces_left.get((piece_color, "some_type"), 0)  # Supposons que "some_type" est un autre attribut de la pièce

        # L'heuristique donne un avantage si le joueur a plus de tuiles de cette couleur
        tile_bonus = tiles_left_for_color * 5  # Par exemple, chaque tuile restante donne un bonus de 5 points

        # Combiner le score du joueur avec le bonus basé sur le nombre de tuiles restantes
        heuristic = player_score + tile_bonus

        print ("score heuristique :", heuristic)
        return heuristic


    
        
    def max_value(self, state: GameState, depth, max_depth, alpha, beta):
        """
        Incarne notre Max player
        """
        if self.is_terminal(depth, max_depth):
            score = self.heuristic_score(state)
            return score, None

        v_star = float('-inf')
        m_star = None
        
        possible_actions = state.generate_possible_light_actions()

        for action in possible_actions:
            new_state = state.apply_action(action)
            v, _ = self.min_value(new_state, depth + 1, max_depth, alpha, beta)

            if v > v_star:
                v_star = v
                m_star = action
                alpha = max(alpha, v_star)
            
            if (v_star >= beta):
                return v_star, m_star   

        return v_star, m_star

    # Minimize value for MIN player
    def min_value(self, state: GameState, depth, max_depth, alpha, beta):
        if self.is_terminal(depth, max_depth):  
            score = self.heuristic_score(state)
            return score, None

        v_star = float('inf')
        m_star = None
        
        possible_actions = state.generate_possible_light_actions()

        for action in possible_actions:
            new_state = state.apply_action(action)
            v, _ = self.max_value(new_state, depth + 1, max_depth, alpha, beta)

            if v < v_star:
                v_star = v
                m_star = action
                beta = min(beta, v_star)
                
            if (v_star <= alpha):
                return v_star, m_star

        return v_star, m_star

    def compute_action(self, current_state: GameState, remaining_time: int = 1e9, **kwargs) -> Action:
        """
        Use the minimax algorithm to choose the best action based on the heuristic evaluation of game states.

        Args:
            current_state (GameState): The current game state.

        Returns:
            Action: The best action as determined by minimax.
        """

        #TODO
        # On commence par un 𝖺𝗅𝗉𝗁𝖺𝖡𝖾𝗍𝖺𝖲𝖾𝖺𝗋𝖼𝗁 d'une profondeur de 2
        
                
        value, move = self.max_value(current_state, 0, 4, float('-inf'), float('inf'))
        return move
                
        raise MethodNotImplementedError()
