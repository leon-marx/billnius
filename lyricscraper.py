from lyricsgenius import Genius
import pandas as pd
import os
import unicodedata

with open("./../genius_credentials.txt", "r") as f:
    CLIENT_ID, CLIENT_TOKEN = f.read().split(",")

# for file in os.listdir("./charts"):
#     df = pd.read_csv(f"./charts/{file}", sep=";", encoding="cp1252")
#     print(df.head())

df = pd.read_csv(f"./charts/{os.listdir('./charts')[160]}", sep=";", encoding="cp1252")
print(df.head())

genius = Genius(CLIENT_TOKEN, timeout=50)
for title, artist in zip(df["title"], df["artist"]):
    if "/" in title:
        title = title.replace("/", "-")
    if not os.path.exists(f"./songs/{title} by {artist}.txt"):
        song = genius.search_song(title, artist, get_full_info=False)
        try:
            with open(f"./songs/{title} by {artist}.txt", "w") as f:
                f.write(unicodedata.normalize("NFKD", song.lyrics).encode("ascii", "ignore").decode("utf-8"))
        except AttributeError:
            os.remove(f"./songs/{title} by {artist}.txt")
            print("Song not found, searching again ignoring the artist.")
            song = genius.search_song(title, get_full_info=False)
            try:
                with open(f"./songs/{title} by {artist} UNCERTAIN.txt", "w") as f:
                    f.write(unicodedata.normalize("NFKD", song.lyrics).encode("ascii", "ignore").decode("utf-8"))
            except AttributeError:
                os.remove(f"./songs/{title} by {artist} UNCERTAIN.txt")
                print(f"This song does not seem to exist: {title} by {artist}")
                with open(f"./songs/{title} by {artist} MISSING.txt", "w") as f:
                    f.write(f"MISSING: This song does not seem to exist: {title} by {artist}")
