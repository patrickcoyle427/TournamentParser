# TournamentParser
Parses .wer files (XML files created by Wizards Event Reporter) and
pull out the names and player ID number of each indivdual player, and the event date.

It uses this information to award points to players. These points are given to the player for participation
and how well they do in a tournament. Files are dropped into a folder that is created the first time the script is run.
Once the user has placed all .wer files they wish to be scanned in the appropriate folder, the script scans the files,
then moves them to a new folder. Finally, the results are exported to a .csv for easy viewing.

# Usage
On first run of this script, two directories will be created in the same
directory as this file: to_parse and parsed_events

Place .wer files that need to be scanned into the to_parse folder.

.wer Files will be found and scanned from that folder, parsed for the player's
 wins and draws, and then moved into parsed_events

After all events are scanned, script exports results found into a .csv file

This script will pick up any .csv files named Points Standings DD-MM-YYYY
when new files are scanned. If there is only one choice, that .csv will be
automatically loaded and added to the new .csv file.

If there is more than one option, the user will be prompted for their choice
of which .csv file should be used.

# The Future
My plan is to eventually encorporate parsing .Tournament files (Konami Tournament Software xml files) into this eventuall
