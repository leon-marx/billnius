from lyricsgenius import Genius
import pandas as pd
import os
import unicodedata
import langdetect

with open("./../genius_credentials.txt", "r") as f:
    CLIENT_ID, CLIENT_SECRET, CLIENT_TOKEN = f.read().split(",")

special_check = [
    "\\",
    "?",
    ".",
    ":",
    ",",
    ";",
    "/",
    "*",
]
feat_check = [
    "Feat",
    "feat",
    "Feat.",
    "feat.",
    "Featuring",
    "featuring",
    "With",
    "with",
    "And",
    "and",
    "&",
    ",",
    ";",
    "X",  # Some features are depicted by X, added here because this is more common than artist names like "Lil Nas X", we hope the latter case is still found without the X
    "x",
]

# for file in os.listdir("./charts"):
#     df = pd.read_csv(f"./charts/{file}", sep=";", encoding="cp1252")
#     print(df.head())

df = pd.read_csv(f"./charts/{os.listdir('./charts')[0]}", sep=";", encoding="cp1252")
print(df.head())

genius = Genius(CLIENT_TOKEN, timeout=50)
genius.remove_section_headers = True  # Remove stuff like [Chorus]
genius.skip_non_songs = True  # Skip lists
genius.verbose = False  # Less spam
for title, artist in zip(df["title"], df["artist"]):
    print(f'Searching for "{title}" by {artist}')
    for flag in feat_check:
        if flag in artist.split(" "):
            # print("    ARTIST NAME PROBABLY CONTAINING A FEATURE! TRYING SIMPLER NAME...")
            artist = artist.split(" ")[:artist.split(" ").index(flag)]
            artist = " ".join(artist)
    for symbol in special_check:
        if symbol in title:
            # print("    TITLE PROBABLY WEIRD! REMOVING SPECIAL CHARACTERS...")
            title = title.replace(symbol, "")
        if symbol in artist:
            # print("    ARTIST PROBABLY WEIRD! REMOVING SPECIAL CHARACTERS...")
            artist = artist.replace(symbol, "")
    if not os.path.exists(f"./songs/{title} by {artist}.txt"):
        # song = genius.search_song(title, artist, get_full_info=False)
        try:
            song_id = genius.search_songs(f"{title} {artist}", per_page=1)["hits"][0]["result"]["id"]
            song = genius.search_song(song_id=song_id, get_full_info=False)
        except IndexError:
            song = None
        if song != None:
            if (song.lyrics.split().count("-") >= 5) | (sum([int(item.isnumeric()) for item in song.lyrics.split()]) >= 20):
                print("    POSSIBLE LIST DETECTED! TRYING AGAIN TO FIND THE LYRICS...")
                song_list = genius.search_songs(f"{title} {artist}", per_page=5)
                id_list = [song_list["hits"][i]["result"]["id"] for i in range(len(song_list))]
                lyrics_list = []
                song = 0
                for id in id_list:
                    s = genius.search_song(song_id=id)
                    if (s.lyrics.split().count("-") < 5) & ((s.lyrics.split().count("-") >= 5) | (sum([int(item.isnumeric()) for item in s.lyrics.split()])) < 20):
                        song = s
                        break
        try:
            if langdetect.detect(song.lyrics) != "en":
                print("    NON_ENGLISH SONG DETECTED! CHECKING FOR FALSE TRANSLATION...")
                songs = genius.search_artist(artist, max_songs=5)
                d = []
                for s in songs.songs:
                    try:
                        d.append(langdetect.detect(s.lyrics))
                    except langdetect.lang_detect_exception.LangDetectException:
                        continue
                lang = max(set(d), key=d.count)
                if langdetect.detect(song.lyrics) != lang:  # TRANSLATION DETECTED
                    print("        TRANSLATION DETECTED! TRYING TO FIND ORIGINAL VERSION...")
                    song_list = genius.search_songs(f"{title} {artist}", per_page=5)
                    id_list = [song_list["hits"][i]["result"]["id"] for i in range(len(song_list))]
                    lyrics_list = []
                    song = 0
                    for id in id_list:
                        s = genius.search_song(song_id=id)
                        lyrics_list.append(s.lyrics)
                        if langdetect.detect(lyrics_list[-1]) == lang:
                            song = s
                            break
        except AttributeError:
            pass
        try:
            with open(f"./songs/{title} by {artist}.txt", "w") as f:
                f.write(unicodedata.normalize("NFKD", song.lyrics).encode("ascii", "ignore").decode("utf-8"))
        except AttributeError:
            os.remove(f"./songs/{title} by {artist}.txt")
            print("    SONG NOT FOUND! TRYING AGAIN IGNORING THE ARTIST...")
            song = genius.search_song(title, get_full_info=False)
            try:
                if langdetect.detect(song.lyrics) != "en":
                    songs = genius.search_artist(artist, max_songs=10)
                    d = []
                    for s in songs.songs:
                        try:
                            d.append(langdetect.detect(s.lyrics))
                        except langdetect.lang_detect_exception.LangDetectException:
                            continue
                    lang = max(set(d), key=d.count)
                    if langdetect.detect(song.lyrics) != lang:  # TRANSLATION DETECTED
                        print("        TRANSLATION DETECTED! TRYING TO FIND ORIGINAL VERSION...")
                        song_list = genius.search_songs(f"{title} {artist}", per_page=5)
                        id_list = [song_list["hits"][i]["result"]["id"] for i in range(len(song_list))]
                        lyrics_list = []
                        song = 0
                        for id in id_list:
                            s = genius.search_song(song_id=id)
                            lyrics_list.append(s.lyrics)
                            if langdetect.detect(lyrics_list[-1]) == lang:
                                song = s
                                break
            except AttributeError:
                pass
            try:
                with open(f"./songs/{title} by {artist} UNCERTAIN.txt", "w") as f:
                    f.write(unicodedata.normalize("NFKD", song.lyrics).encode("ascii", "ignore").decode("utf-8"))
            except AttributeError:
                os.remove(f"./songs/{title} by {artist} UNCERTAIN.txt")
                print(f"    THIS SONG DOES NOT SEEM TO EXIST: {title} by {artist}")
                with open(f"./songs/{title} by {artist} MISSING.txt", "w") as f:
                    f.write(f"MISSING: This song does not seem to exist: {title} by {artist}")
