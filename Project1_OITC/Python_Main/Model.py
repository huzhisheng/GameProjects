import pygame
import pygame.sprite
import random
from pygame.locals import *
import pygame.font
from Bullet import Bullet
from Wall import Wall

root = '.'
root = root+'/'

class Model(pygame.sprite.Sprite):
	def __init__(self,scene,charId,x,y,charType,is_online):
		pygame.sprite.Sprite.__init__(self)
		self.walkImages = None
		self.jumpImages= None
		self.attackImages= None
		self.runImages= None
		self.rushImages= None
		self.hurtImages= None
		self.standImages=None
		self.charType=charType
		self.is_online = is_online

		self.scale=1.5

		if self.charType==1:
			self.p1Load()
		elif self.charType==2:
			self.p2Load()
		else:
			self.p3Load()
		self.boomImages=[pygame.image.load(root+"TestPic/boom0.png").convert_alpha(),
						pygame.image.load(root+"TestPic/boom1.png").convert_alpha(),
						pygame.image.load(root+"TestPic/boom2.png").convert_alpha(),
						pygame.image.load(root+"TestPic/boom3.png").convert_alpha(),
						pygame.image.load(root+"TestPic/boom4.png").convert_alpha()]
		self.boomSound=pygame.mixer.Sound(root+"TestPic/boom.wav")
		self.bubbleImages=[pygame.image.load(root+"TestPic/bubble0.png").convert_alpha(),
						pygame.image.load(root+"TestPic/bubble1.png").convert_alpha(),
						pygame.image.load(root+"TestPic/bubble2.png").convert_alpha(),
						pygame.image.load(root+"TestPic/bubble3.png").convert_alpha(),
						pygame.image.load(root+"TestPic/bubble4.png").convert_alpha(),
						pygame.image.load(root+"TestPic/bubble5.png").convert_alpha(),
						pygame.image.load(root+"TestPic/bubble6.png").convert_alpha(),
						pygame.image.load(root+"TestPic/bubble7.png").convert_alpha(),
						pygame.image.load(root+"TestPic/bubble8.png").convert_alpha(),
						pygame.image.load(root+"TestPic/bubble9.png").convert_alpha(),
						pygame.image.load(root+"TestPic/bubble10.png").convert_alpha(),
						pygame.image.load(root+"TestPic/bubble11.png").convert_alpha()]
		self.wingImage=pygame.image.load(root+"TestPic/wing.png").convert_alpha()
		self.shadowImage=pygame.image.load(root+"TestPic/shadow.png").convert_alpha()
		self.sheldImage=pygame.image.load(root+"TestPic/sheld.png").convert_alpha()
		#charId是每个角色的ID
		self.charId=charId
		self.image=self.walkImages[0]
		self.boomImage=self.boomImages[0]
		self.bubbleImage=self.bubbleImages[0]
		self.scene=scene
		
		rect=self.walkImages[0].get_rect()
		self.rect=Rect(0,0,int(rect.width/self.scale),int(rect.height/self.scale))

		self.shadowImage=pygame.transform.scale(self.shadowImage,(self.rect.width,self.rect.height))
		self.speedX=0
		self.speedY=0
		if self.scene.map_order == 10:
			self.aY = 0.05
		else:
			self.aY=0.1
		self.movingRight=0 #1是走,2是跑,0则不动
		self.movingLeft=0
		self.rect[0] = x
		self.rect[1] = y
		self.direct=1 #-1向左,1向右
		self.jumpTwice=2
		self.life=6
		#********************玩家角色名*******************
		self.playerName='null'
		self.font=pygame.font.SysFont('arial',30)
		self.playerNameFont=self.font.render(self.playerName,False,(0,0,255))

		#**********************状态栏*********************
		self.dead=False
		self.onLand=False
		self.jumping=False
		self.rushing=False
		self.flying=False
		self.leftWall=False
		self.rightWall=False
		self.hiding=False
		self.shelding=True
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

		self.boomState=False
		#*******************
		self.imagenum=0
		self.walkCount=0
		self.runCount=0
		self.jumpCount=0
		self.attackCount=0
		self.rushCount=0
		self.hurtCount=0
		self.boomCount=0
		#*************************************************
		#受到攻击后退的动作
		self.hurtTimeCount=20
		self.hurtBool=0
		self.hurtBackSpeed=0
		self.hurtDirect=0
		#按下s键角色下降一层的动作
		self.dropBool=False
		self.dropTimeCount=20
		#角色二段跳时脚底特效的动作
		self.bubbleBool=False
		self.bubbleCount=0
		#角色飞行时间计数
		self.flyTimeCount=300
		self.flyBool=False
		
		self.hideTimeCount=500
		self.sheldTimeCount=500
		
		#********************角色技能选择******************
		self.skillChosen=0

		self.wingChoice=2
		self.wallChoice=1
		self.hideChoice=0
		#****************网络数据包用到的属性***************
		self.attackTrigger=0
		self.walkRightTrigger=1
		self.walkLeftTrigger=2
		self.runRightTrigger=3
		self.runLeftTrigger=4
		self.rushTrigger=5
		self.hurtTrigger=6
		self.stopMovingRightTrigger=7
		self.stopMovingLeftTrigger=8
		self.jumpTrigger=9
		self.dropTrigger=10
		self.flyTrigger=11
		self.hideTrigger=12
		self.sheldTrigger=13
		#*******************图片大小调整********************
		for i in range(len(self.boomImages)):
			rect=self.boomImages[i].get_rect()
			self.boomImages[i]=pygame.transform.scale(self.boomImages[i],(int(rect.width/self.scale),int(rect.height/self.scale)))
		for i in range(len(self.bubbleImages)):
			rect=self.bubbleImages[i].get_rect()
			self.bubbleImages[i]=pygame.transform.scale(self.bubbleImages[i],(int(rect.width/self.scale),int(rect.height/self.scale)))
		rect=self.wingImage.get_rect()
		self.wingImage=pygame.transform.scale(self.wingImage,(int(rect.width/self.scale),int(rect.height/self.scale)))
		#rect=self.shadowImage.get_rect()
		#self.shadowImage=pygame.transform.scale(self.shadowImage,(int(rect.width/self.scale),int(rect.height/self.scale)))
		rect=self.sheldImage.get_rect()
		self.sheldImage=pygame.transform.scale(self.sheldImage,(int(rect.width/self.scale),int(rect.height/self.scale)))
		for i in range(len(self.walkImages)):
			rect=self.walkImages[i].get_rect()
			self.walkImages[i]=pygame.transform.scale(self.walkImages[i],(int(rect.width/self.scale),int(rect.height/self.scale)))
		for i in range(len(self.jumpImages)):
			rect=self.jumpImages[i].get_rect()
			self.jumpImages[i]=pygame.transform.scale(self.jumpImages[i],(int(rect.width/self.scale),int(rect.height/self.scale)))
		for i in range(len(self.attackImages)):
			rect=self.attackImages[i].get_rect()
			self.attackImages[i]=pygame.transform.scale(self.attackImages[i],(int(rect.width/self.scale),int(rect.height/self.scale)))
		for i in range(len(self.runImages)):
			rect=self.runImages[i].get_rect()
			self.runImages[i]=pygame.transform.scale(self.runImages[i],(int(rect.width/self.scale),int(rect.height/self.scale)))
		for i in range(len(self.rushImages)):
			rect=self.rushImages[i].get_rect()
			self.rushImages[i]=pygame.transform.scale(self.rushImages[i],(int(rect.width/self.scale),int(rect.height/self.scale)))
		for i in range(len(self.hurtImages)):
			rect=self.hurtImages[i].get_rect()
			self.hurtImages[i]=pygame.transform.scale(self.hurtImages[i],(int(rect.width/self.scale),int(rect.height/self.scale)))
		for i in range(len(self.standImages)):
			rect=self.standImages[i].get_rect()
			self.standImages[i]=pygame.transform.scale(self.standImages[i],(int(rect.width/self.scale),int(rect.height/self.scale)))
	def p1Load(self):
		self.walkImages = [pygame.image.load(root+"TestPic/p1_walk0.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p1_walk1.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p1_walk2.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p1_walk3.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p1_walk4.png").convert_alpha()]
		self.jumpImages=[pygame.image.load(root+"TestPic/p1_jump.png").convert_alpha()]
		self.attackImages=[pygame.image.load(root+"TestPic/p1_attack0.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p1_attack1.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p1_attack2.png").convert_alpha()]
		self.runImages=[pygame.image.load(root+"TestPic/p1_run0.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p1_run1.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p1_run2.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p1_run3.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p1_run4.png").convert_alpha()]
		self.rushImages=[pygame.image.load(root+"TestPic/p1_rush.png").convert_alpha()]
		self.hurtImages=[pygame.image.load(root+"TestPic/p1_hurt.png").convert_alpha()]
		self.standImages=[pygame.image.load(root+"TestPic/p1_stand.png").convert_alpha()]
	def p2Load(self):
		self.walkImages = [pygame.image.load(root+"TestPic/p2_walk0.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p2_walk1.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p2_walk2.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p2_walk3.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p2_walk4.png").convert_alpha()]
		self.jumpImages=[pygame.image.load(root+"TestPic/p2_jump.png").convert_alpha()]
		self.attackImages=[pygame.image.load(root+"TestPic/p2_attack0.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p2_attack1.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p2_attack2.png").convert_alpha()]
		self.runImages=[pygame.image.load(root+"TestPic/p2_run0.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p2_run1.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p2_run2.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p2_run3.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p2_run4.png").convert_alpha()]
		self.rushImages=[pygame.image.load(root+"TestPic/p2_rush.png").convert_alpha()]
		self.hurtImages=[pygame.image.load(root+"TestPic/p2_hurt.png").convert_alpha()]
		self.standImages=[pygame.image.load(root+"TestPic/p2_stand.png").convert_alpha()]
	def p3Load(self):
		self.walkImages = [pygame.image.load(root+"TestPic/p3_walk0.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p3_walk1.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p3_walk2.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p3_walk3.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p3_walk4.png").convert_alpha()]
		self.jumpImages=[pygame.image.load(root+"TestPic/p3_jump.png").convert_alpha()]
		self.attackImages=[pygame.image.load(root+"TestPic/p3_attack0.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p3_attack1.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p3_attack2.png").convert_alpha()]
		self.runImages=[pygame.image.load(root+"TestPic/p3_run0.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p3_run1.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p3_run2.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p3_run3.png").convert_alpha(),
						pygame.image.load(root+"TestPic/p3_run4.png").convert_alpha()]
		self.rushImages=[pygame.image.load(root+"TestPic/p3_rush.png").convert_alpha()]
		self.hurtImages=[pygame.image.load(root+"TestPic/p3_hurt.png").convert_alpha()]
		self.standImages=[pygame.image.load(root+"TestPic/p3_stand.png").convert_alpha()]
	# 发射子弹
	def attack(self):
		if self.stateFree==True:
			print("attack:",self.scene.voiceVolume,self.scene.maxVolume)
			power=int(self.scene.voiceVolume*20/self.scene.maxVolume)
			if power>20:
				power=20
			if self.charId!=self.scene.player.charId:
				power=10
			bullet = Bullet(self.scene,(self.rect.centerx,self.rect.centery-30),self.direct,power,self.charId)
			self.scene.bullets.add(bullet)
			self.attackCount=0
			self.imageState=self.attackState
			self.stateFree=False
			if self.is_online:
				if(bullet.direct==-1):
					self.scene.send_new_bullet(bullet.rect[0],bullet.rect[1],0,bullet.power,bullet.createrId)
				else:
					self.scene.send_new_bullet(bullet.rect[0],bullet.rect[1],bullet.direct,bullet.power,bullet.createrId)
				self.scene.send_role_animation(self.attackTrigger)

	def walkRight(self):
		self.movingRight=1
		#print(self.is_online)
		if self.stateFree:
			self.imageState=self.walkState
			if self.is_online:
				self.scene.send_role_animation(self.walkRightTrigger)
	def walkLeft(self):
		self.movingLeft=1
		if self.stateFree:
			self.imageState=self.walkState
			if self.is_online:
				self.scene.send_role_animation(self.walkLeftTrigger)
	def runRight(self):
		self.movingRight=2
		self.imageState=self.runState
		if self.is_online:
			self.scene.send_role_animation(self.runRightTrigger)
	def runLeft(self):
		self.movingLeft=2
		self.imageState=self.runState
		if self.is_online:
			self.scene.send_role_animation(self.runLeftTrigger)
	def rush(self):
		self.rushCount=0
		self.stateFree=False
		self.imageState=self.rushState
		if self.is_online:
			self.scene.send_role_animation(self.rushTrigger)
	def hurt(self):
		self.boomSound.play()
		self.hurtCount=0
		self.stateFree=False
		self.imageState=self.hurtState
		self.boomState=True
		self.boomCount=0
		if self.is_online:
			self.scene.send_role_animation(self.hurtTrigger)
	def stopMovingRight(self):
		self.movingRight=0
		self.imageState=self.standState
		if self.is_online:
			self.scene.send_role_animation(self.stopMovingRightTrigger)
	def stopMovingLeft(self):
		self.movingLeft=0
		self.imageState=self.standState
		if self.is_online:
			self.scene.send_role_animation(self.stopMovingLeftTrigger)
	def jump(self):
		if self.jumpTwice>0:
			if(self.jumpTwice==1):
				self.bubbleBool=True
				self.bubbleCount=0
			self.jumpTwice-=1
			self.jumpCount=0
			self.imageState=self.jumpState
			self.jumping=True
			self.speedY=-6
		if self.is_online:
			self.scene.send_role_animation(self.jumpTrigger)
	def drop(self):
		self.dropBool=True
		self.dropTimeCount=20
		if self.is_online:
			self.scene.send_role_animation(self.dropTrigger)
	def wing(self):
		self.flyBool=True
		self.flyTimeCount=300
		if self.is_online:
			self.scene.send_role_animation(self.flyTrigger)
	def fly(self):
		if self.flyBool:
			self.flying=True
	def stopFly(self):
		self.flying=False
	def wall(self):
		wall=Wall(self.scene,(self.rect.centerx+self.direct*50,self.rect[1]),self.direct)
		self.scene.walls.add(wall)
		if self.is_online:
			self.scene.send_role_animation(self.attackTrigger)
			if self.direct == -1:
				self.scene.send_new_wall(self.rect.centerx+self,direct*50,self.rect[1],0)
			else:
				self.scene.send_new_wall(self.rect.centerx+self,direct*50,self.rect[1],self.direct)

	def hide(self):
		self.hiding=True
		self.hideTimeCount=500
		if self.is_online:
			self.scene.send_role_animation(self.hideTrigger)

	def sheld(self):
		self.shelding=True
		self.sheldTimeCount=500
		if self.is_online:
			self.scene.send_role_animation(self.sheldTrigger)

	def skill(self):
		if self.skillChosen==self.wingChoice:
			self.wing()
		elif self.skillChosen==self.wallChoice:
			self.wall()
		elif self.skillChosen==self.hideChoice:
			self.hide()
	def reset(self):
		self.rect[0]=200
		self.rect[1]=200
		self.speedY=0
		self.shelding=True
		self.sheldTimeCount=500
	def action(self):
		if self.flyBool:
			self.flyTimeCount-=1
			if self.flyTimeCount<=0:
				self.flyBool=False
				self.flying=False
			if self.flying:
				self.speedY-=0.2
		if self.hiding:
			self.hideTimeCount-=1
			if self.hideTimeCount<=0:
				self.hiding=False
		if self.shelding:
			self.sheldTimeCount-=1
			if self.sheldTimeCount<=0:
				self.shelding=False
		if not self.dead:
			if self.rect[1]>=1200:
				self.life-=1
				self.reset()
			#每帧开始时speedX为0
			self.speedX=0
			#角色被击中后退
			if self.hurtBool:
				if self.shelding:
					self.speedX+=int(self.hurtDirect*self.hurtBackSpeed*0.3)
				else:
					self.speedX+=self.hurtDirect*self.hurtBackSpeed
				self.hurtTimeCount-=1
				if self.hurtTimeCount<=0:
					self.hurtBool=0
					self.hurtTimeCount=20
			if self.dropBool:
				self.dropTimeCount-=1
				if self.dropTimeCount<=0:
					self.dropBool=False
					self.dropTimeCount=20
			if self.onLand:
				self.jumpTwice=2
				
				
			if self.imageState==self.runState:
				self.stateFree=True
				self.runCount+=1
				if self.runCount>=50:
					self.runCount=0
				self.image=self.runImages[self.runCount//10]
			elif self.imageState==self.jumpState:
				self.stateFree=True
				self.jumpCount+=1
				if self.jumpCount>=20:
					self.jumpCount=19
				self.image=self.jumpImages[self.jumpCount//20]
			elif self.imageState==self.attackState:
				self.attackCount+=1
				if self.attackCount>=30:
					self.stateFree=True
					self.imageState=self.standState
					self.attackCount=29
				self.image=self.attackImages[self.attackCount//10]
			elif self.imageState==self.rushState:
				self.rushCount+=1
				self.speedX+=self.direct*5
				if self.rushCount>=30:
					self.stateFree=True
					self.imageState=self.standState
					self.rushCount=29
				self.image=self.rushImages[self.rushCount//30]
			elif self.imageState==self.hurtState:
				self.hurtCount+=1
				if self.hurtCount>=15:
					self.hurtCount=14
					self.stateFree=True
					self.imageState=self.standState
				self.image=self.hurtImages[self.hurtCount//15]
			elif self.imageState==self.walkState:
				self.stateFree=True
				self.walkCount+=1
				if self.walkCount>=50:
					self.walkCount=0
				self.image=self.walkImages[self.walkCount//10]
			else:
				self.stateFree=True
				self.image=self.standImages[0]

			if self.boomState:
				self.boomCount+=1
				if self.boomCount>=25:
					self.boomCount=24
					self.boomState=False
				self.boomImage=self.boomImages[self.boomCount//5]
			if self.bubbleBool:
				self.bubbleCount+=1
				if self.bubbleCount>=36:
					self.bubbleCount=35
					self.bubbleBool=False
				self.bubbleImage=self.bubbleImages[self.bubbleCount//3]
				
			if self.movingRight==1:
				self.direct=1
				if self.rect.right<1200:		 
					self.speedX+=2
			if self.movingRight==2:
				self.direct=1
				if self.rect.right<1200:		 
					self.speedX+=5
			if self.movingLeft==1:				
				self.direct=-1		
				if self.rect.left>0:		
					self.speedX-=2
			if self.movingLeft==2:
				self.direct=-1
				if self.rect.right>0:		 
					self.speedX-=5
			if self.onLand and not self.jumping and not self.flying:
				self.speedY=0
				#代码顺序很重要
			if self.leftWall:
				if self.speedX<0:
					self.speedX=0
			if self.rightWall:
				if self.speedX>0:
					self.speedX=0
			
			#函数不直接控制坐标值，只改变速度值speedX\speedY，每帧统一坐标值加相应速度值
			if self.is_online:
				if self.charId==self.scene.player.charId:
					self.rect[1]+=self.speedY
					self.rect[0]+=self.speedX
			else:
				self.rect[1]+=self.speedY
				self.rect[0]+=self.speedX

			if self.rect[1]<0:
				self.rect[1]=0
			if self.rect[0]<0:
				self.rect[0]=0
			if not self.onLand:
				self.speedY+=self.aY
			if self.direct==-1:
				self.image=pygame.transform.flip(self.image,True,False)
	def draw(self):
		if self.boomState:
			if self.direct==1:
				self.scene.scene.blit(self.boomImage,[self.rect.centerx,int(self.rect.centery-90/self.scale)])
			else:
				self.boomImage=pygame.transform.flip(self.boomImage,True,False)
				self.scene.scene.blit(self.boomImage,[int(self.rect.centerx-80/self.scale),int(self.rect.centery-90/self.scale)])
		if self.bubbleBool:
			self.scene.scene.blit(self.bubbleImage,[int(self.rect.centerx-150/self.scale),int(self.rect.centery-150/self.scale)])
		if not self.dead:
			if self.flyBool:
				self.scene.scene.blit(self.wingImage,(int(self.rect[0]-30/self.scale),self.rect[1]))
			if self.shelding:
				self.scene.scene.blit(self.sheldImage,(int(self.rect[0]-15/self.scale),self.rect[1]))
			self.playerNameFont=self.font.render(self.playerName,False,(0,0,255))
			
			if not self.hiding:
				self.scene.scene.blit(self.playerNameFont,(int(self.rect[0]+10/self.scale),int(self.rect[1]-30/self.scale)))
				self.scene.scene.blit(self.image,self.rect)
			if self.hiding:
				if self.charId==self.scene.player.charId:
					self.scene.scene.blit(self.playerNameFont,(int(self.rect[0]+10/self.scale),int(self.rect[1]-30/self.scale)))
					self.scene.scene.blit(self.image,self.rect)
					if not self.imageState==self.attackState and not self.imageState==self.hurtState:
						self.scene.scene.blit(self.shadowImage,(self.rect[0],self.rect[1]))
				elif self.imageState==self.attackState or self.imageState==self.hurtState:
					self.scene.scene.blit(self.playerNameFont,(int(self.rect[0]+10/self.scale),int(self.rect[1]-30/self.scale)))
					self.scene.scene.blit(self.image,self.rect)