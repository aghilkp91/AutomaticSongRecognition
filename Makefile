.PHONY: install flake flake add_audio add_directory recognize

install:
	@echo "*** Installing dependencies ***"
	pip3 install -r requirements.txt

flake:
	@echo "*** Linting python code ***"
	flake8 . --ignore="E501"

create_db:
	@echo "*** Creating the database ***"
	python3 createDatabase.py

add_audio:
	@echo "*** Adding specific Audio to database ***"
	python3 SongRecognition.py add-audio $(song_path)

add_directory:
	@echo "*** Adding all audios to db***"
	python3 SongRecognition.py add-audio $(song_dir)

recognize:
	@echo "*** Running song recognition ***"
	python3 SongRecognition.py recognzie $(song_path)
