#!usr/bin/python3

'''
A quick script to find and display the info the main program will
need check for.
'''

import xml.etree.ElementTree as ET

# .wer file, from Wizards Event Reporter

mtg_file = 'SampleFiles/Magic_Tournament_10_29_18.wer'

mtg_tree = ET.parse(mtg_file)

mtg_root = mtg_tree.getroot()

mtg_count = 0
# counts done to see how many are lines are parsed.

for person in mtg_root.iter('person'):

    idnum = person.get('id')
    
    first = person.get('first')
    middle = person.get('middle')
    last = person.get('last')

    full_name = first + middle + last

    print(idnum, full_name)

    mtg_count += 1

print(mtg_count)
print()

# .tournament file, from the Konami Tournament Software

ygo_file = 'SampleFiles/Yugioh! Sun Tournament 10-28-18 (ID E18-105063).Tournament'

ygo_tree = ET.parse(ygo_file)

ygo_root = ygo_tree.getroot()

ygo_count = 0

for player in ygo_root.iter('Player'):

    idnum = player.find('ID')

    if idnum != None:
        
        # used because the .tournament files save two different tags
        # as <player>. This only wants the one that has the player's name
        # and ID
        
        idnum = player.find('ID').text
        firstname = player.find('FirstName').text
        lastname = player.find('LastName').text

        print(idnum, lastname, firstname)
        ygo_count += 1

print(ygo_count)
