# TournamentParser
Parses a tournament file (an XML file created by either Wizards Event Reporter or Konami Tournament Software)

# What will this do?

- Reads the names and player ID number of participants

- If it is their first time being read, creates a record in a sqlite db.

- If they have already played, increases their tournament points by a user specified number

  - Allows the user to specify how many points should be awarded for entering and if there are any additional
    points for placement
    
 - Record number of participants and date so graphs of tournament attendance can be made

 - Able to select the top x point scorers or all players that meet a certain threshold so they can qualify for
   a special event.

  - Ability to generate a report based on this information
