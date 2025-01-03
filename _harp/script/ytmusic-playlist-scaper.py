from ytmusicapi import YTMusic
import json
import csv
from datetime import datetime
import requests

############################ main
# retrieve json from API
playlist_id = "LRYR5MmaE_IYfzLrqQkSot42Pazmlcb7Z1LcT"
api_key = "AIzaSyD-2MmJytmZA0h-JuTaja2Y48S-8zUhF3s"

url = "https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&part=snippet&maxResults=100&playlistId=%s&key=%s" % (playlist_id, api_key)
res = requests.get(url)

data = res.json()

# convert json to csv
# json_file = './pinocchiop.json'

# with open(json_file, encoding="utf8") as json_data:
#     data = json.load(json_data)

songs = []
fields = ["videoId", "title", "singer"]
for item in data.get("items"):
    ### object ver
    # song = dict()
    # song["title"] = item["snippet"]["title"]
    # song["singer"] = item["snippet"]["videoOwnerChannelTitle"]
    # song["videoId"] = item["contentDetails"]["videoId"]
    # songs.append(song)
    
    ### array ver for simple csv writer
    song = []
    song.append(item["contentDetails"]["videoId"])
    song.append(item["snippet"]["title"])
    song.append(item["snippet"]["videoOwnerChannelTitle"])
    songs.append(song)
    print(123)
# print(songs)

# save to csv
filename = "song_list.csv"
# filename = "song_list" + datetime.today().strftime('%Y_%m_%d_%H_%M_%S') + ".csv"

with open(filename, 'w', encoding="utf8", newline='') as f:
    
    # Create a CSV writer object that will write to the file 'f'
    csv_writer = csv.writer(f)
    
    # Write the field names (column headers) to the first row of the CSV file
    csv_writer.writerow(fields)
    
    # Write all of the rows of data to the CSV file
    csv_writer.writerows(songs)




