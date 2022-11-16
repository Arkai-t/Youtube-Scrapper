import pytest

from VideoParser import VideoParser

class TestVideoParser:

    def testUrlValid(self):
        v = VideoParser("https://www.youtube.com/watch?v=4wTADlDJRQs")
        assert(v.description is None) is True

    def testUrlInvalid(self):
        with pytest.raises(Exception, match=r"URL given is not valid. Make sure you use a valid Youtube URL !") :
            v = VideoParser("notAnURL")

    def testVideoDoesntExist(self):
        with pytest.raises(Exception, match=r"This video doesn't exist !"):
            v = VideoParser("https://www.youtube.com/watch?v=kldjfmqlksf")

    def testgetTitle(self):
        v = VideoParser("https://www.youtube.com/watch?v=4wTADlDJRQs")
        assert(v._getTitle() == "Le droit est-il aussi strict qu'on le croit ?") is True

    def testgetAuthor(self):
        v = VideoParser("https://www.youtube.com/watch?v=4wTADlDJRQs")
        assert(v._getAuthor() == "Linguisticae") is True

    # Validate test in real condition
    def testgetLikes(self):
        v = VideoParser("https://www.youtube.com/watch?v=zfMhwHzS8J4")
        assert(v._getLikes() == 1) is True
    
    def testgetNoLink(self):
        v = VideoParser("https://www.youtube.com/watch?v=zfMhwHzS8J4")
        assert(len(v._getLinks()) == 0) is True

    def testgetLinks(self):
        v = VideoParser("https://www.youtube.com/watch?v=4wTADlDJRQs")
        assert(len(v._getLinks()) == 11) is True

    def testgetSpecificLinks(self):
        v = VideoParser("https://www.youtube.com/watch?v=4wTADlDJRQs")
        assert(v._getLinks()[0] == "http://utip.io/linguisticae") is True

    def testDescription(self):
        v = VideoParser("https://www.youtube.com/watch?v=zfMhwHzS8J4")
        desc = "Test de mon avion \u00e0 d\u00e9collage horizontal et vertical, avec le \\\"nouveaux\\\" dlc breaking ground expansion"
        assert(v._getDescription() == desc) is True

    def testNoComments(self):
        v = VideoParser("https://www.youtube.com/watch?v=zfMhwHzS8J4")
        assert(len(v._getComments()) == 0) is True

    def testCommentValue(self):
        v = VideoParser("https://www.youtube.com/watch?v=zfMhwHzS8J4")
        assert(len(v._getComments()) == 0) is True

    def testCommentContent(self):
        v = VideoParser("https://www.youtube.com/watch?v=o3tRJcG-Pzs&ab")
        assert(v._getComments()[0]['Content'] == "Vends couleur rouge au plus offrant.") is True

    def testCommentAuthor(self):
        v = VideoParser("https://www.youtube.com/watch?v=o3tRJcG-Pzs&ab")
        assert(v._getComments()[0]['Author'] == "L\u00e9o - TechMaker") is True

    # Validate test in real condition
    def testCommentLikes(self):
        v = VideoParser("https://www.youtube.com/watch?v=o3tRJcG-Pzs&ab")
        assert(v._getComments()[0]['NbLikes'] == 475) is True