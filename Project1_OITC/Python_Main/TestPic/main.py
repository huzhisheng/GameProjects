import pygame
import pygame.sprite
import random
from pygame.locals import *
import pygame.font
import sys

class Model(pygame.sprite.Sprite):
	def __init__(self,scene):
		pygame.sprite.Sprite.__init__(self)
		self.walkImages = [pygame.image.load("walk0.png"),
						pygame.image.load("walk1.png"),
						pygame.image.load("walk2.png"),
						pygame.image.load("walk3.png"),
						pygame.image.load("walk4.png"),
						pygame.image.load("walk5.png"),
						pygame.image.load("walk6.png")]
		self.jumpImages=[pygame.image.load("jump0.png"),
						pygame.image.load("jump1.png")]
		self.attackImages=[pygame.image.load("attack0.png"),
						pygame.image.load("attack1.png"),
						pygame.image.load("attack2.png")]
		self.runImages=[pygame.image.load("run0.png"),
						pygame.image.load("run1.png"),
						pygame.image.load("run2.png"),
						pygame.image.load("run3.png"),
						pygame.image.load("run4.png"),
						pygame.image.load("run5.png")]
		self.rushImages=[pygame.image.load("rush0.png"),
						pygame.image.load("rush1.png"),
						pygame.image.load("rush2.png"),
						pygame.image.load("rush3.png"),
						pygame.image.load("rush4.png"),
						pygame.image.load("rush5.png")]
		self.hurtImages=[pygame.image.load("hurt0.png"),
						pygame.image.load("hurt1.png"),
						pygame.image.load("hurt2.png")]
		self.image=None
		self.scene=scene
		self.bullets = pygame.sprite.Group()
		self.rect=self.walkImages[0].get_rect()
		self.enemy=None
		self.speedX=5
		self.speedY=0
		self.aY=0.1
		self.movingRight=0 #1是走,2是跑,0则不动
		self.movingLeft=0
		self.dead=False
		self.rect[0] = 200
		self.rect[1] = 200
		self.onLand=False
		self.jumping=False
		self.direct=1 #-1向左,1向右
		#*******************动画计数专区*******************
		self.walkState=0
		self.runState=1
		self.jumpState=2
		self.attackState=3
		self.rushState=4
		self.hurtState=5
		self.standState=6
		self.imageState=self.standState
		self.stateFree=True
		#*******************
		self.imagenum=0
		self.walkCount=0
		self.runCount=0
		self.jumpCount=0
		self.attackCount=0
		self.rushCount=0
		self.hurtCount=0
		#*************************************************
	 # 发射子弹
	def attack(self):
		if self.stateFree==True:
			bullet = Bullet(self.rect.center)
			bullet.direct=self.direct
			if self.direct==-1:
				bullet.image=pygame.transform.flip(bullet.image,True,False)
			self.bullets.add(bullet)
			self.attackCount=0
			self.imageState=self.attackState
			self.stateFree=False

	def walkRight(self):
		self.movingRight=1
		if self.stateFree:
			self.imageState=self.walkState
	def walkLeft(self):
		self.movingLeft=1
		if self.stateFree:
			self.imageState=self.walkState
	def runRight(self):
		self.movingRight=2
		self.imageState=self.runState
	def runLeft(self):
		self.movingLeft=2
		self.imageState=self.runState
	def rush(self):
		self.rushCount=0
		self.stateFree=False
		self.imageState=self.rushState
	def hurt(self):
		self.hurtCount=0
		self.stateFree=False
		self.imageState=self.hurtState

	def jump(self):
		self.jumpCount=0
		self.imageState=self.jumpState
		self.jumping=True
		self.speedY=-6
	def loadEnemy(self,enemy):
		self.enemy=enemy
	def action(self):
		for bullet in self.bullets:
			bullet.move()
			if bullet.rect.centerx<=0 or bullet.rect.centerx>=1200:
				self.bullets.remove(bullet)
			if self.enemy:
				if pygame.sprite.pygame.sprite.collide_rect_ratio(1)(bullet,self.enemy):
					self.enemy.hurt()
					self.enemy.rect.move_ip(bullet.direct*bullet.power*60, 0)
					bullet.power=0
		if not self.dead:
			
			if self.imageState==self.runState:
				self.runCount+=1
				if self.runCount>=60:
					self.runCount=0
				self.image=self.runImages[self.runCount//10]
			elif self.imageState==self.jumpState:
				self.jumpCount+=1
				if self.jumpCount>=20:
					self.jumpCount=19
				self.image=self.jumpImages[self.jumpCount//10]
			elif self.imageState==self.attackState:
				self.attackCount+=1
				if self.attackCount>=30:
					self.stateFree=True
					self.imageState=self.standState
					self.attackCount=29
				self.image=self.attackImages[self.attackCount//10]
			elif self.imageState==self.rushState:
				self.rushCount+=1
				self.rect[0]+=self.direct*self.speedX
				if self.rushCount>=30:
					self.stateFree=True
					self.imageState=self.standState
					self.rushCount=29
				self.image=self.rushImages[self.rushCount//5]
			elif self.imageState==self.hurtState:
				self.hurtCount+=1
				if self.hurtCount>=15:
					self.hurtCount=14
					self.stateFree=True
					self.imageState=self.standState
				self.image=self.hurtImages[self.hurtCount//5]
			elif self.imageState==self.walkState:
				self.walkCount+=1
				if self.walkCount>=70:
					self.walkCount=0
				self.image=self.walkImages[self.walkCount//10]
			else:
				self.image=self.walkImages[0]

			if self.movingRight==1:
				self.direct=1
				if self.rect.right<1200:		 
					self.rect[0] +=  self.speedX
			if self.movingRight==2:
				self.direct=1
				if self.rect.right<1200:		 
					self.rect[0] +=  2*self.speedX
			if self.movingLeft==1:				
				self.direct=-1		
				if self.rect.left>0:		
					self.rect[0] -=  self.speedX
			if self.movingLeft==2:
				self.direct=-1
				if self.rect.right>0:		 
					self.rect[0] -=  2*self.speedX
			if self.onLand and not self.jumping :
				self.speedY=0
				#代码顺序很重要
			if self.rect.bottom<900:
				self.rect[1]+=self.speedY
			
			if not self.onLand:
				self.speedY+=self.aY
			if self.direct==-1:
				self.image=pygame.transform.flip(self.image,True,False)
	def draw(self):
		self.bullets.draw(self.scene)
		if not self.dead:
			self.scene.blit(self.image,self.rect)
	def AI(self):
		if self.enemy.rect.centerx<self.rect.centerx:
			self.direct=-1
		else:
			self.direct=1
		self.attack()
# NormalControl:


# Skill(object):
	
# setvoice
class Enemy(pygame.sprite.Sprite):
	def __init__(self,scene):
		pygame.sprite.Sprite.__init__(self)
# NormalControl:


# Skill(object):
	
# setvoice
class Land(pygame.sprite.Sprite):
	def __init__(self, initPos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("land.png")
		self.rect = self.image.get_rect()
		self.rect.center=initPos
		self.topRect=Rect(self.rect.left,self.rect.top,400,10)
		
class Collsion(object):
	def __init__(self):
		self.num=10
class Bullet(pygame.sprite.Sprite):
	def __init__(self, initPos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("bullet.png")
		self.rect = self.image.get_rect()
		self.rect.midtop = initPos
		self.speed = 20
		self.direct = 1
		self.power=1
	def move(self):
		if self.direct==1:
			self.rect.left += self.speed
		else:
			self.rect.left -= self.speed
			
class Scene(object):
	def __init__(self):
		pygame.init()
		pygame.mixer.init()	
		pygame.font.init()
		self.size = [1200, 900]
		self.scene = pygame.display.set_mode([self.size[0], self.size[1]])
		pygame.display.set_caption("输出全靠吼")
		self.bgImage = pygame.image.load("bgImage.png")
		self.scene.blit(self.bgImage,(0,0))
		self.clock = pygame.time.Clock()
		self.player=Model(self.scene)
		
		self.enemy=Model(self.scene)
		self.enemy.rect[0]=900
		self.enemy.rect[1]=100
		self.player.enemy=self.enemy
		self.enemy.enemy=self.player
		self.lands= pygame.sprite.Group()
		self.land1=Land((386,622))
		self.land2=Land((844,505))
		self.lands.add(self.land1)
		self.lands.add(self.land2)

		self.lastA=0
		self.lastD=0
	def drawHandle(self):
		self.scene.blit(self.bgImage,(0,0))
		self.player.draw()
		self.enemy.draw()
		self.lands.draw(self.scene)
		pygame.draw.rect(self.scene,(0,0,255),self.land1.topRect,1)

	def actionHandle(self):
		self.player.action()
		self.enemy.action()
		self.landCollision()

	def landCollision(self):
		self.player.onLand=False
		self.enemy.onLand=False
		for land in self.lands:
			if land.topRect.collidepoint(self.player.rect.midbottom) and self.player.speedY>=0:
				if self.player.imageState==self.player.jumpState :
					self.player.imageState=self.player.standState
				self.player.onLand=True
			if land.topRect.collidepoint(self.enemy.rect.midbottom) and self.enemy.speedY>=0:
				if self.enemy.imageState==self.enemy.jumpState :
					self.enemy.imageState=self.enemy.standState
				self.enemy.onLand=True	
		if not self.player.onLand:
			self.player.jumping=False
		if not self.enemy.onLand:
			self.enemy.jumping=False

	def eventHandle(self):
		self.enemy.AI()
		self.lastA+=1
		self.lastD+=1
		eventList = pygame.event.get()
		
		for event in eventList:
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

			if event.type == pygame.KEYDOWN:
				if event.key==pygame.K_d:
					if self.lastD>=20:
						self.player.walkRight()
					else:
						self.player.runRight()
					self.lastD=0
				if event.key==pygame.K_a:
					if self.lastA>=20:
						self.player.walkLeft()
					else:
						self.player.runLeft()
					self.lastA=0
				if event.key==pygame.K_j:
					self.player.attack()
				if event.key==pygame.K_k :
					self.player.jump()
				if event.key==pygame.K_LSHIFT:
					self.player.rush()

			if event.type == pygame.KEYUP:
				if event.key==pygame.K_d:
					self.player.movingRight=0
					self.player.imageState=self.player.standState
				if event.key==pygame.K_a:
					self.player.movingLeft=0
					self.player.imageState=self.player.standState

			if event.type==pygame.MOUSEBUTTONDOWN:
				mouseX,mouseY=pygame.mouse.get_pos()
				
	def collisionHandle(self):
		return
	def run(self):
		
		self.clock.tick(90)
		self.actionHandle()
		self.drawHandle()
		self.eventHandle()
		self.collisionHandle()
		pygame.display.update()
	
scene=Scene()

while True:
	scene.run()
