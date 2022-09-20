#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : [Hajar Sadeghi, hasadeg@iu.edu]
#
# Based on skeleton code provided in CSCI B551, Fall 2022.

import sys

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col, visited):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))
        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        possible_moves = []
        for move in moves:
                # do not add a spot as possible moves if it is already visited
                if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) and move not in visited:
                        possible_moves.append(move)
        return possible_moves

# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

# Function to determine whether the next movie is Up, Right, Left, or Down
def arrow_indicator(curr, nxt):
        x1, y1 = curr[0], curr[1]
        x2, y2 = nxt[0], nxt[1]

        if x2 > x1: return 'D'
        elif x2 < x1: return 'U'
        elif y2 > y1: return 'R'
        elif y2 < y1: return 'L'
        else: return False

# Function to return the complete direction based on the cells in the house map
def get_path(path):
        pnt = 0
        directions = ''
        for v in path:
                if pnt != len(path) - 1:
                        pnt += 1
                        directions += arrow_indicator(v, path[pnt])
        return directions

# Function to calculate the cost (distance) between the pichu and the destination
def manhattan_distance(pnt1, pnt2):
        return (abs(pnt2[0]-pnt1[0]) + abs(pnt2[1]-pnt1[1]))

def search(house_map):
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        # Find destination position
        des_loc = [(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="@"][0]
        # add the path parameter to each point on the map, so that whenever we pop a point, we would know which direction, we have traveled to get to this point 
        fringe=[(pichu_loc,0, [])]
        # a visited array to not revisit the visited states
        visited = []
        
        while fringe:
                # a hashMap to keep track of the node with minimum manhattan distance to pop from fringe
                minDis = {'index': -1,
                        'node': fringe[-1][0],
                        'manhattan': manhattan_distance(fringe[-1][0], des_loc),
                        'steps': fringe[-1][1],
                        'cost': manhattan_distance(fringe[-1][0], des_loc) + fringe[-1][1]}

                # we cannot simply pop the last node in fring, we need to pop the node with minimum manhattan distance to the destination
                for i, node in enumerate(fringe):
                        newDis = manhattan_distance(node[0], des_loc) + node[1]
                        nxtMvs = moves(house_map, node[0][0], node[0][1], visited)
                        if (newDis <= minDis['cost']) and len(nxtMvs) > 0:
                                minDis['index'] = i
                                minDis['node'] = node[0]
                                minDis['manhattan'] = manhattan_distance(node[0], des_loc)
                                minDis['steps'] = node[1]
                                minDis['cost'] = manhattan_distance(node[0], des_loc) + node[1]
                # we pop the node with minimum cost from the fringe
                (curr_move, curr_dist, path)=fringe.pop(minDis['index'])
                # expand the node's path by adding the current move to it, so we would have the updated path in the fringe
                new_path = path + [curr_move]
                # pass the visited as a prameter so that when calculating the possible next moves, we don't get stuck in a loop
                mvs = moves(house_map, *curr_move, visited)
                if mvs:
                        visited.append(curr_move)     
                        for move in mvs:
                                if house_map[move[0]][move[1]]=="@":
                                        visited.append(move)
                                        path.append(des_loc)
                                        final_path = new_path + [des_loc]
                                        return (curr_dist+1, get_path(final_path)) # return a dummy answer
                                else:
                                        fringe.append((move, curr_dist + 1, new_path))
        return -1
# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print(house_map)
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1]) if solution != -1 else print(solution)

