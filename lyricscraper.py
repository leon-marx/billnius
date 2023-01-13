from lyricsgenius import Genius
import pandas as pd
import os
import unicodedata
from langdetect import detect

with open("./../genius_credentials.txt", "r") as f:
    CLIENT_ID, CLIENT_SECRET, CLIENT_TOKEN = f.read().split(",")

title_check = [
    "\\",
    "?",
    ".",
    ":",
    ",",
    ";",
    "/",
]
artist_check = [
    "Feat",
    "feat",
    "Featuring",
    "featuring",
    "With",
    "with",
    "And",
    "and",
    "&",
]

# for file in os.listdir("./charts"):
#     df = pd.read_csv(f"./charts/{file}", sep=";", encoding="cp1252")
#     print(df.head())

df = pd.read_csv(f"./charts/{os.listdir('./charts')[110]}", sep=";", encoding="cp1252")
print(df.head())

genius = Genius(CLIENT_TOKEN, timeout=50)
genius.remove_section_headers = True  # Remove stuff like [Chorus]
genius.skip_non_songs = True  # Skip lists
genius.verbose = False  # Less spam
for title, artist in zip(df["title"], df["artist"]):
    print(f'Searching for "{title}" by {artist}')
    for symbol in title_check:
        if symbol in title:
            # print("    TITLE PROBABLY WEIRD! REMOVING SPECIAL CHARACTERS...")
            title = title.replace(symbol, "")
    for flag in artist_check:
        if flag in artist.split(" "):
            # print("    ARTIST NAME PROBABLY WEIRD! TRYING SIMPLER NAME...")
            artist = artist.split(" ")[:artist.split(" ").index(flag)]
            artist = " ".join(artist)
    if not os.path.exists(f"./songs/{title} by {artist}.txt"):
        song = genius.search_song(title, artist, get_full_info=False)
        try:
            if detect(song.lyrics) != "en":
                print("    NON_ENGLISH SONG DETECTED! CHECKING FOR FALSE TRANSLATION...")
                songs = genius.search_artist(artist, max_songs=5)
                d = []
                for s in songs.songs:
                    d.append(detect(s.lyrics))
                lang = max(set(d), key=d.count)
                if detect(song.lyrics) != lang:  # TRANSLATION DETECTED
                    print("        TRANSLATION DETECTED! TRYING TO FIND ORIGINAL VERSION...")
                    song_list = genius.search_songs(f"{title} {artist}", per_page=5)
                    id_list = [song_list["hits"][i]["result"]["id"] for i in range(len(song_list))]
                    lyrics_list = []
                    song = 0
                    for id in id_list:
                        s = genius.search_song(song_id=id)
                        lyrics_list.append(s.lyrics)
                        if detect(lyrics_list[-1]) == lang:
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
                if detect(song.lyrics) != "en":
                    songs = genius.search_artist(artist, max_songs=10)
                    d = []
                    for s in songs.songs:
                        d.append(detect(s.lyrics))
                    lang = max(set(d), key=d.count)
                    if detect(song.lyrics) != lang:  # TRANSLATION DETECTED
                        print("        TRANSLATION DETECTED! TRYING TO FIND ORIGINAL VERSION...")
                        song_list = genius.search_songs(f"{title} {artist}", per_page=5)
                        id_list = [song_list["hits"][i]["result"]["id"] for i in range(len(song_list))]
                        lyrics_list = []
                        song = 0
                        for id in id_list:
                            s = genius.search_song(song_id=id)
                            lyrics_list.append(s.lyrics)
                            if detect(lyrics_list[-1]) == lang:
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
