# ask for song
# get lyrics
# get the most streamed part
# loop through most streamed part and collect an array of words
# find songs that contain said words in them
# use backtracking to fit the titles to form lyrics
import requests
import re
import spacy
import os
import base64
from dotenv import load_dotenv

nlp = spacy.load("en_core_web_sm")
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# def get_token():
#     auth_string = client_id + ":" + client_secret
#     auth_bytes = auth_string.encode("utf-8")
#     auth_base64 = str(base64.b64decode(auth_base64),"utf-8")
#
#     url = "https://accounts.spotify"
#
def search_tracks(word):
    url = "https://api.deezer.com/search"

    params = {
        "q": word,
        "limit": 30,
        "output": "json"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        tracks = data.get("data", [])
        return tracks
    else:
        print("Error:", response.status_code)


def get_exact_match_track(trackslist, word):
    for track in trackslist:
        if track['title'].lower() == word.lower():
            return track
    return None

def full_appearance(substring, string):
    pattern = rf'\b{re.escape(substring)}\b'
    match = re.search(pattern, string)
    return match is not None

# print(full_appearance("ever had the feeling","have you ever"))

def main():
    lyriclist = []
    matched_tracks = []
    with open("lyrics", "r") as file:
        for line in file:
            words = line.split()
            for word in words:
                lyriclist.append(word)
    # Remove brackets and insides
    pattern = r"\(.*?\)"
    lyriclist = re.sub(pattern,"", " ".join(lyriclist)).split(" ")

    for i in range(len(lyriclist)):
        for j in range(1, min(6, len(lyriclist) - i) + 1):
            phrase = ' '.join(lyriclist[i:i + j])
            # print(f"Searching for tracks for '{phrase}'...")
            tracks_list = search_tracks(phrase)
            for track in tracks_list:
                if track['title'].lower() == phrase.lower():
                    matched_tracks.append(track)
                    break
            else:
                continue
            break
        else:
            continue

    i=1
    while i <= len(matched_tracks)-1:
        if full_appearance(matched_tracks[i]['title'].lower(), matched_tracks[i-1]['title'].lower()):
            matched_tracks.pop(i)
            i=1
            continue
        i+=1


    for track in matched_tracks:
        print(track['title'], "==", track["artist"]["name"])


if __name__ == "__main__":
    main()



# search_query = "hello"  # Your search query
# tracks = search_tracks(search_query)
#
# print(track['rank'],track['title'], "by", track["artist"]['name'])