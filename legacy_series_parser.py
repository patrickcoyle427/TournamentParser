#!usr/bin/python3
'''
Legacy Series Parser

Parses .wer files to determine the points each player will receive towards
the legacy championship
'''

# TODO:

# Add ability to see if tournament has a top 8 play off and base the points
    # earned on that.
    # It is possible to see if a playoff was done in the event tag.
    # The attribute playoffstartround="n" holds this info

# Figure out a way to keep updating the same spreadsheet

# allow multiple file scans in a day. Find a way to scan new data without
    # adding in the same file multiple times

import xml.etree.ElementTree as ET

import csv, datetime, os.path

# ElementTree - used for parsing the .wer files, which are essentially xml files
# csv - used for exporting the results of this script for easy reading
# datetime - used for finding the date for use in the .csv file's filename
# ospath - used to check for multiple versions of .csv files with the same date

def start_parse():

    # runs script through each step of the parsing process

    files_exist = file_check()

    if files_exist:

        events = scan_for_events()

        player_dict = parse_events(events)

        move_files(events)

        print_points(player_dict)

def file_check():

    # will create necessary folders on first launch of program,
    # then will pass each other time. Gives a message to let the user
    # know what to do

    if os.path.isdir('to_parse') and os.path.isdir('parsed_events'):

        return True


    else:

        for i in ['to_parse', 'parsed_events']:

            if not os.path.isdir(i):

                os.makedirs(i)

        print('Folders for .wer files created. Place all files that need to be parsed',
              'into the "to_parse" folder, then run this script again.')

        return False

def scan_for_events():

    # Checks the to_parse folder for .wer events, then passes the list of files
    # to the parser to be scanned and then moved.

    return [file for file in os.listdir('to_parse') if file.endswith('.wer')]

def load_root(to_parse):

    # Loads and returns the root to be used in the start_parse function

    mtg_tree = ET.parse(f'to_parse/{to_parse}')

    mtg_root = mtg_tree.getroot()

    return mtg_root

def parse_events(event_list):

    # Adds participation points for wins and draws to the player's dict

    # wins are determined based on match.get('outcome') return results
    # if outcome == '1' match was played normally with a winner and loser
    # if outcome == '2' match was a draw
    # if outcome == '3' player had no opponent and was awarded a bye.
        # a bye is considered a win.

    players_dict = {}

    for event in event_list:

        root = load_root(event)
        # loads the xml file root

        event_players = get_players(root)
        # Gets the players in the event and adds them to the player dict in
        # the next for loop

        for player in event_players:

            # loops over the event players and adds them to dict if they
            # aren't already there. If they are, just adds the participation point

            dci_num = player[0]
            player_name = player[1]
            player_points = player[2]

            if players_dict.get(dci_num) == None:

                players_dict[dci_num] = [player_name, player_points]

            else:

                players_dict[dci_num][1] + 1

        for match in root.iter('match'):

            outcome = match.get('outcome')

            if outcome == '1' or outcome == '3':

                player_id = match.get('person')
                # person stores the winner's dci number

                players_dict[player_id][1] += 1
                # index one is the number of points the player has.
                # Increments their points by 1 for a win

            elif outcome == '2':

                player_1_id = match.get('person')
                
                players_dict[player_1_id][1] += .5

                player_2_id = match.get('opponent')
                
                players_dict[player_2_id][1] += .5

    return players_dict


def get_players(mtg_root):

    # Builds a list of players, which is returned to parse_events to be
    # added to the dictionary of players
    
    # The value stored is a list of lists that holds the following data:
    # 0: The player's dci number
    # 1: the player's full name
    # 2: The points earned through playing in the event. This is set to 1
        # as each player receives a participation point.

    player_list = []
        
    for person in mtg_root.iter('person'):

        idnum = person.get('id')
        # DCI number
        
        first = person.get('first')
        middle = person.get('middle')
        last = person.get('last')

        full_name = last + ' ' + first

        if middle != '':

            full_name += ' ' + middle

        player_list.append([idnum, full_name, 1])
        # creates a list that is added to the player_list list
        # adds their DCI Number, full name, and 1 indicating number of
        # points earned for the tournamnet qualifier. Each player
        # gets 1 participation point, which is added now.
        
    return player_list

def print_points(players_by_id):

    # Exports the points tallied

    today = datetime.date.today()

    year, month, day = today.year, today.month, today.day
    # used for the filename of the csv file

    filename = f'Point Standings {month}-{day}-{year}.csv'

    if os.path.exists(filename) != True:

        with open(filename, 'w', newline='') as csvfile:

            fieldnames = ['DCINumber', 'Name', 'Points']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for k, v in players_by_id.items():

                writer.writerow({'DCINumber': k, 'Name': v[0], 'Points': v[1]})

    else:

        print('Scan already done today')
        # not a permenant solution
        # fix later.

##    for k, v in players_by_id.items():
##
##        print(f'{k} ({v[0]}): {v[1]}')

def move_files(event_list):

    # moves all files parsed to a new folder so the user knows they
    # were checked

    for event in event_list:

        os.rename(f'to_parse/{event}', f'parsed_events/{event}')
                
def merge_old_results():

    # takes a previous .csv file, opens it, and merge's its points
    # with the ones that are now being scanned

    pass

if __name__ == '__main__':

    start_parse()
