"""Music visualization
	Grid Form"""
import pygame
from pygame.locals import QUIT, KEYDOWN
import time
from random import choice

global block_ranges

class PyGameSoundGridView(object):
	"""View of sound grid model """
	def __init__(self,model,size):
		self.model = model
		self.screen = pygame.display.set_mode(size)
		

	def draw(self):
		"""Draw the blocks to the pygame window"""
		self.screen.fill(pygame.Color('black'))
		for block in self.model.blocks.values():
			r = pygame.Rect(block.left,
							block.top,
							block.size,
							block.size)
			pygame.draw.rect(self.screen, pygame.Color(block.color), r)
		pygame.display.update()


class SoundGridModel(object):
	"""Represents the interaction state for the visualization"""
	def __init__(self, width, height):
		self.width = width
		self.height = height

		self.BLOCK_SIZE = 20
		self.MARGIN = 5

		global block_ranges
		#create dictionary for  block ranges
		block_ranges = dict()

		index = 0
		#create dictionary for blocks
		self.blocks = dict()
		for left in range(self.MARGIN, #beginning of range
						  self.width - self.MARGIN - self.BLOCK_SIZE, #end of range
						  self.MARGIN + self.BLOCK_SIZE): #step size
			for top in range(self.MARGIN, 
							 self.height,
							 self.MARGIN + self.BLOCK_SIZE):
				self.blocks[index] = (Block(left,
										 	top,
										 	self.BLOCK_SIZE))
				block_ranges[index] = ((left, left + self.BLOCK_SIZE), (top, top + self.BLOCK_SIZE))
				index +=1


	#def update(self):
	#	"""Update the model state"""



class Block(object):
	"""Represents a block in the musical visualization grid"""
	def __init__(self, left, top, size,color = 'white'):
		""""Initializes a block object with the geometry and color"""
		self.left = left
		self.top = top
		self.size = size
		self.color = color

class PyGameMouseController(object):
	def __init__(self,model):
		self.model = model

	def handle_event(self, event):
		""" Look for mouse cursor position and clicks to 
		activate sound"""
		pygame.mixer.music.load('Cobwebs.mp3')

		global block_ranges

		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			print "Button Pressed" 	
			# b = choice(self.model.blocks)
			# b.color = "red"		
			cursor_position = pygame.mouse.get_pos() # get cursor position
			for index,block_range in block_ranges.items():
				if cursor_position[0] in range(block_range[0][0], block_range[0][1]) and cursor_position[1] in range(block_range[1][0], block_range[1][1]):
					
					# left = block_range[0][0]
					# top = block_range[1][0]
					pygame.mixer.music.play(0)
					# b = Block(left,top, self.model.BLOCK_SIZE,"blue")
					b = self.model.blocks[index]
					b.color= "blue"
					# b.color = "red"
					
					# print self.model.BLOCK_SIZE
     #        		print left, top
					# r = pygame.Rect(left,
					# 	top,blocks.app
					# 	block.size,  # INHERIT BLOCK_SIZE?
					# 	block.size)
					# pygame.draw.rect(self.screen, pygame.Color('white'), r)


		# elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
		# 	print "Button Released" 
		# 	print pygame.mouse.get_pos()
 
		# if pygame.mouse.get_pressed()[0]:
		# 	self.model.block.color = 'white'

if __name__ == '__main__':
	pygame.init()
	size = (420,420)

	model = SoundGridModel(size[0],size[1])
	view = PyGameSoundGridView(model,size)
	controller = PyGameMouseController(model)
	running = True
	while running: 
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			else:
				controller.handle_event(event)
		#model.update()
		view.draw()
		time.sleep(.001)