from lyricsgenius import Genius, PublicAPI
from langdetect import detect


with open("./../genius_credentials.txt", "r") as f:
    CLIENT_ID, CLIENT_SECRET, CLIENT_TOKEN = f.read().split(",")

genius = Genius(CLIENT_TOKEN)

# song_list = genius.search_songs("me porto bonito bad bunny", per_page=5)
# id_list = [song_list["hits"][i]["result"]["id"] for i in range(len(song_list))]
# lyrics_list = []
# song = 0
# for id in id_list:
#     s = genius.search_song(song_id=id)
#     lyrics_list.append(s.lyrics)
#     if detect(lyrics_list[-1]) == "es":
#         song = s
#         break
ff = ["Featuring"]
artist = "Post Malone Featuring Ozzy Osbourne & Travis Scott"
for flag in ff:
    if flag in artist.split(" "):
        new_artist = artist.split(" ")[:artist.split(" ").index(flag)]
        new_artist = " ".join(new_artist)
        print(new_artist)

print("done")
