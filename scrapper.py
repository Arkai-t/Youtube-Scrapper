import sys
import json

from VideoParser import VideoParser

NB_COMMENTS = 5

# Test number of parameters
if(len(sys.argv) != 5):
    raise Exception("Numbers of parameters incorrect. \nUse ./scrapper.py --input input.json --output output.json")
# Test if parameters are correctly formated
if not (sys.argv[1] == "--input" or sys.argv[3] == "--input"):
    raise Exception("No input file given. \nUse ./scrapper.py --input input.json --output output.json")
if not (sys.argv[1] == "--output" or sys.argv[3] == "--output"):
    raise Exception("No output file given. \nUse ./scrapper.py --input input.json --output output.json")
if not (sys.argv[2].endswith(".json") and sys.argv[4].endswith(".json")):
    raise Exception("Files given are not JSON files. \nUse ./scrapper.py --input input.json --output output.json")

# Determine wich is input or output
if (sys.argv[1] == "--input"):
    inputFile, outputFile = sys.argv[2], sys.argv[4]
else :
    outputFile, inputFile = sys.argv[2], sys.argv[4]
    
# Parse input JSON
with open(inputFile, 'r') as f:
    videosId = json.load(f)['videos_id']

# Parse each video
res = []
for video in videosId:
    data = VideoParser("https://www.youtube.com/watch?v=" + video, NB_COMMENTS).getData()
    data['Id'] = video
    res.append(data)

with open(outputFile, 'w') as f:
    f.write(json.dumps(res, indent=4))

