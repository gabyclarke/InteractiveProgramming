"""Music visualization
	Grid Form"""
import pygame
from pygame.locals import QUIT, KEYDOWN
import time
from random import choice
from math import sqrt


global block_ranges
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
		self.block_no = 12
		self.BLOCK_SIZE = (size[0] - self.MARGIN *(self.block_no + 1)) /self.block_no
		

		global block_ranges
		#create dictionary for  block ranges
		block_ranges = []
		block_range_column = []


		# leftIndex = 0
		# topIndex = 0
		#create dictionary for blocks
		# self.blocks = dict()
		self.blocks = []
		column = []
		#left edge of each block
		for left in range(self.MARGIN, #beginning of range
						  self.width - self.MARGIN - self.BLOCK_SIZE, #end of range
						  self.MARGIN + self.BLOCK_SIZE): #step size
		  #top edge of each block
			for top in range(self.MARGIN, 
							 self.height,
							 self.MARGIN + self.BLOCK_SIZE):
			  #assign each block an index number

				column.append(Block(left, top, self.BLOCK_SIZE))
				block_range_column.append(((left, left + self.BLOCK_SIZE), (top, top + self.BLOCK_SIZE)))
			 	#assign block_ranges an index number
				# block_ranges[leftIndex][topIndex] = ((left, left + self.BLOCK_SIZE), (top, top + self.BLOCK_SIZE))
				# topIndex +=1
				# index +=1
			self.blocks.append(column)
			block_ranges.append(block_range_column)
			# leftIndex +=1
			column = []
			block_range_column = []


	#def update(self):
	#	"""Update the model state"""



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

	def handle_event(self, event):
		""" When a block is clicked, the color of the block changes color and a sound plays
		    A wave of grey moves out from the block clicked"""
		pygame.mixer.music.load('Cobwebs.mp3')

		global block_ranges

		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
		
			cursor_position = pygame.mouse.get_pos() # get cursor position

			for column in range(len(block_ranges)):
				for row in range(len(block_ranges[column])):
					if cursor_position[0] in range(block_ranges[column][row][0][0], block_ranges[column][row][0][1]):
						if cursor_position[1] in range(block_ranges[column][row][1][0], block_ranges[column][row][1][1]):
							pygame.mixer.music.play(0)
							clicked = self.model.blocks[column][row]
							clicked.color= white


			# # for index, block_range in block_ranges.items():
					# if cursor_position[0] in (range(block_ranges[block_range_column][block_range][0][0], 
			# 										block_ranges[block_range_column][block_range][0][1]) 
			# 										and cursor_position[1] in range(block_ranges[block_range_column][block_range][1][0],
			# 										block_ranges[block_range_column][block_range][1][1])):
			# 			pygame.mixer.music.play(0)
			# 			print block_range_column_index, block_range_index
			# 			clicked = self.model.blocks[block_range_column][block_range]
			# 			clicked.color= white

			# 			left = block_range[0][0]
			# 			top = block_range[1][0]
			# 			unit = self.model.MARGIN + self.model.BLOCK_SIZE
						# for index, block_range in block_ranges.items():
						# 	gradient = self.model.blocks[index]

						# 	if (block_range[0][0] in range(left - unit - 1, left + unit + 1)
						# 			and block_range[1][0] in range(top - unit - 1, top + unit + 1)):
						# 		if block_range[0][0] == left and block_range[1][0] == top:
						# 			gradient.color = white
						# 		else:
						# 			gradient.color = light_grey
				# 	block_range_index += 1
				# block_range_column_index += 1
								
		# if event.key == pygame.K_ESCAPE:
		# 	running = False


									# elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
		# 	print "Button Released" 
		# 	print pygame.mouse.get_pos()
 
		# if pygame.mouse.get_pressed()[0]:
		# 	self.model.block.color = 'white'

# class PyGameTime(object):
# 	def __init__(self, time=0):
# 		self.time = time

# 	def getTime(self):
# 		print pygame.time.get_ticks()


if __name__ == '__main__':
	pygame.init()
	size = (420,420)

	model = SoundGridModel(size[0],size[1])
	view = PyGameSoundGridView(model,size)
	controller = PyGameMouseController(model)
	running = True

	prevTime = pygame.time.get_ticks()
	deltaT = 1000

	while running: 
		if pygame.time.get_ticks() - prevTime > deltaT:
			prevTime = pygame.time.get_ticks()
			print prevTime
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			else:
				controller.handle_event(event)
		#model.update()
		view.draw()
		time.sleep(.001)