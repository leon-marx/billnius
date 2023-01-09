from lyricsgenius import Genius
import pandas as pd
import os

with open("./../genius_credentials.txt", "r") as f:
    CLIENT_ID, CLIENT_TOKEN = f.read().split(",")

# for file in os.listdir("./charts"):
#     df = pd.read_csv(f"./charts/{file}", sep=";", encoding='cp1252')
#     print(df.head())

df = pd.read_csv(f"./charts/{os.listdir('./charts')[0]}", sep=";", encoding='cp1252')
print(df.head())

genius = Genius(CLIENT_TOKEN)
for title, artist in zip(df["title"], df["artist"]):
    song = genius.search_song(title, artist)
    try:
        with open(f"./songs/{title} by {artist}.txt", "w") as f:
            f.write(song.lyrics)
    except AttributeError:
        print("Song not found, searching again ignoring the artist.")
        song = genius.search_song(title)
        try:
            with open(f"./songs/{title} by {artist} UNCERTAIN.txt", "w") as f:
                f.write(song.lyrics)
        except AttributeError:
            print(f"This song does not seem to exist: {title} by {artist}")
            with open(f"./songs/{title} by {artist} MISSING.txt", "w") as f:
                f.write(f"MISSING: This song does not seem to exist: {title} by {artist}")