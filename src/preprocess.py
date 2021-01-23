import pandas as pd # Export boards as CSV
import os # Path management
import re # Clean up sgf data
import time # Benchmarking
from board import * # Go engine
from string import ascii_lowercase # Convenience
from visualize import * # Visualize a Go board from its matrix

letter_ind = {ascii_lowercase[i]:i for i in range(26)} # For converting from letters to coordinates

"""
convert_all_sgf
---------------
Converts all .sgf files (containing the moves played in a Go game) in a folder to .csv files containing a matrix
which represents the final board state. 

In a .csv file, a 1 indicates a black stone at that coordinate, a -1 indicates
a white stone at that coordinate, and a 0 indicates an empty point at the coordinate.

Parameters:
    - `folder`: a string designating the data folder containing the .sgf files to convert to .csv
    - `overwrite(=False)`: whether or not to overwrite existing .csv files that have the same name as an .sgf file
    
Preconditions:
    - folder contains only .sgf files
"""
def convert_all_sgf(folder, overwrite=False):
    dir = os.getcwd() + "..\\data\\" + folder # Get the whole file path to the folder
    if not os.path.exists(dir + "_csv"):
        os.mkdir(dir + "_csv") # Make directory for new .csv files

    i = 0 # Keep track of conversion progress
    over = 0 # Files overwritten
    t1 = time.time() # Start time

    for fname in os.listdir(dir): # Loop through all files
        #print("PROCESSING FILE: " + fname)
        if i % 1000 == 0:
            print("%d files converted." % i) # Update on progress

        if os.path.exists(dir+"_csv\\"+fname[:-4]+".csv"):
            i += 1
            if not overwrite: # Skip files that already exist
                continue
            else:
                over += 1

        f = open(dir+"\\"+fname) # Open .sgf file
        f_data = re.sub('^\(;[^;]*;([BW])\[', "\\1[", f.read())[:-1] # Extract move data
        moves = [s[2:4] for s in f_data.split(";")] # Get individual moves
        board = get_final_board(moves) # Play out game (accounting for captures) to get final board state

        if np.array_equal(board, np.zeros((19,19))):
            continue # Throw away empty games

        board_frame = pd.DataFrame(board)
        board_frame.to_csv(dir + "_csv\\" + fname[:-4] + ".csv") # Write final board to .csv under the same name as the .sgf

        i += 1

    print("Finished converting $d files in %f seconds. %d files overwritten." % (i, time.time()-t1, over))

"""
mean_board_csv
--------------
Calculates and writes the mean of a folder of .csv files. Used in calculating covariance between coordinates.

Parameters:
    - `folder`: a string designating the data folder containing the .sgf files to convert to .csv
    
Preconditions:
    - folder contains only 19x19 .csv files
"""
def mean_board_csv(folder):
    avg = np.zeros((19, 19)) # Accumulator for the mean board
    dir = os.getcwd() + "..\\data\\" + folder

    i = 0
    t1 = time.time()

    for fname in os.listdir(dir):
        #print("PROCESSING FILE: " + fname)
        if i % 1000 == 0:
            print(i)
        board = pd.read_csv(dir + "\\" + fname).values[:,1:]
        avg += board
        i += 1

    avg /= i # Divide by number of boards to get mean
    avg_frame = pd.DataFrame(avg)
    avg_frame.to_csv(dir + "\\avg.csv")
    print("Mean board of %s written to %s in %f seconds." % (folder, dir+"\\avg.csv", time.time()-t1))

"""
get_final_board
---------------
Executes the moves in a given game of Go to determine the final board position. 

Parameters:
    - `moves`: an array of two-character lowercase strings with characters from a-s. Strings specify board coordinates,
               with the origin 'aa' indicating the top-left of the board. The first character indicates the row, and the
               second the column.

Preconditions:
    - moves contains only strings of the above format
"""
def get_final_board(moves):
    game_board = Board()

    black = True # Black plays first
    for move in moves: # Play each move
        try:
            x,y = letter_ind[move[0]],letter_ind[move[1]] # Coordinates of move
            if black:
                game_board.place_b(x, y)
            else:
                game_board.place_w(x, y)
            black = not black # Switch to other player
        except: # In event of error, return empty board
            return np.zeros((19,19))
    return game_board.board

"""
mean_normalize
--------------
Mean normalizes all games within each folder of a set of folders. A new folder `XXXX_norm` is created, containing the
mean normalized games for a folder XXXX.

Parameters:
    - `folders`: an array of folder names within the 'data' folder, indicates the collections of games to mean normalize

Preconditions:
    - Every folder in folders contains an `avg.csv`, which is the mean of all .csv files in the folder.
"""
def mean_normalize(folders):
    for folder in folders:
        print(folder+"\n")

        dir = os.getcwd() + "..\\data\\" + folder

        if not os.path.exists(dir + "_norm"):
            os.mkdir(dir + "_norm")

        avg = pd.read_csv(dir+"\\avg.csv").values[:,1:]

        i = 1
        t1 = time.time()

        for fname in os.listdir(dir):
            if i % 1000 == 0:
                print(i)
            if os.path.exists(dir+"_norm\\"+fname): # Skip pre-existing files
                continue
            board = pd.read_csv(dir+"\\"+fname).values[:,1:]
            mean_norm_b = pd.DataFrame(board - avg)
            mean_norm_b.to_csv(dir+"_norm\\"+fname)
            i += 1

        print("Mean normalized %s in %f seconds." % (folder, time.time()-t1))
    print("Mean normalization of %d folders complete." % (len(folders)))
