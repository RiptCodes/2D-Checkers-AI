 # Imports
from loginSystem import *
from copy import deepcopy
import csv
from datetime import datetime
import hashlib  #not needed for final program
from shutil import get_terminal_size  #optional
from termcolor import colored  #optional
import time
import math



version = "4.1.3"

#width of the terminal
width = get_terminal_size().columns

# Ansi colors used to change the console colours
ansi_black = "\u001b[30m"
ansi_red = "\u001b[31m"
ansi_green = "\u001b[32m"
ansi_yellow = "\u001b[33m"
ansi_blue = "\u001b[34m"
ansi_magenta = "\u001b[35m"
ansi_cyan = "\u001b[36m"
ansi_white = "\u001b[37m"
ansi_reset = "\u001b[0m"  #this is the default



# Node is the default template used throughout the code
class Node:
  #  The __init__ function is then called to initialize the node object.
  def __init__(self, board, move=None, parent=None, value=None):
    self.board = board
    self.value = value
    self.move =  move
    self.parent = parent

#  The get_children function takes two parameters: minimizing_player and mandatory_jumping. It returns all of the possible children nodes for this node given those parameters.

  def get_children(self, minimizing_player, mandatory_jumping):
    # Minimizing_player parameter is true if it's the computer move; otherwise it's false.
    # Mandatory jumping means that every player must jump over an opponent in order to make a move on their turn (i.e., there are no jumps allowed).
    current_state = deepcopy(self.board)
    available_moves = []
    children_states = []
    big_letter = ""  #unasigned variable for when the state of the draught turns into a queen
    queen_row = 0  #where the queen can be obtained but is a variable that can be changed
    if minimizing_player is True:  #if the player is the computer
      available_moves = Checkers.find_computer_available_moves(current_state, mandatory_jumping)
      big_letter = "C"
      queen_row = 7
    else:  #if the player is the human player
      available_moves = Checkers.find_player_available_moves(
        current_state, mandatory_jumping)
      big_letter = "B"
      queen_row = 0
    for i in range(
        len(available_moves)
    ):  #iterate through the available moves and create a version of the board that has the move using deepcopy
      old_i = available_moves[i][0]  #get the row of the move
      old_j = available_moves[i][1]  #get the column of the move
      new_i = available_moves[i][2]  #get the row of the new board
      new_j = available_moves[i][3]  #get the column of the new board
      state = deepcopy(current_state)  #create a copy of the current board
      Checkers.make_a_move(state, old_i, old_j, new_i, new_j, big_letter,
                           queen_row)  #make the move
      children_states.append(Node(
        state, [old_i, old_j, new_i, new_j
                ]))  #add the new board to the list of children states
    return children_states  #return the list of children states

  def set_value(self, value):
    self.value = value

  def get_value(self):
    return self.value

  def get_board(self):
    return self.board

  def get_parent(self):
    return self.parent

  def set_parent(self, parent):
    self.parent = parent


class Checkers:  #creating the Checkers game

  def __init__(self):  #constructor method
    self.matrix = [
      [], [], [], [], [], [], [], []
    ]  # Initialize an empty 8x8 matrix to represent the checkers board

    self.player_turn = True  # Initialize a variable to keep track of whose turn it is (True = player, False = computer)
    self.computer_pieces = 12  # Initialize a variable to keep track of the number of remaining computer pieces
    self.player_pieces = 12  # Initialize a variable to keep track of the number of remaining player pieces
    self.available_moves = [
    ]  # Initialize an empty list to keep track of available moves for the current turn
    self.mandatory_jumping = False  # Initialize a variable to keep track if a mandatory jump is available for the current turn

    for row in self.matrix:
      for i in range(8):
        row.append("---")  # Fill the matrix with empty spaces
    self.position_computer(
    )  # Call the function to position the computer pieces on the board
    self.position_player(
    )  # Call the function to position the player pieces on the board

  def position_computer(self):
    for i in range(3):
      for j in range(8):
        if (i + j) % 2 == 1:
          self.matrix[i][j] = "c" + str(i) + str(j)
          # self.matrix[i][j] = "c"+ ansi_red + str(i) + str(j) + ansi_reset # Position the computer pieces in the top three rows of the board

  def position_player(self):
    for i in range(5, 8, 1):
      for j in range(8):
        if (i + j) % 2 == 1:

          self.matrix[i][j] = "b" + str(i) + str(
            j
          )  # Position the player pieces in the bottom three rows of the board

  def print_matrix(self):
    i = 0
    print()
    for row in self.matrix:
      print(i, end="  |")  # Print the row number
      i += 1
      for elem in row:
        print(elem, end=" ")  # Print the elements in the row
      print()
    print()
    for j in range(8):
      if j == 0:
        j = "     0"
      print(j, end="   ")  # Print the column number
    print("\n")

  def get_player_input(self):
    available_moves = Checkers.find_player_available_moves(
      self.matrix, self.mandatory_jumping)
    if len(available_moves) == 0:
      if self.computer_pieces > self.player_pieces:
        print(
          ansi_red +
          "You have no moves left, and you have fewer pieces than the computer.YOU LOSE!"
          + ansi_reset)
        exit()
      else:
        print(ansi_yellow + "You have no available moves.\nGAME ENDED!" +
              ansi_reset)
        exit()
    self.player_pieces = 0
    self.computer_pieces = 0
    while True:

      coord1 = input("Which piece[i,j]: ")
      if coord1 == "":
        print(ansi_cyan + "Game ended!" + ansi_reset)
        exit()
      elif coord1 == "s":
        print(ansi_cyan + "You surrendered.\nCoward." + ansi_reset)
        exit()
      coord2 = input("Where to[i,j]:")
      if coord2 == "":
        print(ansi_cyan + "Game ended!" + ansi_reset)
        exit()
      elif coord2 == "s":
        print(ansi_cyan + "You surrendered.\nCoward." + ansi_reset)
        exit()
      old = coord1.split(",")
      new = coord2.split(",")

      if len(old) != 2 or len(new) != 2:
        print(ansi_red + "Illegal input" + ansi_reset)
      else:
        old_i = old[0]
        old_j = old[1]
        new_i = new[0]
        new_j = new[1]
        if not old_i.isdigit() or not old_j.isdigit() or not new_i.isdigit(
        ) or not new_j.isdigit():
          print(ansi_red + "Illegal input" + ansi_reset)
        else:
          move = [int(old_i), int(old_j), int(new_i), int(new_j)]
          if move not in available_moves:
            print(ansi_red + "Illegal move!" + ansi_reset)
          else:
            Checkers.make_a_move(self.matrix, int(old_i), int(old_j),
                                 int(new_i), int(new_j), "B", 0)
            for m in range(8):
              for n in range(8):
                if self.matrix[m][n][0] == "c" or self.matrix[m][n][0] == "C":
                  self.computer_pieces += 1
                elif self.matrix[m][n][0] == "b" or self.matrix[m][n][0] == "B":
                  self.player_pieces += 1
            break

  def write_to_file(self, enter_name_save):
    with open('boards.csv', 'a+', newline='') as f:
      writer = csv.writer(f)
      writer.writerow(enter_name_save + self.matrix)

    # Open the CSV file for reading
    with open('boards.csv', 'r') as csvfile:
      reader = csv.reader(csvfile)
      # Iterate through the rows in the CSV file
      for row in reader:
        # Print the row followed by a gap
        print(row[0])
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

  def hash_password(enter_pass):
    # Create a new sha256 hash object
    sha256 = hashlib.sha256()

    # The hash object is updated with the bytes of the password
    sha256.update(enter_pass.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    password_hash = sha256.hexdigest()

    return password_hash

  def validate_login(enter_name_save, enter_name):
    # Getting current time
    now = datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    # Saving input to file
    username = enter_name
    # Reading input from file
    with open('inputs.txt', 'r+') as f:
      lines = f.readlines()
      for line in lines:
        if username in line:
          print(ansi_green + "Logged in as ".center(width) + ansi_reset +
                ansi_blue + username.center(width) + ansi_reset)
          break
        elif username in line:
          print(ansi_red + "Found username but wrong password" + ansi_reset)
      else:
        print(ansi_green + "~~".center(width) + ansi_reset + ansi_red +
              enter_name.center(width) + ansi_reset + ansi_green +
              "~~".center(width) + ansi_reset + ansi_red +
              " not found in file\n".center(width) + ansi_reset)
        print(ansi_green + "Welcome to the game of Checkers, ".center(width) +
              ansi_reset + ansi_red + enter_name.center(width) + ansi_reset)
        print(
          ansi_green +
          "You will get asked if you want mandatory jumping on or not. If you say yes, it means that you have to jump over the computer whenever you have to take a piece. If this is off, the game is not restricted and you can play normally."
          .center(width) + ansi_reset)

    with open('inputs.txt', 'a+') as f:
      f.write("\nUsername: " + username + " -- " + time + "\n")

  @staticmethod
  def find_computer_available_moves(board, mandatory_jumping):
    available_moves = [
    ]  # Initialize an empty list to store the available moves
    available_jumps = [
    ]  # Initialize an empty list to store the available jumps
    for m in range(8):  # Iterate over the rows of the board
      for n in range(8):  # Iterate over the columns of the board
        if board[m][n][
            0] == "c":  # If the piece at the current position is a "c"
          if Checkers.check_moves(
              board, m, n, m + 1,
              n + 1):  # Check if the piece can move to (m + 1, n + 1)
            available_moves.append([
              m, n, m + 1, n + 1
            ])  # If the move is valid, add it to the available_moves list
          if Checkers.check_moves(
              board, m, n, m + 1,
              n - 1):  # Check if the piece can move to (m + 1, n - 1)
            available_moves.append([
              m, n, m + 1, n - 1
            ])  # If the move is valid, add it to the available_moves list
          if Checkers.check_jumps(
              board, m, n, m + 1, n - 1, m + 2,
              n - 2):  # Check if the piece can jump to (m + 2, n - 2)
            available_jumps.append([
              m, n, m + 2, n - 2
            ])  # If the jump is valid, add it to the available_jumps list
          if Checkers.check_jumps(
              board, m, n, m + 1, n + 1, m + 2,
              n + 2):  # Check if the piece can jump to (m + 2, n + 2)
            available_jumps.append([
              m, n, m + 2, n + 2
            ])  # If the jump is valid, add it to the available_jumps list
        elif board[m][n][
            0] == "C":  # If the piece at the current position is a "C"
          if Checkers.check_moves(
              board, m, n, m + 1,
              n + 1):  # Check if the piece can move to (m + 1, n + 1)
            available_moves.append([
              m, n, m + 1, n + 1
            ])  # If the move is valid, add it to the available_moves list
          if Checkers.check_moves(
              board, m, n, m + 1,
              n - 1):  # Check if the piece can move to (m + 1, n - 1)
            available_moves.append([
              m, n, m + 1, n - 1
            ])  # If the move is valid, add it to the available_moves list
          if Checkers.check_moves(
              board, m, n, m - 1,
              n - 1):  # Check if the piece can move to (m - 1, n - 1)
            available_moves.append([
              m, n, m - 1, n - 1
            ])  # If the move is valid, add it to the available_moves list
          if Checkers.check_moves(
              board, m, n, m - 1,
              n + 1):  # Check if the piece can move to (m - 1, n + 1)
            available_moves.append([
              m, n, m - 1, n + 1
            ])  # If the move is valid, add it to the available_moves list
          if Checkers.check_jumps(
              board, m, n, m + 1, n - 1, m + 2,
              n - 2):  # Check if the piece can jump to (m + 2, n - 2)
            available_jumps.append([
              m, n, m + 2, n - 2
            ])  # If the jump is valid, add it to the available_jumps list
          if Checkers.check_jumps(
              board, m, n, m - 1, n - 1, m - 2,
              n - 2):  # Check if the piece can jump to (m - 2, n - 2)
            available_jumps.append([
              m, n, m - 2, n - 2
            ])  # If the jump is valid, add it to the available_jumps list
          if Checkers.check_jumps(
              board, m, n, m - 1, n + 1, m - 2,
              n + 2):  # Check if the piece can jump to (m - 2, n + 2)
            available_jumps.append([
              m, n, m - 2, n + 2
            ])  # If the jump is valid, add it to the available_jumps list
          if Checkers.check_jumps(
              board, m, n, m + 1, n + 1, m + 2,
              n + 2):  # Check if the piece can jump to (m + 2, n + 2)
            available_jumps.append([
              m, n, m + 2, n + 2
            ])
    # print(available_moves)
    # print(available_jumps)
                # If the jump is valid, add it to the available_jumps list
    if mandatory_jumping is False:  # If the player is not required to make a jump move
      available_jumps.extend(
        available_moves
      )  # Add the available_moves list to the available_jumps list
      return available_jumps  # Return the combined list of available jump and non-jump moves
    elif mandatory_jumping is True:  # If the player is required to make a jump move
      if len(available_jumps) == 0:  # If there are no available jump moves
        return available_moves  # Return the available non-jump moves instead
      else:  # If there are available jump moves
        return available_jumps  # Return the available jump moves

  @staticmethod
  def check_jumps(board, old_i, old_j, via_i, via_j, new_i, new_j):
    if new_i > 7 or new_i < 0:  # Check if the new row position is out of bounds
      return False
    if new_j > 7 or new_j < 0:  # Check if the new column position is out of bounds
      return False
    if board[via_i][
        via_j] == "---":  # Check if the space the piece will jump over is empty
      return False
    if board[via_i][via_j][0] == "C" or board[via_i][via_j][
        0] == "c":  # Check if the space the piece will jump over is occupied by a friendly piece
      return False
    if board[new_i][new_j] != "---":  # Check if the destination space is empty
      return False
    if board[old_i][old_j] == "---":  # Check if the starting space is empty
      return False
    if board[old_i][old_j][0] == "b" or board[old_i][old_j][
        0] == "B":  # Check if the piece being moved is a black piece
      return False
    return True  # Return True if the move is valid

  @staticmethod
  def check_moves(board, old_i, old_j, new_i, new_j):
    if new_i > 7 or new_i < 0:  # Check if the new row position is out of bounds
      return False
    if new_j > 7 or new_j < 0:  # Check if the new column position is out of bounds
      return False
    if board[old_i][old_j] == "---":  # Check if the starting space is empty
      return False
    if board[new_i][new_j] != "---":  # Check if the destination space is empty
      return False
    if board[old_i][old_j][0] == "b" or board[old_i][old_j][
        0] == "B":  # Check if the piece being moved is a black piece
      return False
    if board[new_i][new_j] == "---":  # Check if the destination space is empty
      return True

  @staticmethod
  def calculate_heuristics(
    board
  ):  #hueristics is the points the computer is calculating as the game plays
    result = 0  #total points
    mine = 0  #computer
    opp = 0  #controlling player
    for i in range(8):  #calculates points by checking through the board
      for j in range(8):  #nested for loop to allow for the board to be checked
        if board[i][j][0] == "c" or board[i][j][
            0] == "C":  #checks if the piece is a computer
          mine += 1  #increases the points for the computer

          if board[i][j][0] == "c":
            result += 5
          if board[i][j][0] == "C":  #if a queen is obtained then add 10 points
            result += 10
          if i == 0 or j == 0 or i == 7 or j == 7:  #if the piece is on the top or bottom of the board or the piece is on the left or right of the board then add 7 points
            result += 7
          if i + 1 > 7 or j - 1 < 0 or i - 1 < 0 or j + 1 > 7:
            continue  #if the piece is off the board then do not add points
          if (board[i + 1][j - 1][0] == "b" or board[i + 1][j - 1][0]
              == "B") and board[i - 1][j + 1] == "---":
            result -= 3  #If the condition being checked is true, then the code will subtract 3 from result. Otherwise, the code will do nothing and the value of result will not be modified.
          if (board[i + 1][j + 1][0] == "b"
              or board[i + 1][j + 1] == "B") and board[i - 1][j - 1] == "---":
            result -= 3
          if board[i - 1][j - 1][0] == "B" and board[i + 1][j + 1] == "---":
            result -= 3

          if board[i - 1][j + 1][0] == "B" and board[i + 1][j - 1] == "---":
            result -= 3
          if i + 2 > 7 or i - 2 < 0:
            continue
          if (board[i + 1][j - 1][0] == "B" or board[i + 1][j - 1][0]
              == "b") and board[i + 2][j - 2] == "---":
            result += 6
          if i + 2 > 7 or j + 2 > 7:
            continue
          if (board[i + 1][j + 1][0] == "B" or board[i + 1][j + 1][0]
              == "b") and board[i + 2][j + 2] == "---":
            result += 6

        elif board[i][j][0] == "b" or board[i][j][0] == "B":
          opp += 1  #adds 1 to player

    return result + (mine - opp) * 1000  #final value of the game

  #If the current space contains a player piece, the function checks for available moves and jump moves in all four diagonal directions. It uses the check_player_moves and check_player_jumps functions to verify that the moves are legal according to the rules of checkers. If a move or jump is found to be legal, it is added to the available_moves or available_jumps list, respectively. Finally, the function checks the value of the mandatory_jumping flag. If it is False, the function returns the list of all available moves and jumps. If it is True, the function checks if there are any jump moves available. If there are, it returns only the jump moves. If there are no jump moves available, it returns the list of all available moves. This ensures that the player makes a jump move if one is available, as required by the game rules.

  @staticmethod
  def find_player_available_moves(board, mandatory_jumping):
    available_moves = []
    available_jumps = []
    for m in range(8):
      for n in range(8):
        if board[m][n][0] == "b":
          if Checkers.check_player_moves(board, m, n, m - 1, n - 1):
            available_moves.append([m, n, m - 1, n - 1])
          if Checkers.check_player_moves(board, m, n, m - 1, n + 1):
            available_moves.append([m, n, m - 1, n + 1])
          if Checkers.check_player_jumps(board, m, n, m - 1, n - 1, m - 2,
                                         n - 2):
            available_jumps.append([m, n, m - 2, n - 2])
          if Checkers.check_player_jumps(board, m, n, m - 1, n + 1, m - 2,
                                         n + 2):
            available_jumps.append([m, n, m - 2, n + 2])
        elif board[m][n][0] == "B":
          if Checkers.check_player_moves(board, m, n, m - 1, n - 1):
            available_moves.append([m, n, m - 1, n - 1])
          if Checkers.check_player_moves(board, m, n, m - 1, n + 1):
            available_moves.append([m, n, m - 1, n + 1])
          if Checkers.check_player_jumps(board, m, n, m - 1, n - 1, m - 2,
                                         n - 2):
            available_jumps.append([m, n, m - 2, n - 2])
          if Checkers.check_player_jumps(board, m, n, m - 1, n + 1, m - 2,
                                         n + 2):
            available_jumps.append([m, n, m - 2, n + 2])
          if Checkers.check_player_moves(board, m, n, m + 1, n - 1):
            available_moves.append([m, n, m + 1, n - 1])
          if Checkers.check_player_jumps(board, m, n, m + 1, n - 1, m + 2,
                                         n - 2):
            available_jumps.append([m, n, m + 2, n - 2])
          if Checkers.check_player_moves(board, m, n, m + 1, n + 1):
            available_moves.append([m, n, m + 1, n + 1])
          if Checkers.check_player_jumps(board, m, n, m + 1, n + 1, m + 2,
                                         n + 2):
            available_jumps.append([m, n, m + 2, n + 2])
    # print(available_jumps)
    if mandatory_jumping is False:
      available_jumps.extend(available_moves)
      return available_jumps
    elif mandatory_jumping is True:
      if len(available_jumps) == 0:
        return available_moves
      else:
        return available_jumps

  @staticmethod
  def check_player_moves(board, old_i, old_j, new_i,
                         new_j):  #all available player moves
    if new_i > 7 or new_i < 0:  #checks if the new_i is out of bounds
      return False  #returns false if the new_i is out of bounds
    if new_j > 7 or new_j < 0:  #checks if the new_j is out of bounds
      return False
    if board[old_i][old_j] == "---":  #checks if the old_i and old_j is empty
      return False
    if board[new_i][new_j] != "---":  #checks if the new_i and new_j is occupied
      return False
    if board[old_i][old_j][0] == "c" or board[old_i][old_j][
        0] == "C":  #checks if the old_i and old_j is a computer player
      return False
    if board[new_i][new_j] == "---":  #checks if moved position is empty
      return True

  @staticmethod
  def check_player_jumps(board, old_i, old_j, via_i, via_j, new_i,
                         new_j):  #all available player jumps
    if new_i > 7 or new_i < 0:  #checks if the new_i is out of bounds
      return False
    if new_j > 7 or new_j < 0:  #checks if the new_j is out of bounds
      return False
    if board[via_i][
        via_j] == "---":  #checks if the route to new i,j is empty to allow it to jump
      return False
    if board[via_i][via_j][0] == "B" or board[via_i][via_j][
        0] == "b":  #checks if the route to new i,j is a player
      return False
    if board[new_i][new_j] != "---":  #checks if the new_i and new_j is occupied
      return False
    if board[old_i][old_j] == "---":  #checks if the old_i and old_j is empty
      return False
    if board[old_i][old_j][0] == "c" or board[old_i][old_j][
        0] == "C":  #checks if the old_i and old_j is a computer player
      return False
    return True  #returns true if the player can jump to the new position

  def evaluate_states(self):  #evaluates the states of the game
    t1 = time.time()  #time the function starts
    current_state = Node(deepcopy(
      self.matrix))  #creates a copy of the current state of the board

    first_computer_moves = current_state.get_children(
      True, self.mandatory_jumping
    )  #uses the get_children fuction to get all the information of the computer
    if len(first_computer_moves) == 0:  #checks if there are no computer moves
      if self.player_pieces > self.computer_pieces:  #checks if the player has more pieces than the computer
        print(
          ansi_yellow +
          "Computer has no available moves left, and you have more pieces left.\nYOU WIN!"
          + ansi_reset)
        exit()  #exits the game
      else:
        print(ansi_yellow +
              "Computer has no available moves left.\nGAME ENDED!" +
              ansi_reset)
        exit()  #exits the game
    dict = {
    }  #creates a dictionary to store the information of the computer moves
    for i in range(
        len(first_computer_moves)):  #iterates through the computer moves
      child = first_computer_moves[i]  #creates a copy of the computer move
      value = Checkers.minimax(child.get_board(), 5, -math.inf, math.inf,
                               False, self.mandatory_jumping)
      dict[value] = child
      
    if len(dict.keys()) == 0:
      print(ansi_green + "Computer has cornered itself.\nYOU WIN!" +
            ansi_reset)
      exit()
    new_board = dict[max(dict)].get_board()
    move = dict[max(dict)].move
    self.matrix = new_board
    print(move)
    print(value)
    t2 = time.time()
    diff = t2 - t1
    print("Computer has moved (" + str(move[0]) + "," + str(move[1]) +
          ") to (" + str(move[2]) + "," + str(move[3]) + ").")
    print("It took him " + str(diff) + " seconds.")

#This is the main computer function that allows the computer to move with AI

  @staticmethod
  def minimax(
    board, depth, alpha, beta, maximizing_player, mandatory_jumping
  ):  #this function has 6 parameters, board describes the available deep copied board. Depth is the depth of the minimax function which allows the computer to go through more possible moves to create a better outcome (difficulty of the computer changes when depth gets higher), alpha is the best value that the maximaizer can currently guarantee at the level or above, beta is the best value that the minimizer can currently guarantee at the level or above, maximizing_player is the superior player, and mandatory_jumping is the boolean that determines if the computer is allowed to jump
    if depth == 1:  #increases bot difficulty as AI checks few moves ahead depending on this number
      return Checkers.calculate_heuristics(
        board
      )  #calculate final score of the board and determine minimax depth using score to make game harder
    current_state = Node(
      deepcopy(board))  #creates a copy of the current state of the board
    if maximizing_player is True:  #checks if the player is the superior player
      max_eval = -math.inf  #initializes the max_eval to -infinity
      #The value of the child's board is returned by the recursive call to minimax, and it is stored in the ev variable. The maximum value of all the children's evaluations is then stored in the max_eval variable using the max function. This is because the maximax function is being called on the "max" player's turn, so it needs to find the maximum value of all the children's evaluations.
      for child in current_state.get_children(True, mandatory_jumping):
        ev = Checkers.minimax(child.get_board(), depth - 1, alpha, beta, False,
                              mandatory_jumping)
        max_eval = max(max_eval, ev)
        alpha = max(alpha, ev)  #max returns its biggest item
        if beta <= alpha:  #If the beta value becomes less than or equal to the alpha value, the function breaks out of the loop because it is guaranteed that the current player will not choose this branch of the tree.
          break
      current_state.set_value(
        max_eval
      )  #sets the value of the current state to the max value of all the children's evaluations
      return max_eval
    else:
      min_eval = math.inf  #initializes the min_eval to infinity
      for child in current_state.get_children(
          False, mandatory_jumping
      ):  #iterates through the children of the current state
        ev = Checkers.minimax(child.get_board(), depth - 1, alpha, beta, True,
                              mandatory_jumping)
        min_eval = min(min_eval, ev)
        beta = min(beta, ev)
        if beta <= alpha:  # If the beta value becomes less than or equal to the alpha value, the function breaks out of the loop for the same reason as above.
          break
      current_state.set_value(min_eval)
      return min_eval

  @staticmethod
  def make_a_move(
    board, old_i, old_j, new_i, new_j, big_letter, queen_row
  ):  #this function is used to make a move. Deep copy algorithm checks this code and uses it in execution during the main code
    letter = board[old_i][old_j][
      0]  #this is the letter that the computer is trying to move
    i_difference = old_i - new_i  #this is the difference between the old and new i
    j_difference = old_j - new_j  #this is the difference between the old and new j
    if i_difference == -2 and j_difference == 2:  #checks if user input is valid for jump with a vector of [-2,2]
      board[old_i + 1][old_j -
                       1] = "---"  #this is valid checking the empty spaces

    elif i_difference == 2 and j_difference == 2:  #checks if user input is valid for jump with a vector of [2,2]
      board[old_i - 1][old_j - 1] = "---"

    elif i_difference == 2 and j_difference == -2:  #checks if user input is valid for jump with a vector of [2,-2]
      board[old_i - 1][old_j + 1] = "---"

    elif i_difference == -2 and j_difference == -2:  #checks if user input is valid for jump with a vector of [-2,-2]
      board[old_i + 1][old_j + 1] = "---"

    if new_i == queen_row:  #checks if the new i is the same as the queen row
      letter = big_letter  #turns the draught into a queen
    board[old_i][
      old_j] = "---"  #turns the old positions of the board into a "---" because the player has moved to an empty spot
    board[new_i][new_j] = letter + str(new_i) + str(
      new_j
    )  #turns the new positions of the board into the letter of the player

  def play(self):  #this function is used to play the game
    print(
      ansi_black +
      """\n_ _ _ ____ _    ____ ____ _  _ ____    ___ ____    ____ _  _ ____ ____ _  _ ____ ____ ____ 
| | | |___ |    |    |  | |\/| |___     |  |  |    |    |__| |___ |    |_/  |___ |__/ [__  
|_|_| |___ |___ |___ |__| |  | |___     |  |__|    |___ |  | |___ |___ | \_ |___ |  \ ___] 
                                                                                           """
      + ansi_reset
    )  #this is the welcome message using ansi values which are used to make the console view look nice

    enter_name = input("Enter your username: ")
    while len(enter_name) < 1:
      print("Issue seeing the username, Try again.")
      enter_name = input("Enter your username: ")

    enter_name_save = ["Username: " + enter_name]
    Checkers.validate_login(enter_name_save, enter_name)

    text = "Some basic rules:\n"
    text_len = len(text)
    highlighted_underlined_text = colored(text,
                                          on_color='on_yellow',
                                          attrs=['underline'])
    left_margin = (width - text_len) // 2
    print(" " * left_margin, highlighted_underlined_text)
    print("1.Enter the coordinates in the form i,j.".center(width))
    print(
      "2.You can quit the game at any time by pressing enter.".center(width))
    print("3.You can surrender at any time by pressing 's'.".center(width))
    print(
      "Now that you've familiarized yourself with the rules, enjoy!".center(
        width))
    while True:  #this is the main loop that is used to play the game
      answer = input("\nNow, we need to know, is jumping mandatory?[Y/n]: ")
      if answer == "Y" or answer == "y":
        self.mandatory_jumping = True
        break
      elif answer == "N" or answer == "n":
        self.mandatory_jumping = False
        break
      elif answer == "":
        print(ansi_cyan + "Game ended!" + ansi_reset)

        enter_name_save.append("Game ended!")
        Checkers.write_to_file(self, enter_name_save)
        exit()
      elif answer == "s":
        print(ansi_cyan +
              "You've surrendered before the game even started.\nPathetic." +
              ansi_reset)
        enter_name_save.append("user has surrendered")
        Checkers.write_to_file(self, enter_name_save)
        exit()
      else:
        print(ansi_red + "Illegal input!" + ansi_reset)
    while True:
      self.print_matrix(
      )  #this is the main loop that is used to print the board
      if self.player_turn is True:  #checks if its the players turn to move
        print(ansi_cyan + "\nPlayer's turn." + ansi_reset)
        self.get_player_input(
        )  #this is the main loop that is used to get the player's input
      else:
        print(ansi_magenta + "Computer's turn." + ansi_reset)
        print("Thinking...")
        self.evaluate_states(
        )  #this is the main loop that is used to evaluate the states of the board
      if self.player_pieces == 0:  #checks if the computer has won because the player hasn't got enough pieces
        self.print_matrix(
        )  #this is the main loop that is used to print the board
        enter_name_save.append("had no pieces left")
        Checkers.write_to_file(self, enter_name_save)
      elif self.computer_pieces == 0:  #checks if the computers pieces are equal to 0, in this case the player wins
        self.print_matrix(
        )  #this is the main loop that is used to print the board
        print(ansi_green + "Computer has no pieces left.\nYOU WIN!" +
              ansi_reset)
        enter_name_save.append(
          "Beat the computer as the computer had no pieces left")
        Checkers.write_to_file(self, enter_name_save)
        exit()
      elif self.computer_pieces - self.player_pieces == 7:  #normally in checkers, the loser must surrender and if you have less than 7-8 pieces you are most likely going to lose
        wish = input(
          "You have 7 pieces fewer than your opponent.Do you want to surrender?"
        )
        if wish == "" or wish == "yes":
          print(ansi_red + "You lost GGs" + ansi_reset)
          enter_name_save.append(
            "lost by having 7 less pieces than the opponent")
          Checkers.write_to_file(self, enter_name_save)
          exit()
      self.player_turn = not self.player_turn  #if its the players turn it will make it the computers turn once it has run all of the above statements


 # if __name__ == '__main__': 
 #     checkers = Checkers()
 #   checkers.play()

checkers = Checkers()


# game = Checkers()

# test_board = deepcopy(game.matrix)
# print(test_board)

# game.find_player_available_moves()

# game.find_player_available_moves(test_board, False)

# print(game.matrix)

# print(game.check_player_moves(, 1, 2, 3, 2))

# print(game.available_moves)
# print(game.mandatory_jumping)
# test_position_computer_player()
