from datetime import datetime
import csv
import requests

# Function to fetch playlist items with pagination
def fetch_playlist_items(playlist_id, api_key):
    base_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    max_results = 50  # Maximum results per request

    all_items = []  # List to store all items

    next_page_token = None
    while True:
        params = {
            'part': 'contentDetails,snippet',
            'maxResults': max_results,
            'playlistId': playlist_id,
            'key': api_key
        }
        if next_page_token:
            params['pageToken'] = next_page_token

        res = requests.get(base_url, params=params)
        data = res.json()

        items = data.get("items", [])
        all_items.extend(items)

        next_page_token = data.get('nextPageToken')
        if not next_page_token:
            break

    return all_items

# Main code
playlist_id = "OLAK5uy_nKNj-77TZN5SmK5IGyXskvVZoM9OGok7g"
api_key = "AIzaSyD-2MmJytmZA0h-JuTaja2Y48S-8zUhF3s"

playlist_items = fetch_playlist_items(playlist_id, api_key)

songs = []
fields = ["videoId", "title", "singer"]

for item in playlist_items:
    song = [
        item["contentDetails"]["videoId"],
        item["snippet"]["title"],
        item["snippet"]["videoOwnerChannelTitle"]
    ]
    songs.append(song)

filename = "../guessSongAsset/songlist.csv"

with open(filename, 'w', encoding="utf-8", newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(fields)
    csv_writer.writerows(songs)

print("Total videos fetched:", len(songs))