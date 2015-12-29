import unittest
import time

class TestVideo(unittest.TestCase):
	def setUp(self): 
		print "setup video test"
	
	def tearDown(self):
		print "cleanup video test"

	def test_Playback(self):
		print "playback video"

	def test_Capture(self):
		print "capture video"

	def test_Sync(self):
		print "Sync video"
		time.sleep(3)

if __name__ == '__main__':
    unittest.main()
