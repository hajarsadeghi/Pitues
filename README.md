# a0-release
# Question 1
# Program's search abstraction
The program starts from the initial state, considers all the possible moves from that state, calculates the cost and pops the point with minimum cost from the fringe. So far, if the current state is equal to the goal state, the program returns the solution (R,L,U,D directions), otherwise it will add the current state along with its path (the directions it has taken to get to this state) to the fringe to be considered later. So, it will repeat the same steps until the next step is actually the goal state, which then returns the result.
# Why does the program often fail to find a solution?
The program was stuck in a loop because in any state, it would consider all the states that were possible from that point, and added them to fringe regardless of if they were visited before or not (got stuck in loop). Therefore, I defined an array called visited, where any state that was expanded would be added to this state, and in this way, whenever the program wants to consider next possible states, it won't revisit the already visited states.
# initial state
Is the arrangement of one pichu (in point (5, 0)), and me (@ (5, 6)) where cost is zero
# goal state
To find the shortest path between pichu and me, which based on map1 is UUURRDDDRRUURRDD, and costs 16 steps
# Set of valid states
Any route from the initial state to the map state where the cost is less than other routes
# successor function
The successor function returns all the points to the top, right, left, bottom that are in the valid index (they are in the bound of our path1/path2 house map), are available (not wall (X) is in there) and the have not been visited before.
# cost function
I used manhattan distance (from the current state to the goal (@) state in every step) since the pichu cannot move diagonal + the steps taken to get to this point 

# Question 2

# Problem with the initial code:
The programs adds a new pichu(p) to each cell where it has the value "."; however, the problem mentions that two pichus cannot be on the same row, column, or diagonal, therefore, before adding a new pichu(calling the add pichu function), we need to recognize the unavailable points.
In our case the unavailable points are the points on a row, column, or diagonal of an already added p where there is no wall (X) between.

# Solution:
I defined a function called: flag_not_allowed, and I call it on the successor function, and before calling the add_pichu function. What it does is that it calls three other function called check_row, check_column, check diagonal where it spots "pichus", and flags the unavailable states. Then, when calling the add_pichu we know that any pichu added to any "." spots is not attacking other pichus.

# Initial State:
First, we read the map1/map2 .txt, and convert them into an array of arrays using the parse_map function. This array contains one pichu (p), and we consider this array our initial state, and add it to our fringe(states to be expanded)

# Goal State:
Arrangement of the K pichus on a 6 by 7 space, where no two pichus are attacking (are on the same row, column or diagonal where no wall is obsecuring the other pichu) each other.

# State Space:
All the arrangement of K pichus from 1 to K inclusive where no two pichus are attacking eachother 

# successor function:
When adding one pichu, if the current arrangemnet of pichu is not our goal, we pop the last pushed state, and review all the possible children of that state using the successor function. For example, if we have two pichus added, we pop the last arrangement of the two added pichus, and expand that state, and consider the arrangement of the third pichu. These possible arrangements of the third pichu (to be expanded later one by one if the goal state isn't found yet) is produced by the successor function.

# Cost:
O(bm), where b is our branching factor where in the first layer it is 21, and m is the maximum depth of the search tree (in our case, how deep did we expanded one 6 by 7 state and children)
