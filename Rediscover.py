import json
import os
import csv
import msgspec


def convert_path(path):
    """
    Checks if the path string has quotations and removes them if so.
    """
    if path[0] == "\"" and path[-1] == "\"":
        return path[1:-1]
    else:
        return path

def get_favourites():
    """
    Converts the YourLibrary.json containing liked songs into a list.
    """
    fav_dir = convert_path(input("YourLibrary.json path: "))

    while fav_dir[-16:]!= "YourLibrary.json":
        print("Invalid path.")
        fav_dir = convert_path(input("YourLibrary.json path: "))

    with open(fav_dir, encoding="utf8") as file:
        global favourites_list
        favourites_list = msgspec.json.decode(file.read())["tracks"]

def read_files():
    """
    Creates a list containing streams from every streaming data file in a directory.
    """
    global streaming_list
    streaming_list = []
    streams_dir = convert_path(input("Extended Streaming History path: "))

    for name in os.listdir(streams_dir):
        # Skips files that don't contain stream data.
        if name[0:3] != "Str": continue

        with open(os.path.join(streams_dir, name), encoding = "utf-8") as file:
            streams = msgspec.json.decode(file.read())
            streaming_list.extend(streams)

def find_tracks():
    """
    Finds streams of songs that aren't in the user's liked songs and adds the song's data to a dictionary.
    """
    global tracks_dict
    tracks_dict = {}

    for stream in streaming_list:
        found_match = False
        uri = stream["spotify_track_uri"]
        name = stream["master_metadata_track_name"]
        album = stream["master_metadata_album_album_name"]
        artist = stream["master_metadata_album_artist_name"]
        date = stream["ts"][0:10]
        # Ignores empty streams (stream files sometimes have incomplete data).
        if stream["master_metadata_track_name"] is None: continue
        # Ignore streams that weren't finished.
        if stream["reason_end"] != "trackdone": continue

        # Compares the artists and track names to see if the song has been liked. The URIs (song ID) aren't compared because a song can have multiple URIs.
        if name in [i["track"] for i in favourites_list] and artist in [i["artist"] for i in favourites_list]:
            continue

        for track in tracks_dict:
            if tracks_dict[track]["name"] == name and tracks_dict[track]["artist"] == artist:
                tracks_dict[track]["plays"] += 1
                tracks_dict[track]["last listen"] = date
                found_match = True
                break

        if not found_match:   
            tracks_dict[uri] = {
                "name": name,
                "album": album,
                "artist": artist,
                "first listen": date,
                "last listen": date,
                "plays": 1}

def create_file():
    """
    Creates a CSV file containing streamed tracks that weren't liked along with stream data.
    """
    fieldnames = ["name", "album", "artist", "first listen", "last listen", "plays"]

    with open(r"C:\Users\natth\Documents\Rediscover.csv", mode = 'w', newline = '', encoding ='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tracks_dict.values())

if __name__ == "__main__":
    get_favourites()
    read_files()
    find_tracks()
    create_file()