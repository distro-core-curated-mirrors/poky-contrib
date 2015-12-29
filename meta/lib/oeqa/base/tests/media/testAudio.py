import unittest
import time

class TestAudio(unittest.TestCase):
	def setUp(self): 
		print "setup audio test"
	def tearDown(self):
		print "cleanup audio test"

	def test_Playback(self):
 		print "playback audio"
		time.sleep(3)

	def test_Capture(self):
		print "capture audio"

	def test_Sync(self):
		print "Sync audio"
		time.sleep(2)

if __name__ == '__main__':
    unittest.main()
