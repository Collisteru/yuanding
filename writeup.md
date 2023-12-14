# Pai Sho Yuanding

Pai Sho Yuanding is a new AI system for the game Skud Pai Sho. Skud Pai Sho is a modern game created by fans of the game of Pai Sho seen in the TV series Avatar: The Last Airbender. It has a large community of enthusiasts. The ruleset can be found [here](https://skudpaisho.com/site/games/skud-pai-sho/pai-sho-rules/).

To our knowledge, there are no good existing AIs for Skud Pai Sho. Part of the goal for this project was to see if we could use techniques discussed in class to create a good AI player for the game.

This project was particularly challenging because it involved implementing the game of Skud Pai Sho from scratch in Python and in a way that would make it a good framework for the AI. To make this task tenable in the month we had, we implmemented a greatly simplified version of Skud Pai Sho that is played on a smaller board and with only one type of piece. Each piece can only move one space orthogonally to decreate the number of options for each piece. These changes significantly reduced the branching factor, which was by far the most challenging aspect of this project. However, even our simplified game is still a very complex environment, adn the AI exhibits interesting and emergent behavior in the environment that we've implemented.


### The libraries used are the following: 
 - math
 - colorama
 - termcolor
 - numpy
 
### The frameworks used was based on the Mancala project in class in terms of having or building up to
 - display function
 - variable board sizing
 - aimagames Minimax 

### Functionality: 
Our testing so far has confirmed the following functionality
 - Board
     - Display
        * We can verify visually that display corresponds to correct boardstate
     - Correct coordinate notation
        * We can verify visually that display corresponds to correct boardstate
     - Gameplay
        * We can play a game that abides by the modified rules
     - Harmony 
     - Win condition checking
        * We create board states in which there should be a win and see there are wins.
     - Harmony chain checking
        * We form harmonies and check internally if the harmonies actually go off.
 - Action
     - Player input
        * We can play a game
     - Placing pieces
     - Removing pieces
     - Moving pieces
         - Legally moving existing pieces
            * Not only can we individually verify legal move placement by manually inputting moves, but also the legal move checker seems to work with the AI.
         - Legally placing pieces
            * Not only can we individually verify legal move placement by manually inputting moves, but also the legal move checker seems to work with the AI.
         - Capturing pieces
            * Pieces seem to get captured in accordance to expected behavior in AI testing and manual player testing.
 - AI
     - Minimax
         - Evaluation function
             * The harmony chains and piece placement are giving manually verifiable utility
             - Harmony chain checking
                * The harmony chains are giving manually verifiable utility
     - Random Gameplay
        * Gameplay of a player vs the random gameplay seems to be playing legal moves and identifies all possible moves.

### The following are functionalities to test but haven't been fully implemented or functionalities that are to be implemented with more progress.
 - Alpha Beta (Requires "Minimax" to work.)


 ## Implementation Details

 Our implementation of Skud Pai Sho was based entirely on the command line, as we didn't want to deal with graphics libraries in the limited time we have. You can play a game with another player entirely with the command line by running the "pvpdemo.py" file.

The game engine itself is mostly contained in PaiSho.py, while certain methods for the pieces exist in piece.py.

Discussing every single aspect of the gameplay implementation would be tedious, since there are over 1,000 lines of code. However, it's worth looking at the highlights. One of the most interesting parts of our implementation of the game rules is the rules that detect harmony circles. We determine whether three or more pieces are all part of the same harmony by adding those harmonies to a graph, and to determine if there is a harmony circle we use DFS to find cycles in the graph. 

A player wins the game when they have a harmony circle that encloses the origin of the board. We detect this by detecting whether a graph of harmonies crosses the four axes of the board, and if it does, we check which axes it crosses. If the harmony cycle crosses all four axes, then the game ends and the player it belongs to is the winner.

You can see this algorithm in particular in the traversal function in PaiSho.py.

### AI

The AI player uses a minmax tree to select the optimal move. Our tree has a maximum depth of 2, as we discovered that the AI takes too long when using any depth larger than that. One interesting way to expand on this project would be to implement alpha-beta pruning to make this process faster, which we believe would allow us to implement a minmax tree at greater depths.




 ### Conclusions

We quickly found out how much branching factor impacted our AI. In our testing, we initially had the pieces able to move 3 spaces, but we realized that a single piece would then have 24 possible moves. This dramatically slowed down iterating through all moves within a certain depth for minimax. To remedy this, we altered the acceptable game rules to restrict the pieces to only be able to move 1 space which drops the branching factor to 4 per piece.

We also found out how potential emergent behavior that's unintuitive to a player would appear. In an example, we were confused regarding a decision that the AI did in that it initially appeared that the AI didn't find the best move, but on further analysis, it turns out that the AI actually saw the opponent planting in the garden which would result in it losing a lot of evaluation. In fact, we talked about the concept of gate control, which in Skud Pai Sho is when a player keeps one of the flowers in a gate to prevent the opponent from being able to use it, and we had decided that we saw it manifest despite not placing direct evaluation value on it.