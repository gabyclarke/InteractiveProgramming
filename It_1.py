"""Music visualization
	Grid Form"""
import pygame
from pygame.locals import QUIT, KEYDOWN
import time
from random import choice

class PyGameSoundGridView(object):
	"""View of sound grid model """

class SoundGridModel(object):
	"""Represents the interaction state for the visualization"""
	def __init__(self, width, height):
		self.width = width
		self.height = height

		self.BLOCK_SIZE = 20
		self.MARGIN = 5

		self.blocks = []
		for left in range(self.MARGIN, #beginning of range
						  self.width - self.MARGIN - self.BLOCK_SIZE, #end of range
						  self.MARGIN + self.BLOCK_SIZE): #step size
			for top in range(self.MARGIN, 
							 self.height,
							 self.MARGIN + self.BLOCK_SIZE):
				self.blocks.append(Block(left,
										 top,
										 self.BLOCK_SIZE))
	#def update(self):
		#"""Update the model state"""



class Block(object):
	"""Represents a block in the musical visualization grid"""
	def __init__(self, left, top, width, height):
		""""Initializes a block object with the geometry and color"""
		self.left = left
		self.top = top
		self.width = height
		self.color = color