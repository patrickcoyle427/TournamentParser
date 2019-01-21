#!usr/bin/python3
'''
Legacy Series Parser

Parses .wer files to determine the points each player will receive towards
the legacy championship
'''

# TODO:

# Read a folder of tournament files, collect the number of wins and draws
    # from those events and then move the files to a new folder.
# Add ability to see if tournament has a top 8 play off and base the points
    # earned on that.
    # It is possible to see if a playoff was done in the event tag.
    # The attribute playoffstartround="n" holds this info
# Export points to a spreadsheet for easy viewing.
    # Figure out a way to keep updating the same spreadsheet

import xml.etree.ElementTree as ET

def start_parse(to_parse):

    # runs script through each step of the parsing process

    root = load_root(to_parse)

    player_dict = build_dict(root)

    print(player_dict)

    player_dict = add_win_points(player_dict, root)

    print_points(player_dict)

def load_root(to_parse):

    # Loads and returns the root to be used in the start_parse function

    mtg_tree = ET.parse(mtg_file)

    mtg_root = mtg_tree.getroot()

    return mtg_root

def build_dict(mtg_root):

    # Builds the player dictionary
    # Returns a dictionary of the players
    # The key is the player's dci number, a unique ID used for tournaments
    # The value stored is a list that holds the following data:
    # 0: the player's full name
    # 1: The number of wins the player has. Starts as 0 and built
        # upon in a later function
    # 2: The number of draws the player has. Starts as 0 and built
        # upon in a later function
    # 3: The points earned through playing in the event. This is set to 1
        # as each player receives a participation point.

    players_by_id = {}
    
    for person in mtg_root.iter('person'):

        idnum = person.get('id')
        # DCI number
        
        first = person.get('first')
        middle = person.get('middle')
        last = person.get('last')

        full_name = last + ' ' + first

        if middle != '':

            full_name += ' ' + middle

        players_by_id[idnum] = [full_name, 0, 0, 1]
        # creates a dict entry based on the player's dci number
        # adds their full name, a 0 indicating number of wins, a 0
        # that indicates number of draws, and 1 indicating number of
        # points earned for the tournamnet qualifier. Each player
        # gets 1 participation point, which is added now.
        
    return players_by_id

def add_win_points(players_by_id, mtg_root):

    # Adds participation points for wins and draws to the player's dict

    # wins are determined based on match.get('outcome') return results
    # if outcome == '1' match was played normally with a winner and loser
    # if outcome == '2' match was a draw
    # if outcome == '3' player had no opponent and was awarded a bye.
        # a bye is considered a win.

    for match in mtg_root.iter('match'):

        outcome = match.get('outcome')

        if outcome == '1' or outcome == '3':

            player_id = match.get('person')
            # person stores the winner's dci number

            players_by_id[player_id][1] += 1
            # index 1 holds the number of wins the player has

        elif outcome == '2':

            player_1_id = match.get('person')
            
            players_by_id[player_1_id][2] += 1
            # index 2 holds the number of draws the player has

            player_2_id = match.get('opponent')
            
            players_by_id[player_2_id][2] += 1

    for k, v in players_by_id.items():

        v[3] += v[1] * 1
        v[3] += v[2] * .5

    return players_by_id

def print_points(players_by_id):

    # Displays the points earned in the event

    for k, v in players_by_id.items():

        print(f'{k} ({v[0]}): {v[3]}')

if __name__ == '__main__':

    mtg_file = 'SampleFiles/Magic_Tournament_10_29_18.wer'
    # .wer file, from Wizards Event Reporter, basically an xml file
    # with a different name

    start_parse(mtg_file)
