# Rediscover
This Python program reads your streaming history and favourite songs to produce a spreadsheet containing songs you forgot to like.

First, request your Extended Streaming History and account data from Spotify. Extract these files. Enter the path of YourLibrary.json (located in the account data folder) and the Extended Streaming History folder into the program. The spreadsheet will be in Documents, titled Rediscover.csv.

The program compares song titles and artist names because a song can have multiple IDs. As a result, a song you've liked may appear in your spreadsheet if the song/artist name has changed.
If you have trouble with formatting in Excel import the file by going to the Data tab and clicking "From Text/CSV".
