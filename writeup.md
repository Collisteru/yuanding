# Pai Sho Yuanding

Pai Sho Yuanding is a new AI system for the game Skud Pai Sho. Skud Pai Sho is a modern game created by fans of the game of Pai Sho seen in the TV series Avatar: The Last Airbender. It has a large community of enthusiasts. The ruleset can be found [here](https://skudpaisho.com/site/games/skud-pai-sho/pai-sho-rules/).

To our knowledge, there are no good existing AIs for Skud Pai Sho. Part of the goal for this project was to see if we could use techniques discussed in class to create a good AI player for the game.

This project was particularly challenging because it involved implementing the game of Skud Pai Sho from scratch in Python and in a way that would make it a good framework for the AI. To make this task tenable in the month we had, we implmemented a greatly simplified version of Skud Pai Sho that is played on a smaller board and with only one type of piece. Each piece can only move one space orthogonally to decreate the number of options for each piece. These changes significantly reduced the branching factor, which was by far the most challenging aspect of this project. However, even our simplified game is still a very complex environment, and the AI exhibits interesting and emergent behavior in the environment that we've implemented.

### Demo

This project includes many demos allowing you to see the AIs in action. To see them, run the following files in your terminal. ALL OUTPUT IS DISPLAYED IN THE TERMINAL, SO MAKE SURE YOU ARE RUNNING THESE VIA THE TERMINAL.

playervsplayer.py -- Play against your friend on the same terminal

playervsai.py -- Allows you to play against the AI

aivsai.py -- Watch the AIs play against each other.

aivsrand.py -- Watch an AI play against a totally random opponent.


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

### Utility Function

The AI player uses a utility function to rate the utility of each board. The utility function is an important feature of the AI design and was designed to help the AI set itself up in the opening as well as help it spot a winning strategy once setup is complete.

The Host tries to maximize the utility of each state, and the Guest tries to minimize the utility.

- PieceBonus: Each Host piece on the board adds 1 to the board's utility; each Guest piece subtracts 1

- HarmonyBonus: Each Host harmony adds 3 to the baord's utility, opposite for the Guest.

- CrossoverBonus: When a harmony crosses over one the four axes on the board, this is called a "crossover bonus." Harmonies are worth more if they cross over one of the four axes.

- WinningBonus: Any move that would win the game is considered to have infinite utility (this is buggy right now.)

You can see the utility implementation in the calculate_utility function.


### Tweaks

There are three main variables you can tweak while playing around with the AI to observe different behaviors.

**Board Radius:** Larger boards offer more room to set up harmonies and fewer capture opportunities, but also tend to be slower for the AIs to calculate. Adjust this by passing in different integers to the PaiSho.PaiSho() function in the demo files.

**Piece Move Radius:** In the original game, different pieces can move different numbers of squares at a time, ranging from 3 to 5. This results in explosive branch factors, so we changed it to 1 in our implementation. However, this results in slow, capture-heavy games with few opporrtunities for harmonies. We have found that 2 is a good sweet spot that still runs at a decent spped. 

In our implementation, all pieces have the same move radius. You can change this by going into piece.py and changing self.type t0 "3" or "4", or whatever you want the move radius to be. MAKE SURE THAT THIS IS A STRING, EVEN THOUGH THE STRING ALWAYS REPRESENTS A DIGIT.

**AI Max Depth:** The most important parameter. Higher values make the AI see more moves into the future, thus making the AI much better, but will also *significantly* slow down AI processing. Do not mix high AI Max Depth with high Piece Move Radius.



### Observations

 - Limiting the pieces to move one at a time tends to make for capture-heavy games.

 - The AIs tend to get into loops of activity, especially with low move radii and low maxDepths. This is because, with such limited restrictions on movement, the AIs get into the same situations over and over again.

 - On a large enough board and with a piece move of 2, an AI can easily beat a random player.

- Two AIs tend to get into stalemates

 ### Conclusions

We quickly found out how much branching factor impacted our AI. In our testing, we initially had the pieces able to move 3 spaces, but we realized that a single piece would then have 24 possible moves. This dramatically slowed down iterating through all moves within a certain depth for minimax. To remedy this, we altered the acceptable game rules to restrict the pieces to only be able to move 1 space which drops the branching factor to 4 per piece.

We also found out how potential emergent behavior that's unintuitive to a player would appear. In an example, we were confused regarding a decision that the AI did in that it initially appeared that the AI didn't find the best move, but on further analysis, it turns out that the AI actually saw the opponent planting in the garden which would result in it losing a lot of evaluation. In fact, we talked about the concept of gate control, which in Skud Pai Sho is when a player keeps one of the flowers in a gate to prevent the opponent from being able to use it, and we had decided that we saw it manifest despite not placing direct evaluation value on it.

If we had more time on this project, we would be very interested in *implement alpha beta pruning to make the AI minmaxes faster*. This would unlock much more powerful AIs, since the AIs would be able to make similarly complex decisions in a much shorter amount of time. We would also be interested in exploring variants of Skud Pai Sho that are clsoer to the original game.