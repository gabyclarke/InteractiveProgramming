"""Sound Grid
	SoftDes Spring 2016 MP4: Interactive Programming
	Gaby Clarke and Kristyn Walker"""

import pygame
from pygame.locals import QUIT, KEYDOWN
import time
from random import choice
from math import sqrt

#colors used
white = (255,255,255)
dark_grey = pygame.Color(105,105,105)
grey = (169,169,169)
light_grey= (220,220,220)


class PyGameSoundGridView(object):
	"""View of sound grid model """
	def __init__(self,model,size):
		self.model = model
		self.screen = pygame.display.set_mode(size)
		

	def draw(self):
		"""Draw the blocks to the pygame window"""
		self.screen.fill(pygame.Color('black'))
		for column in self.model.blocks:
			for block in column:
				r = pygame.Rect(block.left,
								block.top,
								block.size,
								block.size)
				pygame.draw.rect(self.screen, block.color,r) #pygame.Color(block.color), r)
		pygame.display.update()             



class SoundGridModel(object):
	"""Represents the interaction state for the visualization"""
	def __init__(self, width, height):
		self.width = width
		self.height = height

		self.MARGIN = 5
		self.block_no = 15
		self.BLOCK_SIZE = (size[0] - self.MARGIN *(self.block_no + 1)) /self.block_no
		

		# global block_ranges
		self.block_ranges = []
		block_range_column = []

		self.blocks = []
		column = []

		for left in range(self.MARGIN, #beginning of range
						  self.width - self.MARGIN - self.BLOCK_SIZE, #end of range
						  self.MARGIN + self.BLOCK_SIZE): #step size
			for top in range(self.MARGIN, 
							 self.height,
							 self.MARGIN + self.BLOCK_SIZE):
			  	if len(column) <= self.block_no - 1:
					column.append(Block(left, top, self.BLOCK_SIZE))
					block_range_column.append(((left, left + self.BLOCK_SIZE), (top, top + self.BLOCK_SIZE)))
			if len(self.blocks) <= self.block_no - 1:
				self.blocks.append(column)
				self.block_ranges.append(block_range_column)
				column = []
				block_range_column = []




class Block(object):
	"""Represents a block in the musical visualization grid"""
	def __init__(self, left, top, size, color = dark_grey):
		self.left = left
		self.top = top
		self.size = size
		self.color = color

class PyGameMouseController(object):
	def __init__(self, model):
		self.model = model
		self.toggle = [[0 for row in range(self.model.block_no)] for column in range(self.model.block_no)]

		# mouse event state initializations
		self.mousePressed = False
		self.mouseDown = False
		self.mouseReleased = False

		# sound initializations
		pygame.mixer.set_num_channels(self.model.block_no) # sets number of channels to number of blocks
		self.Sounds = ['Sounds/Note1.aiff',
						'Sounds/Note2.aiff',
						'Sounds/Note3.aiff',
						'Sounds/Note5.aiff',
						'Sounds/Note6.aiff',
						'Sounds/Note7.aiff',
						'Sounds/Note8.aiff',
						'Sounds/Note10.aiff',
						'Sounds/Note11.aiff',
						'Sounds/Note12.aiff',
						'Sounds/Note13.aiff',
						'Sounds/Note15.aiff',
						'Sounds/Note16.aiff',
						'Sounds/Note17.aiff',
						'Sounds/Note18.aiff',]
		

	def handle_event(self, event):
		""" When a block is clicked, the color of the block changes color and a sound plays
		    A wave of grey moves out from the block clicked"""

		if event.type == QUIT:
			return

		if event.type == KEYDOWN:
			if event.key == pygame.K_ESCAPE:
			   pygame.quit()
			   return

		for column in range(len(self.model.block_ranges)):
			for row in range(len(self.model.block_ranges[column])):
				if cursor_position[0] in range(self.model.block_ranges[column][row][0][0],
																self.model.block_ranges[column][row][0][1]):
					if cursor_position[1] in range(self.model.block_ranges[column][row][1][0],
												self.model.block_ranges[column][row][1][1]):
						if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
							
							clicked = self.model.blocks[column][row]

							if self.toggle[column][row] == 0:
								clicked.color= grey
								self.toggle[column][row] = 1
							else: #toggle[column][row] == 1:
								clicked.color= dark_grey
								self.toggle[column][row] = 0

						
	def playColumn(self, column):
		""" plays selected block sounds in the current column on separate channels 

			column: current column index
		"""

		for row in range(len(self.toggle[column])):
			if self.toggle[column][row]:
				sound = pygame.mixer.Sound(self.Sounds[row])
				sound.play(0)
				self.model.blocks[column][row].color = white
		for row in range(len(self.toggle[column - 1])):
			if self.toggle[column-1][row]:
				self.model.blocks[column - 1][row].color = grey


if __name__ == '__main__':
	pygame.init()
	size = (420,420)

	model = SoundGridModel(size[0],size[1])
	view = PyGameSoundGridView(model,size)
	controller = PyGameMouseController(model)
	running = True

	prevTime = pygame.time.get_ticks()
	timeIndex = 0
	deltaT = 150

	while running: 
		if pygame.time.get_ticks() - prevTime > deltaT:
			prevTime = pygame.time.get_ticks()
			timeIndex +=1
			if timeIndex == model.block_no:
			    timeIndex = 0
			controller.playColumn(timeIndex)

		cursor_position = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			else:
				controller.handle_event(event)
		
		view.draw()
		time.sleep(.001)