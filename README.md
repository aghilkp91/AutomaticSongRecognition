# AutomaticSongRecognition

This is an attempt to create a program for automatic song recognition for malayalam songs

To install the dependencies
	run "make install"

To create the database and tables for song recognition system
    First give the correct database login information to the variable "sqldb_url" in src/Config.py
    run "make create_db"

To add an add audio file into database
	run "make add_audio <song_file_path>"

To add all songs from a directory
    run "make add_directory <directory_path>"

To recognise a song
    run "make recognize <song_file_path>"
