import numpy as np # Matrix representation

"""
Board
-----
Represents a Go board as a 19x19 matrix, with operations to be performed on it.

Members:
    - board: the matrix representation of the board, where board[i,j]=1 indicates that row i, column j contains a black
             stone. 0 indicates an empty space, and -1 indicates a white stone.

Methods:
    - place_b(x,y): Places a black stone at coordinate (x,y) and checks for capture
    - place_w(x,y): Places a white stone at coordinate (x,y) and checks for capture
    - check_capture(x,y): Checks if any groups adjacent to (x,y) have 0 liberties. If so, removes them.
    - get_neighbors(x,y): Returns the colors and coordinates of all squares adjacent to (x,y)
    - get_group(x,y): Returns all coordinates part of the group at (x,y) and the number of liberties the group has
    - remove_group(x,y): Sets all members of the group at (x,y) to empty 
"""

class Board:
    def __init__(self):
        self.board = np.zeros((19,19))

    def place_b(self,x,y):
        self.board[x,y] = 1
        self.check_capture(x,y)

    def place_w(self,x,y):
        self.board[x,y] = -1
        self.check_capture(x,y)

    def check_capture(self,x,y):
        neigh = self.get_neighbors(x, y)
        for n in neigh:
            ng = self.get_group(*n[1])
            if n[0] != 0: # Don't count adjacent empty squares as a group
                if ng[1] == 0: # No liberties
                    self.remove_group(*n[1])

    def get_neighbors(self,x,y):
        neighbors = []
        for n in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]:
            if n[0] < 0 or n[0] > 18: # Account for cells on the edge / corner
                continue
            elif n[1] < 0 or n[1] > 18:
                continue
            neighbors.append(n)

        return [(self.board[n[0],n[1]], n) for n in neighbors]

    def _get_group(self,x,y,g,libs): # Recursive helper procedure for get_group
        self_c = self.board[x, y] # Color of x,y
        neigh = self.get_neighbors(x, y)

        g.add((x, y))

        for n in neigh:
            if n[0] == 0 and n[1] not in libs: # Add empty neighbor to liberties
                libs.add(n[1])
            if n[0] == self_c and n[1] not in g: # Checks that nonempty neighbor is same color, not already counted
                self._get_group(n[1][0], n[1][1], g, libs)

    def get_group(self,x,y):
        if self.board[x,y] == 0: # Don't count contiguous empty cells as a group
            return set(), -1
        group = set()
        liberties = set()
        self._get_group(x, y, group, liberties)
        return group, len(list(liberties))

    def remove_group(self,x,y):
        group = list(self.get_group(x,y)[0])
        for c in group:
            self.board[c[0],c[1]] = 0