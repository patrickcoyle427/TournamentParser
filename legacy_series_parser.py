#!usr/bin/python3

'''
Legacy Series Parser

Parses .wer files to determine the points each player will receive towards
the legacy championship

Usage:

- On first run of this script, two directories will be created in the same
  directory as this file: to_parse and parsed_events

- Place .wer files that need to be scanned into the to_parse folder.

- .wer Files will be found and scanned from that folder, parsed for the player's
   wins and draws, and then moved into parsed_events

- After all events are scanned, script exports results found into a .csv file

- This script will pick up any .csv files named Points Standings DD-MM-YYYY
  when new files are scanned. If there is only one choice, that .csv will be
  automatically loaded and added to the new .csv file.

  If there is more than one option, the user will be prompted for their choice
  of which .csv file should be used.
'''

# TODO:

# LOL MAKE IT SO YOU CAN DO MULTIPLE SCANS ON THE SAME DAY
    # See find_old_results, it should probably look at the date of
    # file creation, not the name of the file lol
# Add ability to see if tournament has a top 8 play off and base the points
    # earned on that.
    # It is possible to see if a playoff was done in the event tag.
    # The attribute playoffstartround="n" holds this info
# I did a quick and dirty fix to make Wizards Event Reporter .xml files
    # work, and they scan fine, but should they be able to be read by this?
    # If I didn't do it already, maybe just have the script display an
    # error message for .xml files it can't scan and continue on it's way.
    # Maybe dump these files into a new folder so the user knows?
# Allow you to set point modifiers for events (like 10x points for example)

import xml.etree.ElementTree as ET

import csv, datetime, os, os.path, time

# ElementTree - used for parsing the .wer files, which are essentially xml files
# csv - used for exporting the results of this script for easy reading
# datetime - used for finding the date for use in the .csv file's filename
# os - used for creating folders and moving parsed files
# os.path - used for checking for tournament and .csv files

def start_parse():

    # runs script through each step of the parsing process

    dir_exist = dir_check()

    if dir_exist:

        old_points = find_old_results()

        events = scan_for_events()

        player_dict = parse_events(events, old_points)

        move_files(events)

        export_points(player_dict)

def dir_check():

    # will create necessary directories on first launch of program,
    # then will pass each other time. Gives a message to let the user
    # know what to do with the created directories.

    if os.path.isdir('to_parse') and os.path.isdir('parsed_events'):

        return True


    else:

        for i in ['to_parse', 'parsed_events']:

            if not os.path.isdir(i):

                os.makedirs(i)

        print('Folders for .wer files created. Place all files that need to be parsed',
              'into the "to_parse" folder, then run this script again.')

        return False

def find_old_results():

    # Finds the .csv files that have have been created by the parser.
    # Automatically loads the file if there is only 1 choice. Allows the user to choose
    # the file they would like to use if there is more than one possibility.
    
    old_results = [file for file in os.listdir() if file.endswith('.csv') and 'Point Standings' in file]
    # builds a list of all files that end with .csv

    if len(old_results) == 1:

        # if only 1 file is found, only that file is loaded

        return load_old_results(old_results[0])
        # returns the file name to be loaded by the load_old_results function

    elif len(old_results) > 1:

        print('Multiple result files detected. Please choose the results you would like to build upon.')
        # User choice to chose the .csv file they want to add to

        for index, result in enumerate(old_results):

            print(f'{index+1}. {result}')
            # prints all the results found

        load = False

        while load == False:

            try:
                
                choice = input('Please type the number of the file you wish to use: ')

                if int(choice) > len(old_results) or int(choice) < 1:

                    print(f'Not a valid choice. Please choose a number between 1 and {len(old_results)}')

                else:

                    print(f'File to be loaded: {old_results[int(choice)-1]}')
                    # Check to ensure the user is loading the correct file.

                    yn_choice = input('Is this correct? (y/n): ')
                    
                    if yn_choice.lower() in ['y', 'yes', 'yep']:

                        # any other choice besides yes will let you choose another file

                        return load_old_results(old_results[int(choice)-1])
                        # returns the file name to be loaded by the load_old_results function

                        #load = True
                        # breaks out of the load loop


            except ValueError:

                print('Please choose a number.')

    else:

        return None
        # Returns None if no old results are found so that the parse_events function can skip
        # adding anything.


def load_old_results(to_load):

    # loads the old results into the parser to be added to the most recent scan.
    # returns a list of lists to be added into the points dict

    loaded_results = []

    with open(to_load, newline='') as csvfile:

        reader = csv.DictReader(csvfile)

        for row in reader:

            loaded_results.append([row['DCINumber'], row['Name'], row['Points']])

    return loaded_results

def scan_for_events():

    # Checks the to_parse folder for .wer events, then passes the list of files
    # to the parser to be scanned and then moved.

    return [file for file in os.listdir('to_parse') if file.endswith('.wer') or file.endswith('.xml')]
    # list comp to find all .wer files in a folder, in case other files end
    # up in the to_parse folder.

def load_root(to_parse):

    # Loads and returns the root to be used in the start_parse function

    mtg_tree = ET.parse(f'to_parse/{to_parse}')

    mtg_root = mtg_tree.getroot()

    return mtg_root

def parse_events(event_list, old_results):

    # Adds points for wins and draws to the player's dict

    # wins are determined based on match.get('outcome') return results
    # if outcome == '1' match was played normally with a winner and loser
    # if outcome == '2' match was a draw
    # if outcome == '3' player had no opponent and was awarded a bye.
        # a bye is considered a win.

    # event_list - list containing file names of the tournaments about to be scanned
    # old_results - list of lists that holds players and their points from a previous csv file. Merges
    #               this data with the files being scanned.

    players_dict = {}

    for event in event_list:

        root = load_root(event)
        # loads the xml file root

        event_players = get_players(root)
        # Gets the players in the event and adds them to the player dict in
        # the next for loop

        # playoff_round = int(root.get('playoffstartround'))

        #if playoff_round > 0:

        # section will add additional points or calculate points differernt
        # if there is a playoff.

        # can use playoff round to find that match round
        # count the number of matches to determine what the cutoff was
        # Use that to award bonus points based on standing.


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

            # loop adds to the player's points based on wins or draws.
            # an outcome of '1' or '3' means a player received a win
            # an outcome of '2' means there is a draw

            outcome = match.get('outcome')

            if outcome == '1' or outcome == '3':

                player_id = match.get('person')
                # person stores the winner's dci number

                players_dict[player_id][1] += 3
                # index one is the number of points the player has.
                # Increments their points by 3 for a win

            elif outcome == '2':

                # awards 1 point to each player in a draw

                player_1_id = match.get('person')
                
                players_dict[player_1_id][1] += 1

                player_2_id = match.get('opponent')
                
                players_dict[player_2_id][1] += 11

        print(f'{event} scanned')

    if old_results != None and len(event_list) != 0:

        # won't create a new file if no new events are being added.

        # old_results is a list of lists containing:
        # 0: the player's dci number
        # 1: the player's name
        # 2: the player's point value from before.

        for player in old_results:

            # loop adds players from the previously scanned files into the currently built
            # players_dict.

            old_dci_num = player[0]
            old_player_name = player[1]
            old_player_points = float(player[2])

            old_points = players_dict.get(old_dci_num)

            if old_points == None:

                players_dict[old_dci_num] = [old_player_name, old_player_points]

            else:

                players_dict[old_dci_num][1] += old_player_points

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

def export_points(players_by_id):

    # Exports the points tallied

    # players_by_id - a dictionary. Keys are player dci numbers and it holds lists containing the
    #                 player's full name and number of points they have

    print(len(players_by_id))

    if len(players_by_id) != 0:
        
        # checking for a len of 0 so won't create a new file if no files were scanned

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

                print(f'{len(players_by_id)} players in {filename}')

    else:

        print('No new files found. No new points standings exported.')

def move_files(event_list):

    # moves all files parsed to a new folder so the user knows they
    # were checked

    for event in event_list:

        try:

            os.rename(f'to_parse/{event}', f'parsed_events/{event}')

        except FileExistsError:

            print(f'{event} could not be moved. File with same name in',
                  'your parsed_events folder.')

if __name__ == '__main__':

    start_parse()
