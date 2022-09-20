#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : [PUT YOUR NAME AND USERNAME HERE]
#
# Based on skeleton code in CSCI B551, Fall 2022.

import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Function to get the locations of pichus
def get_p(house_map):
    return [ (r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == 'p' ]

# Function to flag all the spots in the same row as the pichu if no wall is between
def check_row(house_map, pichus):
    for p in pichus:
        row, col = p[0], p[1]
        this_row = house_map[row]
        # loop to go in reverse in the row of the pichu
        for j in range(col-1, -1, -1):
            if this_row[j] == 'X':
                break
            elif this_row[j] == '.': 
                this_row = this_row[0:j] + ['b'] + this_row[j+1:]
        # loop to go to the right in the row of the pichu
        for i in range(col+1, len(this_row)):
            if this_row[i] == 'X': 
                break
            elif this_row[i] == '.':
                this_row = this_row[0:i] + ['b'] + this_row[i+1:]
        house_map = house_map[0:row] + [this_row] + house_map[row+1:]
    return house_map

# Function to flag all the spots in the same column as the pichu if no wall is between
def check_column(house_map, pichus):
    for p in pichus:
        # go through all the upper cells of the column where pichu is 
        row, col = p[0]+1, p[1]
        while row < len(house_map) and house_map[row][col]:
            if house_map[row][col] == 'X':
                break 
            elif house_map[row][col] == '.':
                house_map = house_map[0:row] + [house_map[row][0:col] + ['b',] + house_map[row][col+1:]] + house_map[row+1:]
            row += 1

         # go through all the lower cells of the column where pichu is 
        row, col = p[0]-1, p[1]
        while row >= 0 and house_map[row][col]:
            if house_map[row][col] == 'X':
                break 
            elif house_map[row][col] == '.':
                house_map = house_map[0:row] + [house_map[row][0:col] + ['b',] + house_map[row][col+1:]] + house_map[row+1:]
            row -= 1
    
    return house_map

# Function to flag all the spots in the same diagonal as the pichu if no wall is between
def check_diagonal(house_map, pichus):
    for p in pichus:
        # Go diagonal to the upper right
        row, col = p[0]-1, p[1]+1
        while row >= 0 and col < len(house_map[0]) and house_map[row][col]:
            if house_map[row][col] == 'X':
                break 
            elif house_map[row][col] == '.':
                house_map = house_map[0:row] + [house_map[row][0:col] + ['b',] + house_map[row][col+1:]] + house_map[row+1:]
            row -= 1
            col += 1

        # Go diagonal to the lower left
        row, col = p[0]+1, p[1]-1
        while row < len(house_map) and col >= 0 and house_map[row][col]:
            if house_map[row][col] == 'X':
                break 
            elif house_map[row][col] == '.':
                house_map = house_map[0:row] + [house_map[row][0:col] + ['b',] + house_map[row][col+1:]] + house_map[row+1:]
            row += 1
            col -= 1

         # Go diagonal to the lower right
        row, col = p[0]+1, p[1]+1
        while row < len(house_map) and col < len(house_map[0]) and house_map[row][col]:
            if house_map[row][col] == 'X':
                break 
            elif house_map[row][col] == '.':
                house_map = house_map[0:row] + [house_map[row][0:col] + ['b',] + house_map[row][col+1:]] + house_map[row+1:]
            row += 1
            col += 1

        # Go diagonal to the upper left
        row, col = p[0]-1, p[1]-1
        while row >= 0 and col >= 0 and house_map[row][col]:
            if house_map[row][col] == 'X':
                break 
            elif house_map[row][col] == '.':
                house_map = house_map[0:row] + [house_map[row][0:col] + ['b',] + house_map[row][col+1:]] + house_map[row+1:]
            row -= 1
            col -= 1
    return house_map

def flag_not_allowed(house_map):
    # Get the pichu locations
    pichu_loc = get_p(house_map)
    # flag not allowed cells in the pichu rows
    updated_hm = check_row(house_map, pichu_loc)
    # flag not allowed cells in the pichu columns
    updated_hm = check_column(updated_hm, pichu_loc)
    # flag not allowed cells in the pichu diagonal
    updated_hm = check_diagonal(updated_hm, pichu_loc) 
    return updated_hm
    
# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

# Function to remove all the b(blocks) from the house map to print at the end
def remove_blocks(house_map):
    for r in range(0, len(house_map)):
        for c in range(0,len(house_map[0])):
            if house_map[r][c] == 'b':
                house_map = house_map[0:r] + [house_map[r][0:c] + ['.',] + house_map[r][c+1:]] + house_map[r+1:]
    return house_map  

# Get list of successors of given house_map state
def successors(fringe, house_map):
    new_fringe = []
    new_house_map = house_map
    for r in range(0, len(house_map)):
        for c in range(0,len(house_map[0])):
            # for each cell before adding a new pichu, first flag all the not allowed cells, and then add a new pichu
            new_house_map = flag_not_allowed(new_house_map)
            if new_house_map[r][c] == '.':
                updated_hm = add_pichu(new_house_map, r, c)
                if updated_hm not in fringe: new_fringe.append(updated_hm)
    return new_fringe

# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k 

# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_house_map,k):
    fringe = [initial_house_map]
    while len(fringe) > 0:
        for new_house_map in successors( fringe, fringe.pop() ):
            if is_goal(new_house_map,k):
                return(remove_blocks(new_house_map),True) 
            # check for duplicates if any before adding to the fringe
            if new_house_map not in fringe: fringe.append(new_house_map)

# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution else "False")


