import json
import re
import requests
from bs4 import BeautifulSoup
from typing import List

# From https://github.com/egbertbouman/youtube-comment-downloader
from youtube_comment_downloader import *
from itertools import islice

class VideoParser:
    soup : BeautifulSoup
    url : str
    description : str
    nbComments : int

    def __init__(self, url : str, nbComments : int = 5) -> None:
        # Test if we have a valid Youtube URL
        if not(url.startswith("https://www.youtube.com/watch?v=") and len(url) > 33):
            raise Exception("URL given is not valid. Make sure you use a valid Youtube URL !")

        html = requests.get(url)        
        self.soup = BeautifulSoup(html.text, "html.parser")

        # Test if video exist
        if(self.soup.find("meta", itemprop="name") is None):
            raise Exception("This video doesn't exist !")

        self.url = url
        self.description = None
        self.nbComments = nbComments

    def _getTitle(self) -> str: 
        return self.soup.find("meta", itemprop="name")['content']

    def _getAuthor(self) -> str: 
        return self.soup.find("span", itemprop="author").next.next['content']

    def _getLikes(self) -> int:
        #From https://www.javatpoint.com/how-to-extract-youtube-data-in-python
        data = re.search(r"var ytInitialData = ({.*?});", self.soup.prettify()).group(1)  
        data_json = json.loads(data)  
        videoPrimaryInfoRenderer = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']
        likes_label = videoPrimaryInfoRenderer['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonRenderer']['likeButton']['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label'] 
        
        likes = re.sub(r'[^0-9]', '', likes_label)
        return int(likes)
        

    def _getDescription(self) -> str:
        #From https://stackoverflow.com/questions/72354649/how-to-scrape-youtube-video-description-with-beautiful-soup
        pattern = re.compile(r'(?<=shortDescription":").*(?=","isCrawlable)')
        self.description = pattern.findall(str(self.soup))[0].replace('\\n','\n')

        return self.description

    def _getLinks(self) -> List[str]:
        if(self.description is None):
            self.description = self._getDescription()
        
        description = self.description

        # Get Links
        #From https://stackoverflow.com/questions/839994/extracting-a-url-in-python
        res = re.findall(r"(?P<url>https?://[^\s]+)", description)

        # Get Timestamp
        res += re.findall(r"[0-9]+:[0-9]{2}", description)

        return res

    def _getComments(self) -> List[dict]:
        downloader = YoutubeCommentDownloader()
        comments = downloader.get_comments_from_url(self.url, sort_by=SORT_BY_POPULAR)

        #Filter informations from comments
        res = []
        for comment in islice(comments, self.nbComments):
            c = {}
            c['Author'] = comment['author']
            c['Content'] = comment['text']
            c['NbLikes'] = int(comment['votes'])

            res.append(c)

        return res

    def getData(self) -> dict :
        d = {}
        d['Title'] = self._getTitle()
        d['Author'] = self._getAuthor()
        d['NbLikes'] = self._getLikes()
        d['Description'] = self._getDescription()
        d['Links'] = self._getLinks()
        d['Comments'] = self._getComments()

        return d