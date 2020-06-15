class ASRConfig(object):
    audio_frame_rate = 44100
    audio_extension = ".mp3"
    supported_audio = [".mp3", ".m4a"]
    max_audio_process_num = 8
    max_process_num = 8
    enable_console_msg = True
    sqldb_url = 'mysql+mysqlconnector://root:pass@localhost:3306/songrecognition'
    mysql_max_connection = 128
    mysql_insert_number = 20000
    # if search subdirectories when using addAudioFromDir
    search_subdirectories = False
    def __init__(self):
        pass

