import getpass

class BuildDir():
	def getPath(self):
		return '/home/' + getpass.getuser() + '/work/testpoky'
