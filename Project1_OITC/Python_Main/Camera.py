
import pygame
from pygame.locals import *
import pygame.sprite
class Camera(object):
	"""description of class"""
	def __init__(self,scene):
		self.speed_x=0
		self.speed_y=0
		self.scale=1.5
		self.scene=scene
		self.camera=self.scene.scene
		self.player=self.scene.player
		self.camera_width=int(1200/self.scale)
		self.camera_height=int(800/self.scale)
		self.center_x=self.camera_width/2
		self.center_y=self.camera_height/2
		self.bigger_bool=False
		self.smaller_bool=False
		self.biggerTimeCount=50
		self.smallerTimeCount=50
	def action(self):
		self.camera_width=int(1200/self.scale)
		self.camera_height=int(800/self.scale)

		self.speed_x=int((self.player.rect.centerx-self.center_x)/3)
		self.speed_y=int((self.player.rect.centery-self.center_y)/3)
		
		self.center_x=self.center_x+self.speed_x
		self.center_y=self.center_y+self.speed_y

		if self.center_x<self.camera_width/2:
			self.center_x=self.camera_width/2
		if self.center_x>1200-self.camera_width/2:
			self.center_x=1200-self.camera_width/2
		
		if self.center_y<self.camera_height/2:
			self.center_y=self.camera_height/2
		if self.center_y>900-self.camera_height/2:
			self.center_y=900-self.camera_height/2
		if self.bigger_bool==True:
			self.biggerTimeCount=self.biggerTimeCount-1
			if self.scale>1:
				self.scale=self.scale-0.01

			if self.biggerTimeCount<=0:
				self.bigger_bool=False
		if self.smaller_bool==True:
			self.smallerTimeCount=self.smallerTimeCount-1
			if self.scale<1.5:
				self.scale=self.scale+0.01
			if self.smallerTimeCount<=0:
				self.smaller_bool=False
		
	def bigger(self):
		print("asadasdasd")
		self.bigger_bool=True
		self.biggerTimeCount=50
		self.smaller_bool=False
	def smaller(self):
		self.bigger_bool=False
		self.smaller_bool=True
		self.smallerTimeCount=50
	def draw(self):
		wholeImage=self.scene.scene.subsurface(Rect(self.center_x-self.camera_width/2,self.center_y-self.camera_height/2,self.camera_width,self.camera_height)).convert()
		wholeImage=pygame.transform.scale(wholeImage,(1200,900)).convert()
		self.scene.scene.blit(wholeImage,(0,0))
		self.scene.drawHeart()
