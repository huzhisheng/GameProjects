import pygame
root = '.'

class Wall(pygame.sprite.Sprite):
	def __init__(self,scene,initPos,direct):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(root+"/TestPic/wall.png").convert()
		self.rect=self.image.get_rect()
		self.rect.center=initPos
		self.speed=1
		self.direct=direct
		self.scene=scene
		self.timeCount=300
	def action(self):
		self.timeCount-=1
		if self.timeCount<=0:
			self.scene.walls.remove(self)
		if self.direct==1:
			self.rect.left += self.speed
		else:
			self.rect.left -= self.speed
	def collision(self):
		for r in self.scene.charList:
			if pygame.sprite.collide_rect_ratio(1)(self,r):
				if self.rect.centerx<r.rect.centerx:
					r.leftWall=True
					r.rect.left=self.rect.right
				else:
					r.rightWall=True
					r.rect.right=self.rect.left