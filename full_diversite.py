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
    
    
    
    ############## Empechement diversite ##################
     # Fonction qui retourne les positions adjacentes
    def get_adjacent_positions(self, pos, state: GameState):
        """
        Retourne les positions adjacentes à une position donnée sur le plateau.
        """
        x, y = pos
        adjacent_positions = [
            (x - 1, y),  # Haut
            (x + 1, y),  # Bas
            (x, y - 1),  # Gauche
            (x, y + 1)   # Droite
        ]

        # Filtrer les positions qui ne sont pas sur le plateau (en dehors des limites)
        valid_positions = [p for p in adjacent_positions if self.is_within_bounds(p, state)]
        
        return valid_positions

    # Fonction qui vérifie si une position est dans les limites du plateau
    def is_within_bounds(self, pos, state: GameState):
        """
        Vérifie si une position est dans les limites du plateau.
        """
        x, y = pos
        dim_x, dim_y = state.get_rep().get_dimensions()  # Obtenir les dimensions du plateau
        return 0 <= x < dim_x and 0 <= y < dim_y


    def heuristic_full_diversite(self, state: GameState):
        """
        Favorise la diversité des ressources de couleurs autour des tours du joueur Max.
        Le bonus est attribué en fonction du nombre de ressources adjacentes et de leur diversité de couleurs,
        mais seulement s'il n'y a pas de redondance.
        """

        player_symbol = 'W' if state.next_player.get_id() == state.players[0].get_id() else 'B'
        board = state.get_rep().get_env()  # Représentation du plateau
        total_diversity_bonus = 0

        # Parcours des pièces du plateau
        for pos, piece in board.items():
            piece_type = piece.get_type()

            # Vérifier si c'est une tour du joueur Max
            if piece_type[1] == 'C' and piece_type[2] == player_symbol:
                print(f"Tour {player_symbol} détectée en {pos}")
                neighbors = self.get_adjacent_positions(pos, state)
                different_colors = set()
                occupied_count = 0
                has_duplicates = False

                # Analyser les couleurs autour de la tour
                for neighbor in neighbors:
                    if neighbor in board:  # Si une ressource est présente
                        neighbor_piece = board[neighbor].get_type()
                        neighbor_color = neighbor_piece[0]

                        # Vérifier s'il y a un doublon
                        if neighbor_color in different_colors:
                            has_duplicates = True
                            print(f"Doublon détecté pour la couleur {neighbor_color} autour de la tour {pos}. Score annulé.")
                            break  # Arrêter le calcul pour cette tour en cas de doublon
                        
                        # Ajouter la couleur unique au set
                        different_colors.add(neighbor_color)
                        occupied_count += 1
                        print("Ressource trouvée :", neighbor_piece)
                
                # Calculer le bonus uniquement s'il n'y a aucun doublon
                if not has_duplicates:
                    print(f"Couleurs uniques autour de la tour {pos} : {different_colors}")
                    if occupied_count == 4:
                        total_diversity_bonus += 50 
                    elif occupied_count == 3:
                        total_diversity_bonus += 20
                    elif occupied_count == 2:
                        total_diversity_bonus += 5
                    elif occupied_count == 1:
                        total_diversity_bonus += 1  # Bonus minimal pour une seule ressource adjacente

        return total_diversity_bonus



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
        
        full_diversite = self.heuristic_full_diversite(state)
        # print("score full_diversite : ", full_diversite)


        ########## Intégration des heuristique dans notre heuristique finale ##########
        heuristic =  full_diversite

        print("score heuristique :", heuristic)
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
        
                
        value, move = self.max_value(current_state, 0, 2, float('-inf'), float('inf'))
        return move
                
        raise MethodNotImplementedError()
