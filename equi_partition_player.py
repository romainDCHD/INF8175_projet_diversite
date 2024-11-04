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
    
    def is_terminal(self, state: GameState, depth, max_depth):
        """
        Fonction nous permettant de savoir si on a atteint la profondeur souhaitée
        """
        return depth == max_depth or state.is_done()
    
    
    def heuristic_piece_restantes(self, pieces_left):
        """
        Favorise une répartition équilibrée des ressources et des tours en fonction de leurs couleurs.
        Un bonus est attribué en fonction de l'équirépartition des quantités de chaque couleur.
        La séquence des ajouts est : tour, ressource, ressource, tour.
        """
        color_counts_resources = {"R": 0, "G": 0, "B": 0, "Y": 0}  # Comptage des ressources par couleur
        color_counts_towers = {"R": 0, "G": 0, "B": 0, "Y": 0}     # Comptage des tours par couleur

        # Comptage des ressources et tours par couleur
        for piece, n_piece in pieces_left.items():
            color = piece[0]  # Première lettre pour identifier la couleur
            is_tower = 'C' in piece  # Vérifier si c'est une "tour"

            if is_tower:
                color_counts_towers[color] += n_piece
            else:
                color_counts_resources[color] += n_piece

        # Pour les ressources
        values_resources = list(color_counts_resources.values())
        total_resources = sum(values_resources)
        average_resources = total_resources / len(values_resources) if total_resources > 0 else 0
        resources_deviation = int(sum(abs(value - average_resources) for value in values_resources))

        # Pour les tours
        values_towers = list(color_counts_towers.values())
        total_towers = sum(values_towers)
        average_towers = total_towers / len(values_towers) if total_towers > 0 else 0
        towers_deviation = int(sum(abs(value - average_towers) for value in values_towers))

        piece_bonus = 0
        
        # if towers_deviation <= 1 and resources_deviation <= 1:
        #     piece_bonus = 2
        # elif towers_deviation <= 2 and resources_deviation <= 2:
        #     piece_bonus = 1

        # # Vérification des phases de jeu
        total_pieces = total_resources + total_towers
        if total_pieces >= 16:
            # Favoriser l'ajout de tours
            if towers_deviation <= 1 and resources_deviation <= 0:
                piece_bonus = 2
            elif towers_deviation <= 2 and resources_deviation <= 0:
                piece_bonus = 1
            
        elif 8 <= total_pieces < 16:
            # Favoriser l'ajout de ressources
            if resources_deviation <= 1 and towers_deviation <= 1:
                piece_bonus = 2
            elif resources_deviation <= 2 and towers_deviation <= 1:
                piece_bonus = 1
            
        elif 4 <= total_pieces < 8:
            # Retourner à favoriser les tours
            if towers_deviation <= 2 and resources_deviation <= 2:
                piece_bonus = 2
            elif towers_deviation <= 3 and resources_deviation <= 2:
                piece_bonus = 1
            
        else:
            # Favoriser les ressources
            if resources_deviation <= 3 and towers_deviation <= 2:
                piece_bonus = 2
            elif resources_deviation <= 4 and towers_deviation <= 2:
                piece_bonus = 1

        return piece_bonus



    

    def heuristic_score(self, state: GameState):
        """
        Privilégie l'équi-répartition des ressources et tours pour ne pas les gaspiller au début.
        
        """
        ########## Accéder aux paramètres du jeu pour évaluer les heuristiques ##########
        # Score actuel du joueur
        player_score = state.scores[self.get_id()]
        # print("***\nplayer score : ", player_score)

        # Pièces restantes du joueur
        pieces_left = state.players_pieces_left[self.get_id()]
        # print("pieces_left : ", pieces_left)

        ########## Calcul des heuristiques ##########
        # Bonus en fonction du nombre de pièces restantes
        piece_restantes = self.heuristic_piece_restantes(pieces_left)
        
        ########## Intégration des heuristique dans notre heuristique finale ##########
        heuristic = player_score + piece_restantes*3

        # print("score heuristique :", heuristic)
        return heuristic

        
    def max_value(self, state: GameState, depth, max_depth, alpha, beta):
        """
        Incarne notre Max player
        """
        if self.is_terminal(state, depth, max_depth):
            # print("\n**************** joueur Max ***************")
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
        if self.is_terminal(state, depth, max_depth):  
            # print("\n############## Joueur Min ###############")
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
        
                
        value, move = self.max_value(current_state, 0, 4, float('-inf'), float('inf'))
        return move
                
        raise MethodNotImplementedError()
