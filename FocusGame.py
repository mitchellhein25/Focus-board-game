# author: Mitchell Hein
# date: 11/13/20
# description: This program represents the Focus Game. It creates a board and two players, and allows them to play
#   the game turn by turn.

class Player:
    """Represents a player object, with a name, color, reserve, and captured.
    The players will be used in the game and their methods will be used to set the reserves,
    captured, and color checks throughout the game"""

    def __init__(self, player_name, player_color):
        """Initializes the player name and color, as well as sets their reserve
        and captured to 0."""
        self._player_name = player_name
        self._player_color = player_color
        self._player_reserve = 0
        self._player_captured = 0

    def get_player_name(self):
        """Returns player's name"""
        return self._player_name

    def get_player_color(self):
        """Returns player's color"""
        return self._player_color

    def get_player_reserve(self):
        """Returns player's reserve"""
        return self._player_reserve

    def add_player_reserve(self):
        """Adds 1 to the player's reserves"""
        self._player_reserve += 1

    def dec_player_reserve(self):
        """Subtracts 1 to the player's reserves"""
        self._player_reserve -= 1

    def get_player_captured(self):
        """Returns player's captured"""
        return self._player_captured

    def add_player_captured(self):
        """Adds 1 to the player's captured"""
        self._player_captured += 1

class FocusGame:
    """Represents the Game Class. This class will communicate with the Player class by using player objects to check various
    attributes of the players on their turns, such as the Player's color, reserves, and captured."""

    def __init__(self, player_tuple_1, player_tuple_2):
        """Initializes both players be creating player objects, Sets the current turn to 0,
        and initializes the board."""
        self._player_1 = Player(player_tuple_1[0], player_tuple_1[1])
        self._player_2 = Player(player_tuple_2[0], player_tuple_2[1])
        self._current_turn = 0      # May have a value of 1 or player object

        #Create the board by creating a list of 6 lists.
        self._board = [[], [], [], [], [], []]

        #Starting at zero, create the 0,2,4 rows with the alternating colors by referring to the player's colors
        for line in range(0,6,2):
            self._board[line] = [[self._player_1.get_player_color()], [self._player_1.get_player_color()], [self._player_2.get_player_color()],
                              [self._player_2.get_player_color()], [self._player_1.get_player_color()], [self._player_1.get_player_color()]]

        # Starting at 1, create the 1,3,5 rows with the alternating colors by referring to the player's colors
        for line in range(1,7,2):
            self._board[line] = [[self._player_2.get_player_color()], [self._player_2.get_player_color()], [self._player_1.get_player_color()],
                            [self._player_1.get_player_color()], [self._player_2.get_player_color()], [self._player_2.get_player_color()]]

    def get_board(self):
        """returns the board property"""
        return self._board

    def print_board(self):
        """Prints out the current board"""
        for row in self.get_board():
            print(row)

    def get_player(self, player_name):
        """Gets the player object, by name. It grabs both player object and then
        returns the one with the correct name."""
        player_1 = self._player_1
        player_1_name = player_1.get_player_name()

        player_2 = self._player_2
        player_2_name = player_2.get_player_name()

        if player_2_name == player_name:
            return player_2

        if player_1_name == player_name:
            return player_1

    def get_current_turn(self):
        """Returns whose turn it is"""
        return self._current_turn

    def set_current_turn(self, player):
        """Changes the current turn"""
        self._current_turn = player

    def get_other_player(self, player):
        """Gets the other player from the one entered, by player object"""
        if player == self._player_1:
            return self._player_2

        if player == self._player_2:
            return self._player_1

    def validate_turn(self, player, start_coord, end_coord, num_pieces):
        """This method is used in the make_move method to validate that the player
        trying to make a move is the correct player"""

        #If someone has already won
        if self.get_current_turn() == "Game is over.":
            return "Game is over."

        # Make sure it is the currect players turn
        if self.get_current_turn() != player:
            return 'not your turn'

        # if the player provides invalid locations (source or destination), return 'invalid location'

        #if the start and end location are the same
        if start_coord == end_coord:
            return 'invalid location'

        # if the they are trying to move more spots than their number of pieces allows
        if start_coord[0] - end_coord[0] > num_pieces or start_coord[0] - end_coord[0] < -1*num_pieces:
            return 'invalid location'
        if start_coord[1] - end_coord[1] > num_pieces or start_coord[1] - end_coord[1] < -1*num_pieces:
            return 'invalid location'

        #If they are trying to make a diagonal move
        if start_coord[1] - end_coord[1] == num_pieces and start_coord[0] - end_coord[0] == num_pieces:
            return 'invalid location'
        if start_coord[1] - end_coord[1] == -1*num_pieces and start_coord[0] - end_coord[0] == -1*num_pieces:
            return 'invalid location'
        if start_coord[1] - end_coord[1] == -1*num_pieces and start_coord[0] - end_coord[0] == num_pieces:
            return 'invalid location'
        if start_coord[1] - end_coord[1] == num_pieces and start_coord[0] - end_coord[0] == -1*num_pieces:
            return 'invalid location'

    def greater_than_five(self, location, size, player):
        """Assisting method to make_move. Adds the bottom pieces to the reserve or captured of the moving player"""

        end_coord_pieces = location
        bottom_pieces = end_coord_pieces[:size-5]

        #for ea piece, if it is the moving player's color, add it to reserves,
        # otherwise, add it to captured
        for piece in bottom_pieces:
            location.pop(0)
            if piece == player.get_player_color():
                player.add_player_reserve()
            else:
                player.add_player_captured()

    def move_execution(self, num_pieces, end_location, start_location, start_pieces):
        """Executes the move of the player"""

        #If multiple move
        if num_pieces > 1:

            #Grab the number of pieces the player wants to move
            move_pieces = start_pieces[(len(start_pieces) - num_pieces):(len(start_pieces))]

            #Add the players to the destination list on the board
            end_location += move_pieces

            #remove those pieces from the starting location
            for x in range(len(move_pieces)):
                start_location.pop()

        #If single move, move to the destination location and remove a piece from
        # the starting location
        else:
            end_location.append(start_pieces[0])
            start_location.pop()

    def move_piece(self, player_name, start_coord, end_coord, num_pieces):
        """Method for a player to make a move. Determine if move is valid, and then execute."""
        player = self.get_player(player_name)

        #If this is the first turn, set the current player to be the current turn
        if self.get_current_turn() == 0:
            self.set_current_turn(player)

        #validate the users turn and locations with validate_turn method
        validate_turn_location = self.validate_turn(player, start_coord, end_coord, num_pieces)

        #If the turn is not valid and returns a string, then return that string
        if validate_turn_location:
            return validate_turn_location

        #get list of pieces at start location
        start_pieces = self.show_pieces(start_coord)

        #Make sure the player's piece is on top of stack
        if start_pieces == []:
            return 'invalid number of pieces'
        top_start = start_pieces[len(start_pieces) - 1] #last piece in start_coord list
        if top_start != player.get_player_color():
            return 'invalid location'

        end_location = self.get_board()[end_coord[1]][end_coord[0]]

        start_location = self.get_board()[start_coord[1]][start_coord[0]]

        #Execute the move with the helper method
        self.move_execution(num_pieces, end_location, start_location, start_pieces)

        end_coord_size = len(end_location)

        #If the destination loation is greater than five
        # use the helper function to assign the bottom pieces to the correct place
        if end_coord_size > 5:
            self.greater_than_five(end_location, end_coord_size, player)

        #If the player has captured 6 or more pieces, they have won
        if player.get_player_captured() >= 6:
            self.set_current_turn("Game is over.")
            return player.get_player_name() + " Wins"


        #change turns
        self.set_current_turn(self.get_other_player(player))

        return 'successfully moved'


    def show_pieces(self, location):
        """returns a list showing the pieces that are present at that location with the bottom-most pieces
        at the 0th index of the array and other pieces on it in the order."""

        column_num = location[0]    #x-coord
        row_num = location[1]       #y-coord

        board = self.get_board()

        return board[row_num][column_num]


    def show_reserve(self, player_name):
        """shows the count of pieces that are in reserve for the player. If no pieces are in reserve, return 0.
        Using the player's get reserve method"""

        player = self.get_player(player_name)
        return player.get_player_reserve()

    def show_captured(self, player_name):
        """shows the number of pieces captured by that player. If no pieces have been captured, return 0.
        Using the player's get captured method"""

        player = self.get_player(player_name)
        return player.get_player_captured()

    def reserved_move(self, player_name, location):
        """It places the piece from the reserve to the location. It should reduce the reserve
        pieces of that player by one and make appropriate adjustments to pieces at the location.
        If there are no pieces in reserve, return 'no pieces in reserve'"""

        #Get the player and their reserves
        player = self.get_player(player_name)
        reserves = player.get_player_reserve()

        if reserves == 0:
            return 'no pieces in reserve'

        if self.get_current_turn() == "Game is over.":
            return "Game is over."

        # Make sure it is the currect players turn
        if self.get_current_turn() != player:
            return 'not your turn'

        board = self.get_board()
        location = board[location[0]][location[1]]
        color = player.get_player_color()

        #Add their piece to the location
        location.append(color)

        #If the destination has more than 5 pieces
        if len(location) > 5:
            self.greater_than_five(location, len(location), player)

        #Decrease the player reserves by 1
        player.dec_player_reserve()

        #Determine if the player has won
        if player.get_player_captured() >= 6:
            self.set_current_turn("Game is over.")
            return player.get_player_name() + " Wins"

        #change turns
        self.set_current_turn(self.get_other_player(player))

        return 'successfully moved'

# #
# fg = FocusGame(("Mitch", "R"), ("Hannah", "W"))
# fg.print_board()
# print(fg.move_piece("Mitch", (0,0), (0,1), 1))
# fg.print_board()
# print(fg.show_pieces((0,1)))
# print(fg.show_pieces((0,0)))
# fg.print_board()
# print(fg.show_pieces((0,1)))
# print(fg.move_piece("Hannah", (0,2), (0,1), 1))
# fg.print_board()
# print(fg.show_pieces((0,1)))
# print(fg.move_piece("Mitch", (1,0), (2,0), 2))
# fg.print_board()
# print(fg.show_pieces((0,2)))
# print(fg.move_piece("Hannah", (3,0), (2,0), 1))
# fg.print_board()
# print(fg.show_pieces((2,0)))
# print(fg.move_piece("Mitch", (5,3), (5,2), 1))
# fg.print_board()
# print(fg.show_pieces((5,2)))
# print(fg.move_piece("Hannah", (2,0), (2,4), 4))
# fg.print_board()
# print(fg.show_pieces((2,4)))
# print(fg.move_piece("Mitch", (2,5), (2, 4), 1))
# fg.print_board()
# print(fg.show_pieces((2, 4)))
# # print(fg.get_player("Mitch").get_player_reserve())
# print(fg.move_piece("Hannah", (3,5), (3,4), 1))
# fg.print_board()
# print(fg.show_pieces((3,4)))
# print(fg.move_piece("Mitch", (5,2), (5,1), 1))
# fg.print_board()
# print(fg.show_pieces((5,1)))
# print(fg.move_piece("Hannah", (3,4), (2,4), 2))
# fg.print_board()
# print(fg.show_pieces((2,4)))
# print(fg.get_player("Hannah").get_player_reserve())
# print(fg.get_player("Hannah").get_player_captured())
# print(fg.move_piece("Hannah", (3,4), (2,4), 2))
# fg.print_board()
# print(fg.show_pieces((2,4)))
# print(fg.move_piece("Mitch", (5,1), (4,1), 2))
# fg.print_board()
# print(fg.show_pieces((4,1)))
# print(fg.move_piece("Hannah", (1,5), (1,4), 1))
# fg.print_board()
# print(fg.show_pieces((1,4)))
# print(fg.move_piece("Mitch", (4,1), (4,2), 3))
# fg.print_board()
# print(fg.show_pieces((4,2)))
# print(fg.move_piece("Hannah", (2,4), (2,1), 5))
# fg.print_board()
# print(fg.show_pieces((2,1)))
# print(fg.move_piece("Mitch", (4,2), (2,2), 4))
# fg.print_board()
# print(fg.show_pieces((2,2)))
# print(fg.move_piece("Hannah", (2,1), (0,1), 5))
# fg.print_board()
# print(fg.show_pieces((0,1)))
# print(fg.move_piece("Mitch", (0,5), (0,4), 1))
# fg.print_board()
# print(fg.show_pieces((0,4)))
# print(fg.move_piece("Hannah", (0,1), (0,4), 5))
# fg.print_board()
# print(fg.show_pieces((0,4)))
#
# print(fg.move_piece("Mitch", (4,5), (4,4), 1))
# fg.print_board()
# print(fg.show_pieces((4,4)))
# print(fg.move_piece("Hannah", (1,4), (0,4), 2))
# fg.print_board()
# print(fg.show_pieces((0,4)))
# print(fg.show_captured("Hannah"))
# print(fg.show_reserve("Hannah"))
# print(fg.move_piece("Mitch", (4,5), (4,4), 1))
# fg.print_board()
# print(fg.reserved_move("Hannah", (0,5)))
# print(fg.show_reserve("Hannah"))
# fg.print_board()
# print(fg.move_piece("Mitch", (4,5), (4,4), 1))
# fg.print_board()
# print(fg.reserved_move("Hannah", (0,5)))