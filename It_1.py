"""Music visualization
	Grid Form"""
import pygame
from pygame.locals import QUIT, KEYDOWN
import time
from random import choice
from math import sqrt


# global block_ranges
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
		self.block_no = 18
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
		""""Initializes a block object with the geometry and color"""
		self.left = left
		self.top = top
		self.size = size
		self.color = color

class PyGameMouseController(object):
	def __init__(self,model):
		self.model = model
		self.toggle = [[0 for row in range(self.model.block_no)] for column in range(self.model.block_no)]

		self.Sounds = ['Sounds/Note1.aiff',
						'Sounds/Note2.aiff',
						'Sounds/Note3.aiff',
						'Sounds/Note4.aiff',
						'Sounds/Note5.aiff',
						'Sounds/Note6.aiff',
						'Sounds/Note7.aiff',
						'Sounds/Note8.aiff',
						'Sounds/Note9.aiff',
						'Sounds/Note10.aiff',
						'Sounds/Note11.aiff',
						'Sounds/Note12.aiff',
						'Sounds/Note13.aiff',
						'Sounds/Note14.aiff',
						'Sounds/Note15.aiff',
						'Sounds/Note16.aiff',
						'Sounds/Note17.aiff',
						'Sounds/Note18.aiff',]
		
		pygame.mixer.set_num_channels(self.model.block_no)

	def handle_event(self, event):
		""" When a block is clicked, the color of the block changes color and a sound plays
		    A wave of grey moves out from the block clicked"""

		self.MousePressed = False
		self.MouseDown = False
		self.MouseReleased = False

		if event.type == QUIT:
			return

		if event.type == KEYDOWN:
			if event.key == pygame.K_ESCAPE:
			   pygame.quit()
			   return
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			self.MousePressed = True
			self.MouseDown = True
	  
		if event.type == pygame.MOUSEBUTTONUP:
		    self.MouseReleased = True
		    self.MouseDown = False

		# if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
		
		# 	cursor_position = pygame.mouse.get_pos() # get cursor position

    	if MousePressed:
			for column in range(len(self.model.block_ranges)):
				for row in range(len(self.model.block_ranges[column])):
					if cursor_position[0] in range(self.model.block_ranges[column][row][0][0],
																	self.model.block_ranges[column][row][0][1]):
						if cursor_position[1] in range(self.model.block_ranges[column][row][1][0],
													self.model.block_ranges[column][row][1][1]):
							
							clicked = self.model.blocks[column][row]

							if self.toggle[column][row] == 0:
								clicked.color= white
								self.toggle[column][row] = 1
							else: #toggle[column][row] == 1:
								clicked.color= dark_grey
								self.toggle[column][row] = 0

							# print self.toggle[column][row]
							
		# MousePressed = False
		# MouseReleased = False
						
	def playColumn(self, column):
		# print self.toggle[column]
		for row in range(len(self.toggle[column])):
			# print row
			if self.toggle[column][row]:
				# pygame.mixer.music.load(self.Sounds[row])
				sound = pygame.mixer.Sound(self.Sounds[row])
				# print self.Sounds[row]
				sound.play(0)
				# print sound.play(0)



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
			# playColumn()
			prevTime = pygame.time.get_ticks()
			timeIndex +=1
			if timeIndex == model.block_no:
			    timeIndex = 0
			controller.playColumn(timeIndex)
			# print prevTime
			# print timeIndex
		
		cursor_position = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			else:
				controller.handle_event(event)
		#model.update()
		view.draw()
		time.sleep(.001)