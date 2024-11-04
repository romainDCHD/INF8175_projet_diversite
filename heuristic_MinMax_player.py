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
    
    
    def heuristic_piece_restantes(self, pieces_left):
        """
        Privilégie l'équi-répartition des ressources et tours pour ne pas les gaspiller au début.
        
        """
        piece_bonus = 0

        for piece, n_piece in pieces_left.items():
            # Vérifier si c'est une "tour" 
            is_tower = 'C' in piece

            if is_tower:
                if n_piece == 2:
                    piece_bonus += 2  # Bonus maximal si 2 pièces restantes (pour les tours)
                elif n_piece == 1:
                    piece_bonus += 1  # Bonus réduit si 1 pièce restante (pour les tours)
                else:
                    piece_bonus += 0  # Pas de bonus si 0 pièce restante
            else:
                if n_piece == 3:
                    piece_bonus += 3  # Bonus maximal si 3 pièces restantes
                elif n_piece == 2:
                    piece_bonus += 2  # Bonus réduit si 2 pièces restantes
                elif n_piece == 1:
                    piece_bonus += 1  # Bonus plus faible si 1 pièce restante
                else:
                    piece_bonus += 0  # Pas de bonus si 0 pièce restante
        
        # On pondère le score de l'heuristique pour qu'elle ai un poids proportionnel au score
        heuristique = piece_bonus
        return heuristique
    
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


    def heuritic_empechement_diversite(self, state: GameState):
        """
        Permet de bloquer les diversités adverses
        """

        # # Identifier le joueur Max (celui qui commence la partie)
        # max_player_id = 1 if self.get_id() == 1 else 0  # Le joueur Max commence la partie
        # opponent_symbol = 'W' if max_player_id == 0 else 'B'  # L'adversaire est celui opposé au joueur Max
        # player_symbol = 'B' if opponent_symbol == 'W' else 'W'  # Symbole du joueur Max (opposé à l'adversaire)
        
        players =  state.players
        for player in players:
            print("all_players: ", player.get_id()) 
        print("state.get_next_player: ", state.next_player.get_id())
        print("self.get_id() : ", self.get_id())
        
        if state.next_player.get_id() == players[0].get_id():
            player_symbol = 'W'
            opponent_symbol = 'B'            
        elif state.next_player.get_id() == players[1].get_id():
            player_symbol = 'B'
            opponent_symbol = 'W'
        else :
            print("ID problems!!!!!!!!!!!")
        
        board = state.get_rep().get_env()  # Représentation du plateau

        placement_bonus = 0  # Bonus pour remplir la condition autour d'une tour adverse

        # Pour chaque pièce du plateau 
        for pos, piece in board.items():
            # Récupérer les infos de la pièce : ex. RCB = rouge, tour, joueur blanc
            piece_type = piece.get_type()

            # Si c'est une tour adverse
            if piece_type[1] == 'C' and piece_type[2] == opponent_symbol:
                tower_color = piece_type[0]  # La couleur de la tour

                # Vérifier les cases adjacentes à la tour adverse pour y trouver des ressources
                neighbors = self.get_adjacent_positions(pos, state)
                # print ("len(neighbors) : ", len(neighbors)) 
                # Si 4 pièces sont autour de cette tour
                if len(neighbors) == 4:
                    different_colors = set()  # Utiliser un ensemble pour les couleurs différentes
                    player_resource_present = 0  # Vérifier si une ressource du joueur Max est présente
                    piece_like_tower_colors = 0  # nombre de ressources de la couleur de la tour

                    for neighbor in neighbors:
                        # Si une ressource est présente sur la case adjacente
                        if neighbor in board:  
                            neighbor_piece = board[neighbor].get_type()  # Récupérer les infos de la pièce
                            neighbor_color = neighbor_piece[0]  # La couleur de la ressource
                            # print("neighbor_piece : ", neighbor_piece)
                            
                            different_colors.add(neighbor_color)
                            
                            # Si la ressource a la même couleur que la tour, on incrémente
                            if neighbor_piece[0] == tower_color:
                                piece_like_tower_colors += 1
                            
                            # Vérifier si la ressource appartient au joueur Max
                            if neighbor_piece[2] == player_symbol:
                                player_resource_present += 1

                    # Éviter de compléter la diversité avec une troisième couleur différente
                    if len(different_colors) == 4 :
                        # print("Empêchement de diversité, pas d'ajout de ressource")
                        return 0

                    # Si la diversité est partiellement remplie et que c'est avantageux pour le joueur Max
                    if len(different_colors) == 3 and piece_like_tower_colors <= 1:
                        # Si peu de pièces du joueur Max sont présentes
                        if player_resource_present == 1:
                            # print(f"50 points")
                            placement_bonus += 50  # Bonus fort si la condition est remplie
                        # Sinon, moins de points (pour éviter de cibler cet objectif)
                        if player_resource_present > 1:
                            # print(f"20 points")
                            placement_bonus += 20  # Bonus réduit si la condition est remplie
                        
        # L'heuristique est basée sur le score du joueur + un bonus pour la condition spéciale
        heuristic =  placement_bonus

        return heuristic

    def heuristic_score(self, state: GameState):
        """
        Privilégie l'équi-répartition des ressources et tours pour ne pas les gaspiller au début.
        
        """
        ########## Accéder aux paramètres du jeu pour évaluer les heuristiques ##########
        # Score actuel du joueur
        player_score = state.scores[self.get_id()]
        print("***\nplayer score : ", player_score)

        # Pièces restantes du joueur
        pieces_left = state.players_pieces_left[self.get_id()]
        print("pieces_left : ", pieces_left)

        ########## Calcul des heuristiques ##########
        # Bonus en fonction du nombre de pièces restantes
        piece_restantes = self.heuristic_piece_restantes(pieces_left)        
        # print("piece_restantes : ", piece_restantes)
        
        empechement_diversite = self.heuritic_empechement_diversite(state)
        print("empechement_diversite : ", empechement_diversite)


        ########## Intégration des heuristique dans notre heuristique finale ##########
        heuristic = player_score  + empechement_diversite

        print("score heuristique :", heuristic)
        return heuristic

        
    def max_value(self, state: GameState, depth, max_depth, alpha, beta):
        """
        Incarne notre Max player
        """
        if self.is_terminal(depth, max_depth):
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
        if self.is_terminal(depth, max_depth):  
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
