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


class sound_grid_view(object):
	""" View of sound grid model """

	def __init__(self,model,size):
		self.model = model
		self.screen = pygame.display.set_mode(size)
		
	def draw(self):
		""" Draws the blocks to the pygame window """
		self.screen.fill(pygame.Color('black'))
		for column in self.model.blocks:
			for block in column:
				r = pygame.Rect(block.left,
								block.top,
								block.size,
								block.size)
				pygame.draw.rect(self.screen, block.color,r)
		pygame.display.update()             


class sound_grid_model(object):
	""" Represents the interaction state for the visualization """

	def __init__(self, width, height):
		self.width = width
		self.height = height

		self.margin = 5
		self.block_no = 15
		self.block_size = (size[0] - self.margin *(self.block_no + 1)) /self.block_no
		
		self.block_ranges = []
		block_range_column = []

		self.blocks = []
		column = []

		# generates columns of blocks by sweeping x- and y-axes
		# blocks stored in self.blocks
		for left in range(self.margin, #beginning of range
						  self.width - self.margin - self.block_size, #end of range
						  self.margin + self.block_size): #step size
			for top in range(self.margin, 
							 self.height,
							 self.margin + self.block_size):
			  	if len(column) <= self.block_no - 1:
					column.append(block(left, top, self.block_size))
					block_range_column.append(((left, left + self.block_size), (top, top + self.block_size)))
			if len(self.blocks) <= self.block_no - 1:
				self.blocks.append(column)
				self.block_ranges.append(block_range_column)
				column = []
				block_range_column = []


class block(object):
	""" Represents a block in the musical visualization grid """

	def __init__(self, left, top, size, color = dark_grey):
		self.left = left
		self.top = top
		self.size = size
		self.color = color


class controller(object):
	""" Manages user input """
	def __init__(self, model):
		self.model = model
		self.toggle = [[0 for row in range(self.model.block_no)] for column in range(self.model.block_no)]

		# sound initializations
		pygame.mixer.set_num_channels(self.model.block_no) # sets number of channels to number of blocks
		self.sounds = ['Sounds/Note1.aiff',
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
		    A wave of grey moves out from the block clicked

		    event: pygame event while running"""

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
						
	def play_column(self, column):
		""" Plays selected block sounds in the current column on separate channels 

			column: current column index
		"""

		for row in range(len(self.toggle[column])):
			if self.toggle[column][row]:
				sound = pygame.mixer.Sound(self.sounds[row])
				sound.play(0)
				self.model.blocks[column][row].color = white
		for row in range(len(self.toggle[column - 1])):
			if self.toggle[column-1][row]:
				self.model.blocks[column - 1][row].color = grey


if __name__ == '__main__':
	pygame.init()
	size = (420,420)

	model = sound_grid_model(size[0],size[1])
	view = sound_grid_view(model,size)
	controller = controller(model)
	running = True

	prev_time = pygame.time.get_ticks()
	time_index = 0
	deltaT = 150

	while running: 
		if pygame.time.get_ticks() - prev_time > deltaT:
			prev_time = pygame.time.get_ticks()
			time_index +=1
			if time_index == model.block_no:
			    time_index = 0
			controller.play_column(time_index)

		cursor_position = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			else:
				controller.handle_event(event)
		
		view.draw()
		time.sleep(.001)