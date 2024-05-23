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

def remove_consecutive_duplicates(text):
    words = text.split()
    cleaned_text = [words[0]]  # Start with the first word

    # Iterate over the words starting from the second one
    for i in range(1, len(words)):
        # If the current word is not the same as the previous one, add it to the cleaned text
        if words[i] != words[i - 1]:
            cleaned_text.append(words[i])

    # Join the cleaned words back into a string
    return ' '.join(cleaned_text)


def get_matchability_score(lyric_list,matched_tracks):
    words_in_matches = [track['title'].lower() for track in matched_tracks] # returns array
    cleaned_word_in_matches = remove_consecutive_duplicates(" ".join(words_in_matches))
    count=0
    for word in lyric_list:
        if word in cleaned_word_in_matches:
            count += 1
    return round((count/len(lyric_list)*100),2)

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
    print(lyriclist)
    for i in range(len(lyriclist)):
        for j in range(1, min(8, len(lyriclist) - i) + 1):
            phrase = ' '.join(lyriclist[i:i + j])
            print(f"Searching for titles phrassed: '{phrase}'...")
            tracks_list = search_tracks(phrase)
            for track in tracks_list:
                if track['title'].lower() == phrase.lower():
                    matched_tracks.append(track)
                    print("Found")
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
        print(track['title'], "_________________", track["artist"]["name"])

    print(f"Match Score: {get_matchability_score(lyriclist, matched_tracks)}%")

if __name__ == "__main__":
    main()



# search_query = "hello"  # Your search query
# tracks = search_tracks(search_query)
#
# print(track['rank'],track['title'], "by", track["artist"]['name'])