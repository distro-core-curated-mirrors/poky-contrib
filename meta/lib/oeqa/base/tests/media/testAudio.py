import unittest
import time
from util.tag import tag
from util.timeout import timeout

@tag(type="audio")
class TestAudio(unittest.TestCase):
	def setUp(self): 
		print "setup audio test"

	def tearDown(self):
		print "cleanup audio test"

        @tag("sanity")
        @timeout(2) 
	def test_Playback(self):
 		print "playback audio"
		time.sleep(3)

	def test_Capture(self):
		time.sleep(3)
		print "capture audio"

        @timeout(5) 
	def test_Sync(self):
		print "Sync audio"
		time.sleep(2)

if __name__ == '__main__':
    unittest.main()
