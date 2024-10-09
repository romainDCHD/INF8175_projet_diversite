from typing import Dict, Generator, List, Optional, Set, Tuple

from player_divercite import PlayerDivercite
from game_state_divercite import GameStateDivercite
from seahorse.game.action import Action
from seahorse.game.light_action import LightAction
from seahorse.game.game_layout.board import Piece
from seahorse.game.game_state import GameState
from seahorse.utils.custom_exceptions import MethodNotImplementedError


class HeuristicDivercite:
    def __init__(self, game_state: GameStateDivercite):
        self.game_state = game_state

    def evaluate_action(self, action: LightAction) -> float:
        """
        Évalue une action basée sur son potentiel de score et son impact sur l'adversaire.
        Favorise la création de Divercités et le blocage des opportunités adverses.

        Args:
            action (LightAction): L'action à évaluer.

        Returns:
            float: La valeur de l'action basée sur son impact potentiel.
        """
            
        piece = action.data["piece"]
        pos = action.data["position"]

        # Simuler l'application de l'action pour voir son impact
        future_state = self.game_state.apply_action(action)
        current_scores = self.game_state.scores
        future_scores = future_state.scores

        current_player_id = self.game_state.next_player.get_id()
        if(self.game_state.players[0]==current_player_id):
            opponent_id = self.game_state.players[1]
        else: 
            opponent_id = self.game_state.players[0]

        current_score = current_scores[current_player_id]
        future_score = future_scores[current_player_id]

        # 1. Bonus pour créer une Divercité
        if self.game_state.piece_type_match('C', pos) and future_state.check_divercite(pos):
            divercite_value = 5
        else:
            divercite_value = 0

        # 2. Bloquer une Divercité potentielle de l'adversaire
        block_value = self.block_opponent(future_state, pos, opponent_id)

        # 3. Évaluation de l'action en fonction des points immédiats et potentiels
        immediate_gain = future_score - current_score

        # Retourner la somme des points gagnés, avec priorité aux Divercités et au blocage
        return immediate_gain + divercite_value + block_value

    def block_opponent(self, future_state: GameStateDivercite, pos: Tuple[int, int], opponent_id: int) -> float:
        """
        Vérifie si l'action bloque une opportunité de Divercité de l'adversaire.

        Args:
            future_state (GameStateDivercite): L'état futur du jeu après l'action.
            pos (Tuple[int, int]): La position de la pièce placée.
            opponent_id (int): L'ID de l'adversaire.

        Returns:
            float: Une valeur supplémentaire si l'action bloque une Divercité de l'adversaire.
        """
        neighbors = future_state.get_neighbours(pos[0], pos[1])

        for _, (neighbor_piece, neighbor_pos) in neighbors.items():
            if isinstance(neighbor_piece, Piece) and neighbor_piece.get_owner_id() == opponent_id:
                if future_state.check_divercite(neighbor_pos):
                    # Si l'adversaire peut compléter une Divercité ici, ajouter un bonus de blocage
                    return 3  # Valeur du blocage, à ajuster selon l'importance
        return 0

    def best_action(self) -> LightAction:
        """
        Choisit la meilleure action parmi les actions possibles.

        Returns:
            LightAction: La meilleure action basée sur l'heuristique.
        """
        possible_actions = list(self.game_state.generate_possible_light_actions())

        # Évaluer chaque action et choisir la meilleure
        best_action = max(possible_actions, key=self.evaluate_action)
        
        return best_action
    
    def evaluate_state(self, state: GameStateDivercite) -> float:
        # Implémentez une évaluation de l'état de jeu
        print("ici", state.next_player.get_id())
        print(state.scores)
        return state.scores[state.next_player.get_id()]  # Exemple simple

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
            return 0, None

        v_star = float('-inf')
        m_star = None
        
        possible_actions = list(state.generate_possible_light_actions())

        heuristic=HeuristicDivercite(state)

        best_moves = sorted(possible_actions, key=lambda a: heuristic.evaluate_action(a), reverse=True)[:n]

        for action in best_moves:
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
            return 0, None

        v_star = float('inf')
        m_star = None

        possible_actions = list(state.generate_possible_light_actions())

        heuristic=HeuristicDivercite(state)

        best_moves = sorted(possible_actions, key=lambda a: heuristic.evaluate_action(a))[:n]

        for action in best_moves:
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
                
