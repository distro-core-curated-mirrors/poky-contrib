import os
from dogtail import tree
from dogtail.utils import run
import time
from dogtail.tree import predicate
from base import Base

print "===========Entering imagesShown==============="

try:
    bitbake = tree.root.application('bitbake')
except:
    print "can not connect to the application"
else:
    try:
        hob = bitbake.child( roleName='frame' )
    except:
        print "can not connect to the application"


class ImagesShown(Base):

	def images(self):	
		try:
			hob.child(name = 'Images').click()
		except:
			self.writeInFile("images shown: can not find Images button")
			return 10
		images = bitbake.child( roleName='dialog', name = 'Open My Images')

		while True:		
			try:
				imageList = images.findChildren(predicate.GenericPredicate(roleName="table cell"))
				break
			except TypeError:
				self.writeInFile("images shown: trying to get the list")
				return 10
		if len(imageList) <= 0:
			self.writeInFile("images shown: failed")
		else:
			self.writeInFile("images shown: passed")
		try:
			images.child("Cancel").click()
		except:
			self.writeInFile("images shown: can not find cancel button")
		return 10

