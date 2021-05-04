import pygame
root = '.'
class Bullet(pygame.sprite.Sprite):
	def __init__(self, scene,initPos,direct,power,createrId):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(root+"/TestPic/bullet_new.png").convert_alpha()			
		self.rect = self.image.get_rect()
		self.rect.midtop = initPos
		self.speed = 20
		self.direct = direct
		self.power=power
		self.image=pygame.transform.scale(self.image,(int(self.rect.width*(self.power/10)),int(self.rect.height*(self.power/10))))
		#发出这颗子弹的角色Id
		self.createrId=createrId
		self.scene=scene
		self.damaged=[]
		self.imageCount=0
		for i in range(len(self.scene.charList)):
			self.damaged.append(1)
		self.image=pygame.transform.scale(self.image,(int(self.rect.width*power/10),int(self.rect.height*power/10)))
		if self.direct==-1:
				self.image=pygame.transform.flip(self.image,True,False)
		self.image=self.image

	def move(self):
		if self.direct==1:
			self.rect.left += self.speed
		else:
			self.rect.left -= self.speed
	def action(self):
		self.move()
		self.imageCount+=1
		if self.rect.centerx<=0 or self.rect.centerx>=1200:
				self.scene.bullets.remove(self)
				return
	def collision(self):
		for i in range(len(self.scene.charList)):
			if pygame.sprite.collide_rect_ratio(1)(self,self.scene.charList[i]):
				if not self.scene.charList[i].rushing and self.scene.charList[i].charId!=self.createrId and self.damaged[i]>=1:
					self.damaged[i]=0
					self.scene.charList[i].hurt()
					self.scene.charList[i].hurtBool=1
					self.scene.charList[i].hurtDirect=self.direct
					self.scene.charList[i].hurtBackSpeed=self.power
		for w in self.scene.walls:
			if pygame.sprite.collide_rect_ratio(1)(self,w):
				self.scene.bullets.remove(self)