import pygame
import pygame.sprite
import random
from pygame.locals import *
import pygame.font
import sys
import numpy
from base import Protocol
import socket
from threading import Thread
import threading
image_path = 'images/'
music_path = 'music/'
server_ip = '127.0.0.1'
server_port = 7777

class Model(pygame.sprite.Sprite):
	def __init__(self,scene,charId):
		pygame.sprite.Sprite.__init__(self)
		self.walkImages = [pygame.image.load(image_path + "walk0.png").convert_alpha(),
						pygame.image.load(image_path + "walk1.png").convert_alpha(),
						pygame.image.load(image_path + "walk2.png").convert_alpha(),
						pygame.image.load(image_path + "walk3.png").convert_alpha(),
						pygame.image.load(image_path + "walk4.png").convert_alpha()]
		self.runImages=[pygame.image.load(image_path + "run0.png").convert_alpha(),
						pygame.image.load(image_path + "run1.png").convert_alpha(),
						pygame.image.load(image_path + "run2.png").convert_alpha(),
						pygame.image.load(image_path + "run3.png").convert_alpha(),
						pygame.image.load(image_path + "run4.png").convert_alpha(),
						pygame.image.load(image_path + "run5.png").convert_alpha(),
						pygame.image.load(image_path + "run6.png").convert_alpha(),
						pygame.image.load(image_path + "run7.png").convert_alpha()]
		self.standImages=[pygame.image.load(image_path + "stand0.png").convert_alpha()]
		self.hurtImages=[pygame.image.load(image_path + "hurt0.png").convert_alpha()]
		self.jumpImages=[pygame.image.load(image_path + "jump0.png").convert_alpha()]
		self.boomImages=[pygame.image.load(image_path + "boom0.png").convert_alpha(),
						pygame.image.load(image_path + "boom1.png").convert_alpha(),
						pygame.image.load(image_path + "boom2.png").convert_alpha(),
						pygame.image.load(image_path + "boom3.png").convert_alpha(),
						pygame.image.load(image_path + "boom4.png").convert_alpha()]
		self.upImages=[pygame.image.load(image_path + "up0.png").convert_alpha(),
						pygame.image.load(image_path + "up1.png").convert_alpha(),
						pygame.image.load(image_path + "up2.png").convert_alpha(),
						pygame.image.load(image_path + "up3.png").convert_alpha()]
		self.rushCutImages=[pygame.image.load(image_path + "rushCut.png").convert_alpha()]
		self.boomSound=pygame.mixer.Sound(music_path + "boom.wav")
		self.image=self.standImages[0]
		self.boomImage=self.boomImages[0]
		self.upImage=self.upImages[0]
		self.scene=scene
		self.charId=charId
		self.rect=self.standImages[0].get_rect()
		self.bodyRect=Rect(0,0,60,130)
		self.speedX=5
		self.speedY=0
		self.aY=0.1
		self.movingRight=0 	#1是走,2是跑,0则不动
		self.movingLeft=0
		self.dead=False
		self.rect[0] = 200
		self.rect[1] = 200
		self.health=100		#血量

		self.onLand=False
		self.jumping=False
		self.jumpTwice=2
		self.direct=-1 #-1向左,1向右
		self.defendBool=False
		#剑的轨迹
		self.swordLights=pygame.sprite.Group()
		self.swordLightCount=0
		
		#********************玩家角色名*******************
		self.playerName=''
		self.font=pygame.font.SysFont('microsoft Yahei',30)
		self.playerNameFont=self.font.render(self.playerName,False,(0,0,255))
		#*******************动作手臂专区*******************
		self.mouseX=0
		self.mouseY=0
		self.oldMouseX=0
		self.oldMouseY=0

		self.deltaX=None
		self.deltaY=None
		self.deltaLength=None
		
		self.endX=0
		self.endY=0
		self.armVector=pygame.Vector2(0,0)
		self.newArmVecor=pygame.Vector2(0,0)
		self.armAngle=0
		self.arm=pygame.image.load(image_path + "arm.png").convert_alpha()
		self.armRect=self.arm.get_rect()
		self.newArm=self.arm
		self.newArmRect=self.armRect
		
		self.swordDeltaX=0
		self.swordDeltaY=0
		self.swordVector=pygame.Vector2(0,0)
		self.swordAngle=0
		self.sword=pygame.image.load(image_path + "sword0.png").convert_alpha()
		self.swordRect=self.sword.get_rect()
		self.newSword=self.sword
		self.newSwordRect=self.swordRect
		
		self.hurtX=0
		self.hurtY=0
		
		self.swordPointX=0
		self.swordPointY=0
		self.oldSwordPointX=0
		self.oldSwordPointY=0
		self.cutDirect=0#1代表下，0代表上
		self.cutPower=0
		#*******************动画计数专区*******************
		self.walkState=0
		self.runState=1
		self.jumpState=2
		self.hurtState=3
		self.standState=4
		self.imageState=self.standState
		self.stateFree=True
		self.boomState=False
		#*******************
		self.imagenum=0
		self.walkCount=0
		self.runCount=0
		self.jumpCount=0
		self.hurtCount=0

		self.boomCount=0
		#*************************************************
		self.hurtBool=False
		self.hurtRushBool=False
		self.hurtTimeCount=20
		self.hurtDirect=0

		self.upBool=False
		self.upTimeCount=0
		self.upCutX=0
		self.upCutY=0

		self.downBool=False
		self.downTimeCount=0

		self.rushCutBool=False
		self.rushCutTimeCount=0
		self.hurtRect=None
		#****************网络数据包用到的属性***************
		self.cutTrigger=0
		self.walkRightTrigger=1
		self.walkLeftTrigger=2
		self.runRightTrigger=3
		self.runLeftTrigger=4
		self.hurtTrigger=5
		self.stopMovingRightTrigger=6
		self.stopMovingLeftTrigger=7
		self.jumpTrigger=8
		
		#************************************************
		#*******************鼠标技能专区*******************
		self.leftFlag=False
		self.rightFlag=False
		self.upFlag=False
		self.downFlag=False
		self.lastCutCount=0
	def reset(self):
		self.rect[0]=200
		self.rect[1]=200
		self.health=100
		self.speedX=0
		self.speedY=0
	def getAngle(self,a, b, c):#a是mouse b是arm c是sword
		a2=a*a
		b2=b*b
		c2=c*c
		cos_M = (b2+a2-c2) / (2 * a*b)
		angleAMB = numpy.arccos(cos_M)/numpy.pi * 180
		#print(angleAMB)
		return angleAMB
	def cut(self):
		if self.upBool or self.downBool:
			self.hurtRect=Rect(0,0,100,332)
			self.hurtRect.centerx=self.upCutX
			self.hurtRect.centery=self.upCutY+50
			
		for r in self.scene.charList:
			if r.charId!=self.charId:
				if r.bodyRect.collidepoint(self.hurtX,self.hurtY) or r.bodyRect.collidepoint(self.hurtX,self.rect.centery) or r.bodyRect.collidepoint(self.swordPointX,self.rect.centery) or r.bodyRect.collidepoint(self.swordPointX,self.swordPointY):
					if r.defendBool:
						self.boomSound.play()
						r.boomState=True
						r.boomCount=0
					else:
						r.health-=1
						r.hurt()
						r.hurtDirect=self.cutDirect
				if self.upBool or self.downBool:
					if self.hurtRect.collidepoint(r.rect.centerx,r.rect.centery):
						r.hurtRushBool=True
	
	def upCut(self):
		self.upBool=True
		self.upTimeCount=0
		self.upCutX=self.hurtX
		self.upCutY=self.hurtY
	def downCut(self):
		self.downBool=True
		self.downTimeCount=0
		self.upCutX=self.hurtX
		self.upCutY=self.hurtY
	def rushCut(self):
		for r in self.scene.charList:
			if r.charId!=self.charId:
				if r.bodyRect.collidepoint(self.hurtX,self.hurtY) or r.bodyRect.collidepoint(self.swordPointX,self.swordPointY) or r.bodyRect.collidepoint(self.endX,self.endY):
					if r.defendBool:
						self.boomSound.play()
						r.boomState=True
						r.boomCount=0
					else:
						r.health-=1
						r.hurt()
						r.hurtDirect=self.cutDirect
	def leftRushCut(self):
		self.direct=-1
		self.rushCutBool=True
		self.rushCutTimeCount=0
	def rightRushCut(self):
		self.direct=1
		self.rushCutBool=True
		self.rushCutTimeCount=0
	def rushCutPose(self):
		self.newArmVector=pygame.Vector2(self.direct,0)	
		self.newArmVector.scale_to_length(40)
		self.endX=self.newArmVector.x+self.rect.centerx
		self.endY=self.newArmVector.y+self.rect.centery-30
		self.armAngle=-self.armVector.angle_to(self.newArmVector)
		self.newArm=pygame.transform.rotate(self.arm,self.armAngle)
		self.newArmRect=self.newArm.get_rect()
		self.newArmRect.center=(self.rect.centerx,self.rect.centery-30)
		self.newSword=self.sword
		if self.direct==-1:
			self.newSword=pygame.transform.flip(self.newSword,True,False)
		self.newSwordRect=self.newSword.get_rect()
		self.newSwordRect.center=(self.endX,self.endY)
	def crossCut(self):
		direct=1
		if self.hurtX<self.rect.centerx:
			direct=-1
		crosscut=crossCutLight(self.scene,self,direct,(self.rect.centerx,self.rect.centery-60))
		self.scene.crossCutLights.add(crosscut)
	def walkRight(self):
		self.movingRight=1
		if self.stateFree:
			self.imageState=self.walkState
		self.scene.send_role_animation(self.walkRightTrigger)
	def walkLeft(self):
		self.movingLeft=1
		if self.stateFree:
			self.imageState=self.walkState
		self.scene.send_role_animation(self.walkLeftTrigger)
	def runRight(self):
		self.movingRight=2
		self.imageState=self.runState
		self.scene.send_role_animation(self.runRightTrigger)
	def runLeft(self):
		self.movingLeft=2
		self.imageState=self.runState
		self.scene.send_role_animation(self.runLeftTrigger)
	def stopMovingRight(self):
		self.movingRight=0
		self.imageState=self.standState
		self.scene.send_role_animation(self.stopMovingRightTrigger)
	def stopMovingLeft(self):
		self.movingLeft=0
		self.imageState=self.standState
		self.scene.send_role_animation(self.stopMovingLeftTrigger)
	def hurt(self):
		#self.boomSound.play()
		self.hurtCount=0
		self.stateFree=False
		self.imageState=self.hurtState
		self.hurtBool=True
		#self.boomState=True
		#self.boomCount=0

	def jump(self):
		if self.jumpTwice>0:
			self.jumpTwice-=1
			self.jumpCount=0
			self.imageState=self.jumpState
			self.jumping=True
			self.speedY=-7
			self.scene.send_role_animation(self.jumpTrigger)

	def cutFlagReset(self):
		self.leftFlag=False
		self.rightFlag=False
		self.upFlag=False
		self.downFlag=False
	def action(self):
		
		self.lastCutCount+=1
		v=pygame.Vector2(self.mouseX-self.oldMouseX,self.mouseY-self.oldMouseY)
		if self.mouseX<200 and v.x<0:
			self.leftFlag=True
			self.lastCutCount=0
		if self.mouseX>1000 and v.x>0:
			self.rightFlag=True
			self.lastCutCount=0
		if self.mouseY<100 and v.y<0:
			self.upFlag=True
			self.lastCutCount=0
		if self.mouseY>800 and v.y>0:
			self.downFlag=True
			self.lastCutCount=0
		if self.lastCutCount>=40:
			self.cutFlagReset()
		
		if v.x>600:
			self.rightRushCut()
			self.cutFlagReset()
		if v.x<-600:
			self.leftRushCut()
			self.cutFlagReset()
		if v.y>400:
			self.downCut()
			self.cutFlagReset()
		if v.y<-400:
			self.upCut()
			self.cutFlagReset()
		if self.leftFlag and self.rightFlag and self.upFlag and self.downFlag:
			self.crossCut()
			self.cutFlagReset()
		#print(self.upFlag,self.downFlag,self.leftFlag,self.rightFlag)
		if v.y>0:
			self.cutDirect=1
		else:
			self.cutDirect=-1
			
		self.swordLights.update()

		self.defendBool=False
		#******************是否在防御**********************
		if self.bodyRect.collidepoint(self.hurtX,self.hurtY):
			self.defendBool=True

		
		#*************************************************
		self.bodyRect.center=self.rect.center
		#******************手臂挥舞************************
		self.deltaX=self.mouseX-self.rect.centerx
		self.deltaY=self.mouseY-self.rect.centery+30
		
		mouseVector=pygame.Vector2(self.deltaX,self.deltaY)
		armLength=40
		swordLength=100
		
		if mouseVector.length()>140:
			self.newArmVector=pygame.Vector2(self.deltaX,self.deltaY)	
			self.newArmVector.scale_to_length(40)
			self.endX=self.newArmVector.x+self.rect.centerx
			self.endY=self.newArmVector.y+self.rect.centery-30
			self.armAngle=-self.armVector.angle_to(self.newArmVector)
			self.newArm=pygame.transform.rotate(self.arm,self.armAngle)
			self.newArmRect=self.newArm.get_rect()
			self.newArmRect.center=(self.rect.centerx,self.rect.centery-30)
		elif mouseVector.length()>65:
			mouseLength=mouseVector.length()
			aAngle=self.getAngle(mouseLength,armLength,swordLength)
			mouseAngle=self.armVector.angle_to(mouseVector)
			#print(mouseAngle)
			self.armAngle=aAngle+mouseAngle

			self.newArmVector=pygame.Vector2(1,0)
			self.newArmVector.rotate_ip(self.armAngle)
			#print(armVector.x,armVector.y)
			self.newArmVector.scale_to_length(40)
			self.endX=self.newArmVector.x+self.rect.centerx
			self.endY=self.newArmVector.y+self.rect.centery-30
			self.newArm=pygame.transform.rotate(self.arm,-self.armAngle)
			self.newArmRect=self.newArm.get_rect()
			self.newArmRect.center=(self.rect.centerx,self.rect.centery-30)
		else:
			self.endX=self.newArmVector.x+self.rect.centerx
			self.endY=self.newArmVector.y+self.rect.centery-30
			self.newArmRect.center=(self.rect.centerx,self.rect.centery-30)
		self.swordDeltaX=self.mouseX-self.endX
		self.swordDeltaY=self.mouseY-self.endY
		swordVector=pygame.Vector2(self.swordDeltaX,self.swordDeltaY)
		if swordVector.length==0:
			swordVector.x=1
			swordVector.y=1
		swordVector.scale_to_length(100)
		self.swordAngle=-self.swordVector.angle_to(swordVector)

		self.newSword=pygame.transform.rotate(self.sword,self.swordAngle)#self.swordAngle)
		self.newSwordRect=self.newSword.get_rect()
		self.newSwordRect.center=(self.endX,self.endY)
		#添加剑的幻影
		self.swordLightCount+=1
		if self.swordLightCount>=3:
			self.swordLightCount=0
			newSwordLight=SwordLight(self,self.swordAngle,self.newSwordRect.center)
			self.swordLights.add(newSwordLight)

		self.hurtX=int(self.endX+swordVector.x/1.5)
		self.hurtY=int(self.endY+swordVector.y/1.5)
		self.oldSwordPointX=self.swordPointX
		self.oldSwordPointY=self.swordPointY
		self.swordPointX=int(self.endX+swordVector.x/1)
		self.swordPointY=int(self.endY+swordVector.y/1)
		v=pygame.Vector2(self.swordPointX-self.oldSwordPointX,self.swordPointY-self.oldSwordPointY)
		self.cutPower=int(v.length())
		
		if not self.dead:
			
			if self.cutPower>80:
				self.cut()
			if self.speedY>5 and self.hurtY>self.rect.centery:
				self.cut()
			#每帧开始时speedX为0
			self.speedX=0
			#被击中时的抖动
			if self.hurtBool:
				self.hurtBool=False
				if self.hurtDirect==-1:
					self.rect[1]+=self.hurtDirect*5
				#self.hurtTimeCount-=1
				#if self.hurtTimeCount<=0:
				elif not self.onLand:
					self.rect[1]+=self.hurtDirect*5
			if self.hurtRushBool:
				self.speedY+=self.hurtDirect*7
				self.jumping=True
				self.hurtRushBool=False
					#self.hurtTimeCount=20
			if self.imageState==self.runState:
				self.runCount+=1
				if self.runCount>=24:
					self.runCount=0
				self.image=self.runImages[self.runCount//3]
			elif self.imageState==self.jumpState:
				self.jumpCount+=1
				if self.jumpCount>=20:
					self.jumpCount=19
				self.image=self.jumpImages[self.jumpCount//20]
	
			
			elif self.imageState==self.hurtState:
				self.hurtCount+=1
				if self.hurtCount>=15:
					self.hurtCount=14
					self.stateFree=True
					self.imageState=self.standState
				self.image=self.hurtImages[self.hurtCount//15]
			elif self.imageState==self.walkState:
				self.walkCount+=1
				if self.walkCount>=20:
					self.walkCount=0
				self.image=self.walkImages[self.walkCount//4]
			else:
				self.image=self.standImages[0]
			if self.boomState:
				self.boomCount+=1
				if self.boomCount>=25:
					self.boomCount=24
					self.boomState=False
				self.boomImage=self.boomImages[self.boomCount//5]
			if self.upBool:
				self.upTimeCount+=1
				if self.upTimeCount>=20:
					self.upTimeCount=19
					self.upBool=False
				self.upImage=self.upImages[self.upTimeCount//5]
			if self.downBool:
				self.downTimeCount+=1
				if self.downTimeCount>=20:
					self.downTimeCount=19
					self.downBool=False
				self.upImage=self.upImages[self.downTimeCount//5]
				self.upImage=pygame.transform.flip(self.upImage,False,True)
			if self.rushCutBool:
				self.rushCutTimeCount+=1
				self.speedX+=20*self.direct
				if self.rushCutTimeCount>=20:
					self.rushCutBool=False
				self.image=self.rushCutImages[0]
				self.rushCut()
				self.rushCutPose()
			if self.onLand:
				self.jumpTwice=2
				
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
			if self.onLand and not self.jumping :
				self.speedY=0
			if self.speedY<-15:#垂直速度阈值
				self.speedY=-8
				#代码顺序很重要
			#函数不直接控制坐标值，只改变速度值speedX\speedY，每帧统一坐标值加相应速度值
			if self.scene.player.charId==self.charId:
				self.rect[1]+=self.speedY
				self.rect[0]+=self.speedX
			if self.rect[0]<0:
				self.rect[0]=0
			if self.rect[1]<0:
				self.speedY=0
				self.rect[1]=0
			if self.rect.centerx>1200:
				self.rect.centerx=1000
			if self.rect.centery>890:
				self.rect.centery=600
			if self.health<=0:
				self.health=0
			if not self.onLand:
				self.speedY+=self.aY
			if self.direct==-1:
				self.image=pygame.transform.flip(self.image,True,False)
		
	def draw(self):
		self.playerNameFont=self.font.render(self.playerName,False,(0,0,0))
		self.swordLights.draw(self.scene.scene)
		if self.boomState:
			if self.direct==1:
				self.scene.scene.blit(self.boomImage,[self.rect.centerx,self.rect.centery-90])
			else:
				self.boomImage=pygame.transform.flip(self.boomImage,True,False)
				self.scene.scene.blit(self.boomImage,[self.rect.centerx-100,self.rect.centery-90])
		
		if self.upBool or self.downBool:
				self.scene.scene.blit(self.upImage,[self.upCutX,self.upCutY-90])
				#pygame.draw.rect(self.scene.scene,(0,0,255),self.hurtRect,1)
		if not self.dead:
			self.scene.scene.blit(self.playerNameFont,(self.rect[0]+10,self.rect[1]-30))
			self.scene.scene.blit(self.newSword,self.newSwordRect)
			self.scene.scene.blit(self.newArm,self.newArmRect)
			self.scene.scene.blit(self.image,self.rect)
class SwordLight(pygame.sprite.Sprite):
	def __init__(self,player,angle,initPos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image_path + "sword1.png").convert_alpha()
		self.image = pygame.transform.rotate(self.image,angle)
		self.rect=self.image.get_rect()
		self.rect.center=initPos
		self.player=player
		self.timeCount=60
	def update(self):
		self.timeCount-=1
		if self.timeCount==0:
			self.player.swordLights.remove(self)
class crossCutLight(pygame.sprite.Sprite):
	def __init__(self,scene,player,direct,initPos):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load(image_path + "crossCut.png").convert_alpha()
		self.rect=self.image.get_rect()
		self.rect.center=initPos
		self.direct=direct
		self.player=player
		self.scene=scene
		self.timeCount=0
		if self.direct==-1:
			self.image=pygame.transform.flip(self.image,True,False)
	def update(self):
		self.timeCount+=1
		if self.timeCount>60:
			self.scene.crossCutLights.remove(self)
		self.rect.centerx+=self.direct*10
		for r in scene.charList:
			if pygame.sprite.collide_rect_ratio(1)(self,r) and self.player.charId!=r.charId:
				r.hurt()
class Rain(pygame.sprite.Sprite):
	def __init__(self,scene,initPos):
		pygame.sprite.Sprite.__init__(self)
		self.scene=scene
		self.vector1=pygame.Vector2(0,-1)
		self.vector2=pygame.Vector2(-1,-10).normalize()
		self.vector3=pygame.Vector2(2,10)
		self.vector3.scale_to_length(10)
		self.angle=self.vector1.angle_to(self.vector2)
		self.image=pygame.image.load(image_path + "rain.png").convert_alpha()
		self.image=pygame.transform.rotate(self.image,-self.angle)
		self.rect=self.image.get_rect()
		self.rect.center=initPos
	def update(self):
		self.rect[0]+=self.vector3.x
		self.rect[1]+=self.vector3.y
		if self.rect[1]>788:
			self.scene.rains.remove(self)
class Scene(object):
	def __init__(self):
		pygame.init()
		pygame.mixer.init()	
		pygame.font.init()
		#self.swordLights=pygame.sprite.Group()
		self.size = [1200, 900]
		self.scene = pygame.display.set_mode([self.size[0], self.size[1]])
		pygame.display.set_caption("影")
		self.normalBgImage = pygame.image.load(image_path + "inkBg3.png").convert()
		self.thunderBgImage=pygame.image.load(image_path + "inkBg4.png").convert()
		self.bgImage=self.normalBgImage
		self.pauseImage=pygame.image.load(image_path + "pauseImage.png").convert()
		self.loseImage=pygame.image.load(image_path + "loseImage.png").convert()
		self.rains=pygame.sprite.Group()
		self.scene.blit(self.bgImage,(0,0))
		self.clock = pygame.time.Clock()
		self.player=None
		self.landRect=Rect(0,788,1200,112)
		self.charList=[]
		self.lastA=0
		self.lastD=0
		pygame.mixer.music.load(music_path + "rain.wav")
		self.thunderWav=pygame.mixer.Sound(music_path + "thunder.wav")
		self.crossCutLights=pygame.sprite.Group()

		self.bloodImage=pygame.image.load(image_path + "blood.png").convert_alpha()
		self.bloodImageRect=self.bloodImage.get_rect()
		
		#*************************************************
		self.g_client = socket.socket()
		self.IP = server_ip
		self.ADDRESS = (self.IP,server_port)
		#****************网络数据包用到的属性*****************
		self.netPlayerMove=0
		self.netPlayerNew=1
		self.netPlayerOff=2
		self.netArmSwordNew=3
		self.netAnimationNew=4
		#*************************************************
		self.breakFlag=False
		self.playerName=''
		self.mouseX=0
		self.mouseY=0

		self.rainCount=0
		self.thunderCount=200
		self.thunderTimeCount=0
		self.thunderBool=False
	def thunder(self):
		self.bgImage=self.thunderBgImage
		self.thunderBool=True
		self.thunderTimeCount=0
	def createRain(self):
		
		x=random.randint(-100,1200)
		y=0
		rain=Rain(self,(x,y))
		self.rains.add(rain)
	def charTrigger(self,trigger,charId):
		for r in self.charList:
			if r.charId == charId:
				if trigger==0:
					pass
				elif trigger==1:
					if r.stateFree:
						r.imageState=r.walkState
					r.direct=1
				elif trigger==2:
					if r.stateFree:
						r.imageState=r.walkState
					r.direct=-1
				elif trigger==3:
					r.imageState=r.runState
					r.direct=1
				elif trigger==4:
					r.imageState=r.runState
					r.direct=-1
				elif trigger==5:
					pass
				elif trigger==6:
					r.movingRight=0
					r.imageState=r.standState
				elif trigger==7:
					r.movingLeft=0
					r.imageState=r.standState
				elif trigger==8:
					r.jumpCount=0
					r.imageState=r.jumpState
					r.jumping=True
	def drawHandle(self):
		bloodWidth=int(self.player.health*self.bloodImageRect.width/100)
		newRect=Rect(0,0,bloodWidth,self.bloodImageRect.height)
		newBlood=self.bloodImage.subsurface(newRect).copy()
		
		self.scene.blit(self.bgImage,(0,0))
		if self.thunderBool:
			self.thunderTimeCount+=1
			if self.thunderTimeCount==12:
				self.bgImage=self.normalBgImage
				self.thunderBool=False
		
		self.scene.blit(newBlood,newRect)
		for r in self.charList:
			r.draw()

		self.crossCutLights.draw(self.scene)
		self.rains.draw(self.scene)
	def actionHandle(self):
		if self.player.health<=0:
			self.playerLose()	
		#雨
		self.rainCount+=1
		if self.rainCount==2:
			self.rainCount=0
			self.createRain()
		#雷
		self.thunderCount-=1
		if self.thunderCount==0:
			self.thunder()
			self.thunderWav.play()
			self.thunderCount=random.randint(400,800)
		self.rains.update()
		self.crossCutLights.update()
		for r in self.charList:
			r.action()	
	def landCollision(self):
		for r in self.charList:
			r.onLand=False
		for r in self.charList:
			if self.landRect.collidepoint(r.rect.midbottom) and r.speedY>=0:
				if r.imageState==r.jumpState :
					r.imageState=r.standState
				r.onLand=True
		for r in self.charList:
			if not r.onLand:
				r.jumping=False
	def eventHandle(self):
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
				if event.key==pygame.K_w :
					self.player.jump()
				if event.key==pygame.K_ESCAPE:
					self.pause() 

			if event.type == pygame.KEYUP:
				if event.key==pygame.K_d:
					self.player.stopMovingRight()
					
				if event.key==pygame.K_a:
					self.player.stopMovingLeft()
					
			if event.type==pygame.MOUSEBUTTONDOWN:
				mouseX,mouseY=pygame.mouse.get_pos()
				
	def collisionHandle(self):
		self.landCollision()
	def run(self):
		
		self.mouseX,self.mouseY=pygame.mouse.get_pos()
		self.player.oldMouseX=self.player.mouseX
		self.player.oldMouseY=self.player.mouseY
		self.player.mouseX=self.mouseX
		self.player.mouseY=self.mouseY
		self.send_new_mouse()
		self.collisionHandle()
		self.actionHandle()
		self.drawHandle()
		self.eventHandle()
		self.send_role_move()
		#print(self.player.defendBool)
		pygame.display.update()
		self.clock.tick(60)

	#*********************网络模块*********************
	def send_role_move(self):

		#发送角色的坐标给服务端

		# 构建数据包
		p = Protocol()
		p.add_int32(0)
		x=self.player.rect[0]
		y=self.player.rect[1]
		if x<0:
			x=0
		if y<=0:
			y=0
		p.add_int32(x)
		p.add_int32(y)
		data = p.get_pck_has_head()
		# 发送数据包
		self.g_client.sendall(data)
	def send_role_animation(self,trigger):
		#发送角色的动画状态给服务端

		# 构建数据包
		p = Protocol()
		p.add_int32(4)
		p.add_int32(trigger)
		p.add_int32(self.player.charId)
		data = p.get_pck_has_head()
		# 发送数据包
		self.g_client.sendall(data)
	def send_new_role(self):

		#告诉服务端有新玩家加入

		# 构建数据包
		p = Protocol()
		p.add_int32(1)
		p.add_str(self.playerName)
		p.add_int32(self.player.rect[0])
		p.add_int32(self.player.rect[1])
		p.add_int32(self.player.charId)
		data = p.get_pck_has_head()
		# 发送数据包
		self.g_client.sendall(data)
	def send_new_mouse(self):
		#发送角色的鼠标的位置
		
		# 构建数据包
		p = Protocol()
		p.add_int32(3)
		p.add_int32(self.player.mouseX)
		p.add_int32(self.player.mouseY)
		p.add_int32(self.player.charId)
		data = p.get_pck_has_head()
		# 发送数据包
		self.g_client.sendall(data)
	def pck_handler(self,pck):
		p = Protocol(pck)
		pck_type = p.get_int32()

		if pck_type == self.netPlayerMove:  # 玩家移动的数据包
			x = p.get_int32()
			y = p.get_int32()
			charId = p.get_int32()
			for r in self.charList:
				if r.charId == charId:
					r.rect[0] = x
					r.rect[1] = y
					break
		elif pck_type == self.netPlayerNew:  # 新玩家数据包
			playerName=p.get_str()
			x = p.get_int32()
			y = p.get_int32()
			charId = p.get_int32()
			r = Model(self,charId)
			r.playerName=playerName
			self.charList.append(r)
		elif pck_type == self.netPlayerOff:  # 玩家掉线
			charId = p.get_int32()
			for r in self.charList:
				if r.charId == charId:
					self.charList.remove(r)
					break
		elif pck_type == self.netArmSwordNew:# 手臂和剑状态更新
			
			
			mouseX=p.get_int32()
			mouseY=p.get_int32()
			charId=p.get_int32()
			for r in self.charList:
				if r.charId == charId:
					r.oldMouseX=r.mouseX
					r.oldMouseY=r.mouseY
					r.mouseX=mouseX
					r.mouseY=mouseY
					#break		
		elif pck_type == self.netAnimationNew:
			trigger=p.get_int32()
			charId=p.get_int32()
			self.charTrigger(trigger,charId)
		else:
			return
	
	def msg_handler(self):

		#处理服务端返回的消息

		while True:
			bytes = self.g_client.recv(1024)
			# 以包长度切割封包
			while True:
				# 读取包长度
				length_pck = int.from_bytes(bytes[:4], byteorder='little')
				# 截取封包
				pck = bytes[4:4 + length_pck]
				# 删除已经读取的字节
				bytes = bytes[4 + length_pck:]
				# 把封包交给处理函数
				self.pck_handler(pck)
				# 如果bytes没数据了，就跳出循环
				if len(bytes) == 0:
					break
	def net_init(self):
		# 与服务器建立连接
		self.g_client.connect(self.ADDRESS)
		# 开始接受服务端消息
		thead = Thread(target=self.msg_handler)
		thead.setDaemon(True)
		thead.start()
		# 告诉服务端有新玩家
		self.player_enter()
		self.player=Model(self,random.randint(0,1000))
		self.charList.append(self.player)
		self.player.playerName=self.playerName
		self.send_new_role()
		pygame.mixer.music.play(-1,0)
	def enter_input_handle(self):
		eventList = pygame.event.get()
		
		for event in eventList:
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

			if event.type == pygame.KEYDOWN:
				if event.key==pygame.K_0:
					self.playerName=self.playerName+'0'
				elif event.key==pygame.K_1:
					self.playerName=self.playerName+'1'
				elif event.key==pygame.K_2:
					self.playerName=self.playerName+'2'
				elif event.key==pygame.K_3:
					self.playerName=self.playerName+'3'
				elif event.key==pygame.K_4:
					self.playerName=self.playerName+'4'
				elif event.key==pygame.K_5:
					self.playerName=self.playerName+'5'
				elif event.key==pygame.K_6:
					self.playerName=self.playerName+'6'
				elif event.key==pygame.K_7:
					self.playerName=self.playerName+'7'
				elif event.key==pygame.K_8:
					self.playerName=self.playerName+'8'
				elif event.key==pygame.K_9:
					self.playerName=self.playerName+'9'
				elif event.key==pygame.K_a:
					self.playerName=self.playerName+'A'
				elif event.key==pygame.K_b:
					self.playerName=self.playerName+'B'
				elif event.key==pygame.K_c:
					self.playerName=self.playerName+'C'
				elif event.key==pygame.K_d:
					self.playerName=self.playerName+'D'
				elif event.key==pygame.K_e:
					self.playerName=self.playerName+'E'
				elif event.key==pygame.K_f:
					self.playerName=self.playerName+'F'
				elif event.key==pygame.K_g:
					self.playerName=self.playerName+'G'
				elif event.key==pygame.K_h:
					self.playerName=self.playerName+'H'
				elif event.key==pygame.K_i:
					self.playerName=self.playerName+'I'
				elif event.key==pygame.K_j:
					self.playerName=self.playerName+'J'
				elif event.key==pygame.K_k:
					self.playerName=self.playerName+'K'
				elif event.key==pygame.K_l:
					self.playerName=self.playerName+'L'
				elif event.key==pygame.K_m:
					self.playerName=self.playerName+'M'
				elif event.key==pygame.K_n:
					self.playerName=self.playerName+'N'
				elif event.key==pygame.K_o:
					self.playerName=self.playerName+'O'
				elif event.key==pygame.K_p:
					self.playerName=self.playerName+'P'
				elif event.key==pygame.K_q:
					self.playerName=self.playerName+'Q'
				elif event.key==pygame.K_r:
					self.playerName=self.playerName+'R'
				elif event.key==pygame.K_s:
					self.playerName=self.playerName+'S'
				elif event.key==pygame.K_t:
					self.playerName=self.playerName+'T'
				elif event.key==pygame.K_u:
					self.playerName=self.playerName+'U'
				elif event.key==pygame.K_v:
					self.playerName=self.playerName+'V'
				elif event.key==pygame.K_w:
					self.playerName=self.playerName+'W'
				elif event.key==pygame.K_x:
					self.playerName=self.playerName+'X'
				elif event.key==pygame.K_y:
					self.playerName=self.playerName+'Y'
				elif event.key==pygame.K_z:
					self.playerName=self.playerName+'Z'
			if event.type==pygame.MOUSEBUTTONDOWN:
				self.mouseX,self.mouseY=pygame.mouse.get_pos()
	def enter_action_handle(self):
		if self.mouseX>450 and self.mouseX<750 and self.mouseY>700 and self.mouseY<745:
			self.breakFlag=True
	def player_enter(self):
		enterImage=pygame.image.load(image_path + 'enterImage.png').convert()
		enterImage = pygame.transform.scale(enterImage, (self.size[0], self.size[1]))
		font =  pygame.font.SysFont('microsoft Yahei',60)
		#textip=font.render(self.IP,False,(255,200,10))
		playerName=font.render(self.playerName,False,(255,200,10))
		while True:
			self.scene.blit(enterImage,(0,0))
			#self.scene.blit(textip,(555,257))
			self.scene.blit(playerName,(550,573))
			self.enter_input_handle()
			self.enter_action_handle()
			playerName=font.render(self.playerName,False,(255,255,255))
			if self.breakFlag:
				return
			pygame.display.update()
	def pause(self):
		while True:
			self.scene.blit(self.pauseImage,(0,0))
			eventList = pygame.event.get()
			for event in eventList:
				if event.type==pygame.MOUSEBUTTONDOWN:
					self.mouseX,self.mouseY=pygame.mouse.get_pos()
					if self.mouseX>425 and self.mouseX<750 and self.mouseY>340 and self.mouseY<390:
						return
					if self.mouseX>425 and self.mouseX<750 and self.mouseY>500 and self.mouseY<550:
						pygame.quit()
						exit()
			pygame.display.update()
	def playerLose(self):
		while True:
			self.scene.blit(self.loseImage,(0,0))
			eventList = pygame.event.get()
			for event in eventList:
				if event.type==pygame.MOUSEBUTTONDOWN:
					self.mouseX,self.mouseY=pygame.mouse.get_pos()
					if self.mouseX>440 and self.mouseX<780 and self.mouseY>610 and self.mouseY<660:
						self.player.reset()
						return
					if self.mouseX>440 and self.mouseX<780 and self.mouseY>720 and self.mouseY<770:
						pygame.quit()
						exit()
			pygame.display.update()
scene=Scene()
scene.net_init()
while True:
	scene.run()
