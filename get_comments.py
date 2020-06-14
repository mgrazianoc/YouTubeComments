from googleapiclient.discovery import build
import json


# -------- CONFIGURATION ----------------------------------
def init_youtube_api():
    print("Initializing YouTube Api V3...")
    
    api_key = init_key()
    api = build("youtube", "v3", developerKey=api_key)
    return api


def init_key():
    print("Gathering user developer Key...")
    
    with open("Key.txt", 'r') as code:
        api_key = code.readline()
    return api_key



# -------- API use --------------------------------------

def get_comments(video_ID):
	print("Getting coments...")
	process = init_youtube_api()
	
	request = process.commentThreads().list(
		part = "snippet", videoId = video_ID,
		textFormat = "plainText",
		order = "relevance",
		maxResults = 100 # CHANGE THIS IF YOU WANT LESS, 0 < maxResults < 101
	)
	
	coments = request.execute()	
	return coments




# ----- FILTERING AND WRITING -----------------------------------

def filters(data):
	# SEE "raw_data_example.json" to see data with junk
	data = data["items"]
	
	clean_data = [{"Position": i+1} for i in range(len(data))]
	
	for i in range(len(data)):
		# content
		clean_data[i].update(
			{"Conteúdo": data[i]["snippet"]["topLevelComment"]["snippet"]["textOriginal"]}
		)
		
		# likes
		clean_data[i].update(
			{"Likes": data[i]["snippet"]["topLevelComment"]["snippet"]["likeCount"]})
		
		# replies
		clean_data[i].update(
		{"Replies": data[i]["snippet"]["totalReplyCount"]})
		
	
	return clean_data


def write_data(data, name):
	
	data = json.dumps(data, indent = 2)
	with open(name, "w") as file:
		file.write(str(data))


	
# --------- CHANGE THINGS HERE ---------------------------	
if __name__ == "__main__":
	# https://www.youtube.com/watch?v=VIDEO_ID
	VIDEO_ID = "JmdqHPgT6u8"
	
	# gettind data
	data = get_comments(VIDEO_ID)
	
	# cleaning junk
	data = filters(data)
	
	# FILE_NAME.json
	FILE_NAME = "hello_world"
	
	write_data(data, f"{FILE_NAME}.json")