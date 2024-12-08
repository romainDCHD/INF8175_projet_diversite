import re
import matplotlib.pyplot as plt

# Exemple de contenu du fichier log
log_content = """
ng for listeners 1 out of 1 are connected.
2024-12-07 17:46:03.169 | INFO     | seahorse.game.io_stream:handle_identify:212 - Identifying a listener
2024-12-07 17:46:03.171 | INFO     | seahorse.game.io_stream:handle_identify:213 - __GUI__1733611563162
2024-12-07 17:46:03.172 | DEBUG    | seahorse.game.io_stream:handle_identify:214 - Deserialized data {'identifier': '__GUI__1733611563162'}
2024-12-07 17:46:03.243 | INFO     | seahorse.game.io_stream:stop:333 - Starting match
2024-12-07 17:46:03.248 | INFO     | seahorse.game.master:play_game:129 - Player : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:46:03.250 | INFO     | seahorse.game.master:play_game:129 - Player : random_player_divercite_2 - 1299775648336
2024-12-07 17:46:03.254 | INFO     | seahorse.game.master:play_game:132 - Player now playing : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:46:03.268 | INFO     | seahorse.game.master:step:97 - time : 900
2024-12-07 17:46:24.520 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  🅆
◇  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  ▢
◇  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  ▢
◇  ◇  ◇  ◇  ◇  
  ▢  ▢  ▢  ▢
◇  ◇  ◇  ◇  ◇

2024-12-07 17:46:24.548 | INFO     | seahorse.game.master:play_game:132 - Player now playing : random_player_divercite_2 - 1299775648336
2024-12-07 17:46:24.558 | INFO     | seahorse.game.master:step:97 - time : 900
2024-12-07 17:46:24.561 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  🅆
◇  ◆  ◇  ◇  ◇  
  ▢  ▢  ▢  ▢
◇  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  ▢
◇  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  ▢
◇  ◇  ◇  ◇  ◇

2024-12-07 17:46:24.583 | INFO     | seahorse.game.master:play_game:132 - Player now playing : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:46:24.591 | INFO     | seahorse.game.master:step:97 - time : 878.749082326889
2024-12-07 17:46:44.848 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◇  ◇  ◇  ◇
  ▢  ▢  🅆  🅆
◇  ◆  ◇  ◇  ◇
  ▢  ▢  ▢  ▢
◇  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  ▢
◇  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  ▢
◇  ◇  ◇  ◇  ◇

2024-12-07 17:46:44.861 | INFO     | seahorse.game.master:play_game:132 - Player now playing : random_player_divercite_2 - 1299775648336
2024-12-07 17:46:44.884 | INFO     | seahorse.game.master:step:97 - time : 899.9973454475403
2024-12-07 17:46:44.887 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◇  ◇  ◇  ◇
  ▢  ▢  🅆  🅆
◇  ◆  ◇  ◇  ◇
  ▢  ▢  ▢  ▢
◇  ◇  ◇  ◇  ◇  
  ▢  ▢  ▢  ▢
◇  ◇  ◇  ◇  ◇
  ▢  🄱  ▢  ▢
◇  ◇  ◇  ◇  ◇

2024-12-07 17:46:44.907 | INFO     | seahorse.game.master:play_game:132 - Player now playing : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:46:44.918 | INFO     | seahorse.game.master:step:97 - time : 858.492104768753
2024-12-07 17:47:06.973 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◇  ◇  ◇  ◇
  ▢  ▢  🅆  🅆
◇  ◆  ◇  ◇  ◇
  ▢  ▢  ▢  🅆
◇  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  ▢
◇  ◇  ◇  ◇  ◇
  ▢  🄱  ▢  ▢
◇  ◇  ◇  ◇  ◇  

2024-12-07 17:47:07.004 | INFO     | seahorse.game.master:play_game:132 - Player now playing : random_player_divercite_2 - 1299775648336
2024-12-07 17:47:07.019 | INFO     | seahorse.game.master:step:97 - time : 899.9942035675049
2024-12-07 17:47:07.022 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◇  ◇  ◆  ◇
  ▢  ▢  🅆  🅆
◇  ◆  ◇  ◇  ◇  
  ▢  ▢  ▢  🅆
◇  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  ▢
◇  ◇  ◇  ◇  ◇
  ▢  🄱  ▢  ▢
◇  ◇  ◇  ◇  ◇

2024-12-07 17:47:07.041 | INFO     | seahorse.game.master:play_game:132 - Player now playing : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:47:07.051 | INFO     | seahorse.game.master:step:97 - time : 836.4375133514404
2024-12-07 17:47:27.373 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◇  ◇  ◆  ◇
  ▢  🅆  🅆  🅆
◇  ◆  ◇  ◇  ◇
  ▢  ▢  ▢  🅆
◇  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  ▢
◇  ◇  ◇  ◇  ◇
  ▢  🄱  ▢  ▢
◇  ◇  ◇  ◇  ◇  

2024-12-07 17:47:27.402 | INFO     | seahorse.game.master:play_game:132 - Player now playing : random_player_divercite_2 - 1299775648336
2024-12-07 17:47:27.416 | INFO     | seahorse.game.master:step:97 - time : 899.9912028312683
2024-12-07 17:47:27.420 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◇  ◇  ◆  ◇
  ▢  🅆  🅆  🅆
◇  ◆  ◇  ◇  ◇  
  🄱  ▢  ▢  🅆
◇  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  ▢
◇  ◇  ◇  ◇  ◇
  ▢  🄱  ▢  ▢
◇  ◇  ◇  ◇  ◇

2024-12-07 17:47:27.436 | INFO     | seahorse.game.master:play_game:132 - Player now playing : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:47:27.445 | INFO     | seahorse.game.master:step:97 - time : 816.1153712272644
2024-12-07 17:47:45.404 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◇  ◇  ◆  ◇
  🅆  🅆  🅆  🅆
◇  ◆  ◇  ◇  ◇
  🄱  ▢  ▢  🅆
◇  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  ▢
◇  ◇  ◇  ◇  ◇  
  ▢  🄱  ▢  ▢
◇  ◇  ◇  ◇  ◇

2024-12-07 17:47:45.430 | INFO     | seahorse.game.master:play_game:132 - Player now playing : random_player_divercite_2 - 1299775648336
2024-12-07 17:47:45.444 | INFO     | seahorse.game.master:step:97 - time : 899.9887406826019
2024-12-07 17:47:45.465 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◇  ◇  ◆  ◇  
  🅆  🅆  🅆  🅆
◇  ◆  ◇  ◇  ◇
  🄱  ▢  ▢  🅆
◆  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  ▢
◇  ◇  ◇  ◇  ◇
  ▢  🄱  ▢  ▢
◇  ◇  ◇  ◇  ◇

2024-12-07 17:47:45.478 | INFO     | seahorse.game.master:play_game:132 - Player now playing : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:47:45.487 | INFO     | seahorse.game.master:step:97 - time : 798.1559541225433
2024-12-07 17:48:28.427 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◇  ◇  ◆  ◆
  🅆  🅆  🅆  🅆
◇  ◆  ◇  ◇  ◇
  🄱  ▢  ▢  🅆
◆  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  ▢
◇  ◇  ◇  ◇  ◇  
  ▢  🄱  ▢  ▢
◇  ◇  ◇  ◇  ◇

2024-12-07 17:48:28.452 | INFO     | seahorse.game.master:play_game:132 - Player now playing : random_player_divercite_2 - 1299775648336
2024-12-07 17:48:28.464 | INFO     | seahorse.game.master:step:97 - time : 899.9681658744812
2024-12-07 17:48:28.468 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◇  ◇  ◆  ◆
  🅆  🅆  🅆  🅆
◇  ◆  ◇  ◇  ◇
  🄱  ▢  ▢  🅆  
◆  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  ▢
◇  ◇  ◆  ◇  ◇
  ▢  🄱  ▢  ▢
◇  ◇  ◇  ◇  ◇

2024-12-07 17:48:28.489 | INFO     | seahorse.game.master:play_game:132 - Player now playing : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:48:28.497 | INFO     | seahorse.game.master:step:97 - time : 755.2150712013245
2024-12-07 17:49:47.754 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◇  ◆  ◆  ◆
  🅆  🅆  🅆  🅆
◇  ◆  ◇  ◇  ◇  
  🄱  ▢  ▢  🅆
◆  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  ▢  
◇  ◇  ◆  ◇  ◇
  ▢  🄱  ▢  ▢  
◇  ◇  ◇  ◇  ◇  

2024-12-07 17:49:48.025 | INFO     | seahorse.game.master:play_game:132 - Player now playing : random_player_divercite_2 - 1299775648336
2024-12-07 17:49:48.155 | INFO     | seahorse.game.master:step:97 - time : 899.9636414051056
2024-12-07 17:49:48.161 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◇  ◆  ◆  ◆  
  🅆  🅆  🅆  🅆
◇  ◆  ◇  ◇  ◇  
  🄱  ▢  ▢  🅆
◆  ◇  ◇  ◇  ◇  
  ▢  ▢  ▢  ▢
◇  ◇  ◆  ◇  ◇
  ▢  🄱  ▢  ▢
◇  ◇  ◆  ◇  ◇  

2024-12-07 17:49:48.310 | INFO     | seahorse.game.master:play_game:132 - Player now playing : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:49:48.328 | INFO     | seahorse.game.master:step:97 - time : 675.9578804969788
2024-12-07 17:51:51.134 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◇  ◆  ◆  ◆
  🅆  🅆  🅆  🅆
◇  ◆  ◇  ◇  ◇
  🄱  ▢  ▢  🅆
◆  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  ▢
◇  ◇  ◆  ◇  ◇
  ▢  🄱  ▢  ▢
◇  ◆  ◆  ◇  ◇  

2024-12-07 17:51:51.163 | INFO     | seahorse.game.master:play_game:132 - Player now playing : random_player_divercite_2 - 1299775648336
2024-12-07 17:51:51.187 | INFO     | seahorse.game.master:step:97 - time : 899.9586265087128
2024-12-07 17:51:51.190 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◇  ◆  ◆  ◆
  🅆  🅆  🅆  🅆
◇  ◆  ◇  ◇  ◇  
  🄱  ▢  ▢  🅆
◆  ◇  ◇  ◇  ◇  
  ▢  ▢  ▢  ▢
◇  ◆  ◆  ◇  ◇
  ▢  🄱  ▢  ▢
◇  ◆  ◆  ◇  ◇  

2024-12-07 17:51:51.649 | INFO     | seahorse.game.master:play_game:132 - Player now playing : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:51:51.670 | INFO     | seahorse.game.master:step:97 - time : 553.1529948711395
2024-12-07 17:52:30.785 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◆  ◆  ◆  ◆
  🅆  🅆  🅆  🅆  
◇  ◆  ◇  ◇  ◇
  🄱  ▢  ▢  🅆
◆  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  ▢
◇  ◆  ◆  ◇  ◇  
  ▢  🄱  ▢  ▢
◇  ◆  ◆  ◇  ◇

2024-12-07 17:52:30.824 | INFO     | seahorse.game.master:play_game:132 - Player now playing : random_player_divercite_2 - 1299775648336
2024-12-07 17:52:30.940 | INFO     | seahorse.game.master:step:97 - time : 899.9561169147491
2024-12-07 17:52:31.043 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◆  ◆  ◆  ◆
  🅆  🅆  🅆  🅆  
◇  ◆  ◇  ◇  ◇  
  🄱  ▢  ▢  🅆
◆  ◇  ◇  ◇  ◇  
  ▢  ▢  ▢  ▢
◇  ◆  ◆  ◇  ◇
  🄱  🄱  ▢  ▢
◇  ◆  ◆  ◇  ◇  

2024-12-07 17:52:31.195 | INFO     | seahorse.game.master:play_game:132 - Player now playing : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:52:31.221 | INFO     | seahorse.game.master:step:97 - time : 514.0391118526459
2024-12-07 17:52:55.637 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◆  ◆  ◆  ◆
  🅆  🅆  🅆  🅆
◇  ◆  ◆  ◇  ◇
  🄱  ▢  ▢  🅆
◆  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  ▢
◇  ◆  ◆  ◇  ◇
  🄱  🄱  ▢  ▢  
◇  ◆  ◆  ◇  ◇

2024-12-07 17:52:55.669 | INFO     | seahorse.game.master:play_game:132 - Player now playing : random_player_divercite_2 - 1299775648336
2024-12-07 17:52:55.687 | INFO     | seahorse.game.master:step:97 - time : 899.8542313575745
2024-12-07 17:52:55.692 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◆  ◆  ◆  ◆  
  🅆  🅆  🅆  🅆
◇  ◆  ◆  ◆  ◇
  🄱  ▢  ▢  🅆
◆  ◇  ◇  ◇  ◇  
  ▢  ▢  ▢  ▢
◇  ◆  ◆  ◇  ◇  
  🄱  🄱  ▢  ▢  
◇  ◆  ◆  ◇  ◇

2024-12-07 17:52:56.089 | INFO     | seahorse.game.master:play_game:132 - Player now playing : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:52:56.110 | INFO     | seahorse.game.master:step:97 - time : 489.62368512153625
2024-12-07 17:53:20.922 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◆  ◆  ◆  ◆
  🅆  🅆  🅆  🅆
◇  ◆  ◆  ◆  ◆
  🄱  ▢  ▢  🅆
◆  ◇  ◇  ◇  ◇
  ▢  ▢  ▢  ▢  
◇  ◆  ◆  ◇  ◇
  🄱  🄱  ▢  ▢
◇  ◆  ◆  ◇  ◇

2024-12-07 17:53:20.955 | INFO     | seahorse.game.master:play_game:132 - Player now playing : random_player_divercite_2 - 1299775648336
2024-12-07 17:53:20.971 | INFO     | seahorse.game.master:step:97 - time : 899.8492240905762
2024-12-07 17:53:20.977 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◆  ◆  ◆  ◆
  🅆  🅆  🅆  🅆
◇  ◆  ◆  ◆  ◆  
  🄱  ▢  ▢  🅆
◆  ◇  ◇  ◇  ◇  
  ▢  ▢  ▢  ▢
◆  ◆  ◆  ◇  ◇
  🄱  🄱  ▢  ▢  
◇  ◆  ◆  ◇  ◇

2024-12-07 17:53:21.531 | INFO     | seahorse.game.master:play_game:132 - Player now playing : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:53:21.543 | INFO     | seahorse.game.master:step:97 - time : 464.8119640350342
2024-12-07 17:53:43.155 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◆  ◆  ◆  ◆
  🅆  🅆  🅆  🅆
◇  ◆  ◆  ◆  ◆
  🄱  ▢  ▢  🅆
◆  ◇  ◇  ◇  ◆  
  ▢  ▢  ▢  ▢
◆  ◆  ◆  ◇  ◇
  🄱  🄱  ▢  ▢
◇  ◆  ◆  ◇  ◇

2024-12-07 17:53:43.186 | INFO     | seahorse.game.master:play_game:132 - Player now playing : random_player_divercite_2 - 1299775648336
2024-12-07 17:53:43.200 | INFO     | seahorse.game.master:step:97 - time : 899.8449013233185
2024-12-07 17:53:43.209 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◆  ◆  ◆  ◆
  🅆  🅆  🅆  🅆  
◆  ◆  ◆  ◆  ◆
  🄱  ▢  ▢  🅆
◆  ◇  ◇  ◇  ◆
  ▢  ▢  ▢  ▢  
◆  ◆  ◆  ◇  ◇
  🄱  🄱  ▢  ▢
◇  ◆  ◆  ◇  ◇  

2024-12-07 17:53:43.347 | INFO     | seahorse.game.master:play_game:132 - Player now playing : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:53:43.362 | INFO     | seahorse.game.master:step:97 - time : 443.20108819007874
2024-12-07 17:53:59.269 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◆  ◆  ◆  ◆
  🅆  🅆  🅆  🅆
◆  ◆  ◆  ◆  ◆
  🄱  ▢  🅆  🅆
◆  ◇  ◇  ◇  ◆
  ▢  ▢  ▢  ▢
◆  ◆  ◆  ◇  ◇
  🄱  🄱  ▢  ▢  
◇  ◆  ◆  ◇  ◇

2024-12-07 17:53:59.295 | INFO     | seahorse.game.master:play_game:132 - Player now playing : random_player_divercite_2 - 1299775648336
2024-12-07 17:53:59.310 | INFO     | seahorse.game.master:step:97 - time : 899.8381688594818
2024-12-07 17:53:59.314 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◆  ◆  ◆  ◆
  🅆  🅆  🅆  🅆  
◆  ◆  ◆  ◆  ◆
  🄱  ▢  🅆  🅆
◆  ◇  ◇  ◇  ◆
  ▢  🄱  ▢  ▢
◆  ◆  ◆  ◇  ◇  
  🄱  🄱  ▢  ▢
◇  ◆  ◆  ◇  ◇

2024-12-07 17:53:59.487 | INFO     | seahorse.game.master:play_game:132 - Player now playing : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:53:59.495 | INFO     | seahorse.game.master:step:97 - time : 427.2938723564148
2024-12-07 17:54:15.441 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◆  ◆  ◆  ◆
  🅆  🅆  🅆  🅆
◆  ◆  ◆  ◆  ◆
  🄱  ▢  🅆  🅆
◆  ◇  ◇  ◇  ◆
  ▢  🄱  ▢  🅆
◆  ◆  ◆  ◇  ◇  
  🄱  🄱  ▢  ▢
◇  ◆  ◆  ◇  ◇

2024-12-07 17:54:15.475 | INFO     | seahorse.game.master:play_game:132 - Player now playing : random_player_divercite_2 - 1299775648336
2024-12-07 17:54:15.482 | INFO     | seahorse.game.master:step:97 - time : 899.8355243206024
2024-12-07 17:54:15.492 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◆  ◆  ◆  ◆  
  🅆  🅆  🅆  🅆
◆  ◆  ◆  ◆  ◆
  🄱  ▢  🅆  🅆
◆  ◇  ◇  ◇  ◆
  ▢  🄱  ▢  🅆
◆  ◆  ◆  ◇  ◇
  🄱  🄱  ▢  🄱  
◇  ◆  ◆  ◇  ◇

2024-12-07 17:54:15.767 | INFO     | seahorse.game.master:play_game:132 - Player now playing : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:54:15.838 | INFO     | seahorse.game.master:step:97 - time : 411.34785175323486
2024-12-07 17:54:28.343 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◆  ◆  ◆  ◆
  🅆  🅆  🅆  🅆
◆  ◆  ◆  ◆  ◆
  🄱  ▢  🅆  🅆
◆  ◇  ◇  ◆  ◆  
  ▢  🄱  ▢  🅆
◆  ◆  ◆  ◇  ◇
  🄱  🄱  ▢  🄱
◇  ◆  ◆  ◇  ◇

2024-12-07 17:54:28.375 | INFO     | seahorse.game.master:play_game:132 - Player now playing : random_player_divercite_2 - 1299775648336
2024-12-07 17:54:28.380 | INFO     | seahorse.game.master:step:97 - time : 899.8259150981903
2024-12-07 17:54:28.382 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◆  ◆  ◆  ◆  
  🅆  🅆  🅆  🅆
◆  ◆  ◆  ◆  ◆
  🄱  ▢  🅆  🅆
◆  ◇  ◇  ◆  ◆
  🄱  🄱  ▢  🅆  
◆  ◆  ◆  ◇  ◇
  🄱  🄱  ▢  🄱
◇  ◆  ◆  ◇  ◇

2024-12-07 17:54:28.519 | INFO     | seahorse.game.master:play_game:132 - Player now playing : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:54:28.528 | INFO     | seahorse.game.master:step:97 - time : 398.8441460132599
2024-12-07 17:54:38.547 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◆  ◆  ◆  ◆
  🅆  🅆  🅆  🅆
◆  ◆  ◆  ◆  ◆
  🄱  ▢  🅆  🅆
◆  ◇  ◇  ◆  ◆  
  🄱  🄱  🅆  🅆
◆  ◆  ◆  ◇  ◇
  🄱  🄱  ▢  🄱
◇  ◆  ◆  ◇  ◇

2024-12-07 17:54:38.581 | INFO     | seahorse.game.master:play_game:132 - Player now playing : random_player_divercite_2 - 1299775648336
2024-12-07 17:54:38.591 | INFO     | seahorse.game.master:step:97 - time : 899.8230137825012
2024-12-07 17:54:38.691 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◆  ◆  ◆  ◆
  🅆  🅆  🅆  🅆  
◆  ◆  ◆  ◆  ◆
  🄱  ▢  🅆  🅆
◆  ◇  ◇  ◆  ◆  
  🄱  🄱  🅆  🅆
◆  ◆  ◆  ◇  ◇
  🄱  🄱  🄱  🄱
◇  ◆  ◆  ◇  ◇  

2024-12-07 17:54:38.931 | INFO     | seahorse.game.master:play_game:132 - Player now playing : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:54:38.979 | INFO     | seahorse.game.master:step:97 - time : 388.82673692703247
2024-12-07 17:54:45.679 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◆  ◆  ◆  ◆
  🅆  🅆  🅆  🅆
◆  ◆  ◆  ◆  ◆  
  🄱  ▢  🅆  🅆
◆  ◇  ◇  ◆  ◆
  🄱  🄱  🅆  🅆
◆  ◆  ◆  ◇  ◆  
  🄱  🄱  🄱  🄱
◇  ◆  ◆  ◇  ◇

2024-12-07 17:54:45.727 | INFO     | seahorse.game.master:play_game:132 - Player now playing : random_player_divercite_2 - 1299775648336
2024-12-07 17:54:45.739 | INFO     | seahorse.game.master:step:97 - time : 899.7231478691101
2024-12-07 17:54:45.748 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◇  ◆  ◆  ◆  ◆  
  🅆  🅆  🅆  🅆
◆  ◆  ◆  ◆  ◆  
  🄱  ▢  🅆  🅆
◆  ◇  ◇  ◆  ◆  
  🄱  🄱  🅆  🅆
◆  ◆  ◆  ◆  ◆  
  🄱  🄱  🄱  🄱
◇  ◆  ◆  ◇  ◇

2024-12-07 17:54:45.816 | INFO     | seahorse.game.master:play_game:132 - Player now playing : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:54:45.832 | INFO     | seahorse.game.master:step:97 - time : 382.12664675712585
2024-12-07 17:54:47.339 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◆  ◆  ◆  ◆  ◆
  🅆  🅆  🅆  🅆  
◆  ◆  ◆  ◆  ◆
  🄱  ▢  🅆  🅆
◆  ◇  ◇  ◆  ◆
  🄱  🄱  🅆  🅆
◆  ◆  ◆  ◆  ◆  
  🄱  🄱  🄱  🄱
◇  ◆  ◆  ◇  ◇

2024-12-07 17:54:47.375 | INFO     | seahorse.game.master:play_game:132 - Player now playing : random_player_divercite_2 - 1299775648336
2024-12-07 17:54:47.380 | INFO     | seahorse.game.master:step:97 - time : 899.7145681381226
2024-12-07 17:54:47.386 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◆  ◆  ◆  ◆  ◆
  🅆  🅆  🅆  🅆  
◆  ◆  ◆  ◆  ◆
  🄱  ▢  🅆  🅆
◆  ◆  ◇  ◆  ◆
  🄱  🄱  🅆  🅆
◆  ◆  ◆  ◆  ◆  
  🄱  🄱  🄱  🄱
◇  ◆  ◆  ◇  ◇

2024-12-07 17:54:47.420 | INFO     | seahorse.game.master:play_game:132 - Player now playing : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:54:47.423 | INFO     | seahorse.game.master:step:97 - time : 380.62034797668457
2024-12-07 17:54:47.496 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◆  ◆  ◆  ◆  ◆
  🅆  🅆  🅆  🅆
◆  ◆  ◆  ◆  ◆
  🄱  ▢  🅆  🅆
◆  ◆  ◆  ◆  ◆
  🄱  🄱  🅆  🅆
◆  ◆  ◆  ◆  ◆
  🄱  🄱  🄱  🄱
◇  ◆  ◆  ◇  ◇

2024-12-07 17:54:47.522 | INFO     | seahorse.game.master:play_game:132 - Player now playing : random_player_divercite_2 - 1299775648336
2024-12-07 17:54:47.525 | INFO     | seahorse.game.master:step:97 - time : 899.7104501724243
2024-12-07 17:54:47.528 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◆  ◆  ◆  ◆  ◆
  🅆  🅆  🅆  🅆
◆  ◆  ◆  ◆  ◆  
  🄱  🄱  🅆  🅆
◆  ◆  ◆  ◆  ◆
  🄱  🄱  🅆  🅆
◆  ◆  ◆  ◆  ◆
  🄱  🄱  🄱  🄱
◇  ◆  ◆  ◇  ◇

2024-12-07 17:54:47.548 | INFO     | seahorse.game.master:play_game:132 - Player now playing : Strategy_B_player_heuristic1_1 - 1299761887440
2024-12-07 17:54:47.552 | INFO     | seahorse.game.master:step:97 - time : 380.54864382743835
2024-12-07 17:54:47.560 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◆  ◆  ◆  ◆  ◆
  🅆  🅆  🅆  🅆
◆  ◆  ◆  ◆  ◆
  🄱  🄱  🅆  🅆  
◆  ◆  ◆  ◆  ◆
  🄱  🄱  🅆  🅆
◆  ◆  ◆  ◆  ◆
  🄱  🄱  🄱  🄱
◇  ◆  ◆  ◇  ◆

2024-12-07 17:54:47.581 | INFO     | seahorse.game.master:play_game:132 - Player now playing : random_player_divercite_2 - 1299775648336
2024-12-07 17:54:47.582 | INFO     | seahorse.game.master:step:97 - time : 899.7070515155792
2024-12-07 17:54:47.588 | INFO     | seahorse.game.master:play_game:159 - Current game state:

◆  ◆  ◆  ◆  ◆
  🅆  🅆  🅆  🅆
◆  ◆  ◆  ◆  ◆
  🄱  🄱  🅆  🅆  
◆  ◆  ◆  ◆  ◆
  🄱  🄱  🅆  🅆
◆  ◆  ◆  ◆  ◆
  🄱  🄱  🄱  🄱  
◇  ◆  ◆  ◆  ◆

2024-12-07 17:54:47.764 | INFO     | seahorse.game.master:play_game:169 - Strategy_B_player_heuristic1_1:26
2024-12-07 17:54:47.769 | INFO     | seahorse.game.master:play_game:169 - random_player_divercite_2:18
2024-12-07 17:54:47.771 | INFO     | seahorse.game.master:play_game:172 - Winner - Strategy_B_player_heuristic1_1
2024-12-07 17:54:47.779 | VERD

"""

# Identifiants des joueurs
player_1_name = "Strategy_B_player_heuristic1_1"
player_2_name = "full_diversite_2"

# Fonction pour extraire les temps de début de tour d'un joueur
def extract_times(player_name, log_content):
    pattern = re.compile(
        rf"Player now playing : {player_name}.*?\n.*?step:97 - time : (\d+\.?\d*)",
        re.DOTALL
    )
    return [float(match) for match in pattern.findall(log_content)]

# Extraction des temps des deux joueurs
player_1_times = extract_times(player_1_name, log_content)

# Calcul des durées des tours pour chaque joueur
player_1_durations = [
    player_1_times[i] - player_1_times[i + 1]
    for i in range(len(player_1_times) - 1)
]


# Calcul des sommes
player_1_total_time = sum(player_1_durations)

# Affichage des résultats
print(f"Temps début du joueur 1 ({player_1_name}): {player_1_times}\n")

print(f"Durée par tour du joueur 1 ({player_1_name}): {player_1_durations}")
print(f"Temps total du joueur 1 : {player_1_total_time} secondes\n")


# Tracé du diagramme
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(player_1_durations) + 1), player_1_durations, marker='o', label="Temps par tour")
plt.title("Temps par tour au cours du temps")
plt.xlabel("Tour")
plt.ylabel("Temps (secondes)")
plt.xticks(range(1, len(player_1_durations) + 1))  # Afficher chaque tour
plt.grid(True)
plt.legend()
plt.show()