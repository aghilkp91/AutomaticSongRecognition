from . import Model
from .Config import ASRConfig
import time, gc


def log(end="\n", *msg):
    if not ASRConfig.enable_console_msg:
        return
    for m in msg:
        print(m);
    print(end);


def commandWrapper(func):
    if not ASRConfig.enable_console_msg:
        return lambda: func

    def wrapper(*args, **kwargs):
        print("--->")
        func(*args, **kwargs)
        print("<---\n")

    return wrapper


@commandWrapper
def addAudio(filepath):
    log("Check Song Hash")
    song = Model.Audio.initFromFile(filepath)

    log("-Adding audio %s to the database-" % song.filename)
    if song.isFingerprinted():
        log("Add song fail: song already been fingerprinted")
        return
    song.getId(new=True)
    log("Get Song id success: song id", song.id)
    log("Start read song data")
    song.read()
    log("Success")
    log("Start get fingerprints")
    t1 = time.time()
    song.getFingerprints()
    t2 = time.time()
    log("Success! (Time cost: %d sec, total number: %s ) " % (t2 - t1, len(song.fingerprints)))
    log("Start insert fingerprints")
    t1 = time.time()
    song.startInsertFingerprints()
    t2 = time.time()
    log("Insert fingerprints into database success (Time cost: %d sec)" % (t2 - t1))
    log("Add Song Success!")


@commandWrapper
def addAudioFromDir(dir):
    songs = Model.Audio.initFromDir(dir)
    for song in songs:
        if song.isFingerprinted():
            log("Add audio fail: file(%s) already been fingerprinted" % song.filename)
            continue

    songs = [song for song in songs if not song.isFingerprinted()]
    songs_num = len(songs)
    log("Have %d audio to process." % songs_num)
    for song in songs:
        song.getId(new=True)
        print("Song Id: %s, song name: %s" % (song.id, song.name))

    log("Start generate fingerprints.")
    for i in range(0, songs_num, ASRConfig.max_audio_process_num):
        tempnum = i + ASRConfig.max_audio_process_num if i + ASRConfig.max_audio_process_num <= songs_num else songs_num
        log("Processing %d/%d" % (tempnum, songs_num))
        t1 = time.time()
        total_threads = []
        running_threads = []
        st = 0
        for song in songs[i:i + ASRConfig.max_audio_process_num:]:
            total_threads.append(Model._getFingerprints(st, song))
            st += 1
        st = 0
        while st < len(total_threads):
            if len(running_threads) < ASRConfig.max_audio_process_num:
                total_threads[st].start()
                running_threads.append(total_threads[st])
                st += 1
                time.sleep(0.2)
                continue
            for t in running_threads:
                if not t.is_alive():
                    running_threads.remove(t)
        for t in total_threads:
            t.join()

        t2 = time.time()
        log("Finish! (Time cost: %d)" % (t2 - t1))

        for song in songs[i:i + ASRConfig.max_audio_process_num:]:
            log("Start insert fingerprints for %s" % song.name)
            t1 = time.time()
            song.startInsertFingerprints()
            song.cleanup()
            t2 = time.time()
            log("Insert fingerprints into database success (Time cost: %d sec)" % (t2 - t1))

        gc.collect()

    log("all audio have been added.")


@commandWrapper
def recognizeAudio(filepath):
    song = Model.Audio.initFromFile(filepath)
    log("Recognizing %s" % song.filename)
    log("Start read audio data......")
    song.read()
    log("Success")

    log("Start get fingerprints......")
    song.getFingerprints()
    log("Success (Total number: %s)" % len(song.fingerprints))

    log("Recognize......")
    t1 = time.time()
    result = song.recognize()
    t2 = time.time()
    if result["count"] == 0:
        log("Can not find any song fit this audio")
        return
    log("Most Possible: %s (fingerprints match: %s), using %d sec" % (result["name"], result["count"], t2 - t1))
